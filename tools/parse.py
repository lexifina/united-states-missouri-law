"""Parse the cached Revisor of Statutes pages into corpus.json. Reads only .cache; no network."""
import json
import os
import re
import sys
from datetime import date

from bs4 import BeautifulSoup

from state_lib import Act, Fetcher, key, norm, sha, text_of, write_corpus

HERE = os.path.dirname(os.path.abspath(__file__))
F = Fetcher(HERE, 'x')
RETRIEVED = '2026-10-30'
ASOF = date(2026, 10, 30)
VERSION_DATE = '2026-10-29'   # day before retrieval: commits are dated noon local time, so the retrieval day would lie in the future
DASH = re.compile(r'^-{5,}\s*(\S+)\s+(\d{1,2}/\d{1,2}/\d{4})\s*-{5,}$')


def when(s):
    m, d, y = map(int, s.split('/'))
    return date(y, m, d)


def soup(url):
    b = F.cached(url)
    return BeautifulSoup(b.decode('utf-8', 'replace'), 'lxml'), b


def section_of(div):
    """(heading, lines) of one div.norm: the bold lead-in, the paragraphs, then the footnote lines."""
    bold = div.find('span', class_='bold')
    head = norm(bold.get_text(' ')) if bold else ''
    head = re.sub(r'\s*[-—]+$', '', head).strip().replace('*', '').strip()
    lines = []
    first = True
    for p in div.find_all('p', recursive=False):
        if first and bold:
            bold.extract()
        first = False
        lines.append(norm(p.get_text(' ')))
    for fp in div.select('div.foot p'):
        t = norm(fp.get_text(' '))
        if t and not re.fullmatch(r'-+', t) and not re.match(r'\(\d{4}\)', t):   # "(1954) Held that ..." is a case note
            lines.append(t)
    return head, [l for l in lines if l]


def chapter_sections(s):
    """-> [{num, date, head, lines}] in page order; one entry per printed version."""
    out, pending = [], None
    first = s.find('div', class_='norm')
    if first is None:
        return out
    box = first.parent
    for el in box.children:
        name = getattr(el, 'name', None)
        if name == 'div' and 'norm' in (el.get('class') or []):
            head, lines = section_of(el)
            pending = {'head': head, 'lines': lines}
        elif name == 'p' and pending is not None:
            m = DASH.match(norm(el.get_text(' ')))
            if m:
                pending['num'], pending['date'] = m.group(1), when(m.group(2))
                out.append(pending)
                pending = None
    return out


def current(entries):
    """The latest version of each section already in force on the retrieval day, in first-seen order."""
    best, order = {}, []
    for e in entries:
        if e['date'] > ASOF:
            continue
        if e['num'] not in best:
            order.append(e['num'])
        if e['num'] not in best or e['date'] >= best[e['num']]['date']:
            best[e['num']] = e
    return [best[n] for n in order]


def statutes(man):
    acts, skipped = [], 0
    for ch in man['chapters']:
        if F.cached(ch['url']) is None:     # the Revisor never served this chapter (see decisions)
            continue
        s, b = soup(ch['url'])
        box = s.find('div', class_='lr-font-norm')
        txt = norm(box.get_text(' ')) if box else ''
        m = re.search(r'Chapter\s+' + ch['num'] + r'\s+(.*?)\s*(?:✹|⚿|$)', txt)
        name = m.group(1).strip() if m else ''
        a = Act(f'rsmo-chapter-{key("", ch["num"], 3)}', f'RSMo ch. {ch["num"]}',
                f'Revised Statutes of Missouri, Chapter {ch["num"]}' + (f': {name}' if name else ''), ch['url'], VERSION_DATE)
        entries = chapter_sections(s)
        cur = current(entries)
        skipped += len({e['num'] for e in entries}) - len(cur)
        for e in cur:
            lab = e['num']
            a.add(key('sec', lab, 3), f'RSMo {lab}', 'section', text_of(['# ' + e['head']] + e['lines']))
        a.sha256 = sha(b)
        acts.append(a)
    return acts, skipped


def constitution(man):
    acts = []
    s, b = soup(man['constit_home'])
    em = [e for e in s.find_all('em') if e.get_text().startswith('We, the people')]
    pre = Act('constitution-preamble', 'Mo. Const. preamble', 'Constitution of Missouri, Preamble', man['constit_home'], VERSION_DATE, sha256=sha(b))
    if em:
        pre.add('preamble', 'Preamble', 'preamble', text_of(['# Preamble', em[0].get_text(' ')]))
    acts.append(pre)
    for i, art in enumerate(man['articles'], start=1):
        s, b = soup(art['url'])
        a = Act(f'constitution-art-{i:02d}', f'Mo. Const. art. {art["article"]}', f'Constitution of Missouri, Article {art["article"]}',
                art['url'], VERSION_DATE, sha256=sha(b))
        for d in s.find_all('div', class_='norm'):
            head, lines = section_of(d)
            m = re.match(r'([IVXLC]+)\s+Section\s+(\S+?)\.?\s', head + ' ')
            lab = m.group(2) if m else head
            a.add(key('sec', lab, 3), f'Art. {art["article"]}, Section {lab}', 'section', text_of(['# ' + head] + lines))
        acts.append(a)
    return acts


def main():
    man = json.load(open(os.path.join(HERE, '.cache', 'manifest.json')))
    st, skipped = statutes(man)
    acts = constitution(man) + st
    country = {'code': 'US-MO', 'name': 'United States (Missouri)', 'slug': 'united-states-missouri', 'lang': 'en',
               'tz': 'America/Chicago', 'future_branch': 'future',
               'publisher': {'name': 'Missouri Revisor of Statutes', 'email': 'rsmo@revisor.mo.gov.invalid'},
               'default_in_force_rule': {'text': 'Each act is the oldest version available, dated the day before retrieval; each section is the version whose effective date had already come.',
                                         'source': 'https://revisor.mo.gov/main/Home.aspx'},
               'licence_note': 'Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). Source: Missouri Revisor of Statutes, an unofficial posting.'}
    sources = [{'name': 'Revised Statutes of Missouri (Revisor of Statutes)', 'url': 'https://revisor.mo.gov/main/Home.aspx', 'retrieved': RETRIEVED,
                'licence': 'Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site is an uncertified, unofficial posting by the Revisor; its Terms of Use page reads "TBD" and its footer claims "all rights reserved" for the site; it has no robots.txt.',
                'notes': 'Constitution of Missouri (14 articles and the preamble) and RSMo chapters 556-569 (chapters 560 and 564 are not used in RSMo). Court-decision annotations the Constitution pages print are not taken.'}]
    decisions = [
        'Each act is a single "oldest version available": the Revisor posts the current text, with no dated history of the whole chapter.',
        f'Every act is dated {VERSION_DATE}, the day before retrieval ({RETRIEVED}): the site states each section is posted on its effective date, so the page is current on the retrieval day, and commits are dated noon local time, which on the retrieval day would lie in the future of the build.',
        'Where a chapter prints several versions of a section (an amendment with a later effective date), the unit holds the latest version whose effective date is on or before the retrieval day. Sections whose only version takes effect later, and the later versions of sections, are not included (' + str(skipped) + ' section numbers in this build).',
        'One act per chapter and one per article of the Constitution; one unit per section number. Each unit also keeps the footnote lines the Revisor prints under the section: the law line citing the enacting bills and the transfer or effective-date note.',
        'Case-note annotations printed after Constitution sections (lines that begin with a year in parentheses, such as "(1954) Held that ...") are not taken.',
        'RSMo chapters 570-579 (stealing, weapons and the rest of the criminal code), 442 (titles and conveyances) and 351 (corporations) are not in this build: the Revisor site answered each request for those chapters with its "Loading..." or "Server busy" page, or sent the client back to its home page, and the requests were stopped there rather than repeated.']
    write_corpus(HERE, country, sources, acts, decisions)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    main()
