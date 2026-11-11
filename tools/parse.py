"""Offline Missouri current-text parser: full normative DOM and source dates.

Usage: python parse.py --cache CACHE --base corpus/rework-input.json --output OUTPUT --as-of YYYY-MM-DD
The cache holds official HTML named sha256(URL).html or raw/sha256(URL).
"""
import argparse, json, re, hashlib, copy
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
ASOF = None
CACHE = None
DASH = re.compile(r'^-{5,}\s*(\S+)\s+(\d{1,2}/\d{1,2}/\d{4})\s*-{5,}$')
def source(url):
    k=hashlib.sha256(url.encode()).hexdigest()
    for p in (CACHE/(k+'.html'), CACHE/'raw'/k, CACHE/k):
        if p.exists():return p.read_bytes()
    raise FileNotFoundError('Official source HTML absent: '+url)

def norm(t):
    t = t.translate(str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‒': '-', '‑': '-', '\u200b': '', '\ufeff': '', '\xad': ''}))
    return re.sub('\\s+', ' ', t).strip()

def key(label):
    return 'sec-' + re.sub('\\d+', lambda m: m.group(0).zfill(3), re.sub('[^a-z0-9]+', '-', label.lower()).strip('-'))

def section(div):
    bold = div.find('span', class_='bold')
    head = norm(bold.get_text(' ')) if bold else ''
    head = re.sub('\\s*-+$', '', head).strip().replace('*', '').strip()
    if bold:
        bold.extract()
    for p in div.select('div.foot p'):
        t = norm(p.get_text(' '))
        if re.fullmatch('-+', t) or re.match('^\\(\\d{4}\\)', t):
            p.extract()
    pieces = []

    def walk(node):
        if isinstance(node, NavigableString):
            pieces.append(str(node) + ' ')
        elif isinstance(node, Tag):
            for child in node.children:
                walk(child)
            if node.name in ('p', 'tr', 'br'):
                pieces.append('\n')
    walk(div)
    lines = [norm(x) for x in ''.join(pieces).split('\n')]
    return '# ' + head + '\n' + '\n'.join((x for x in lines if x)) + '\n'

def parse_chapter(ch, old):
    url = 'https://revisor.mo.gov/main/ViewChapter.aspx?chapter=' + ch
    b = source(url)
    soup = BeautifulSoup(b.decode('utf-8', 'replace'), 'lxml')
    selected = {}
    printed = {}
    for div in soup.find_all('div', class_='norm'):
        match = None
        for sib in div.next_siblings:
            if isinstance(sib, Tag) and sib.name == 'div' and ('norm' in (sib.get('class') or [])):
                break
            if isinstance(sib, Tag) and sib.name == 'p':
                match = DASH.fullmatch(norm(sib.get_text(' ')))
                if match:
                    break
        if not match:
            continue
        num, dt = match.groups()
        m, d, y = map(int, dt.split('/'))
        day = date(y, m, d).isoformat()
        if day > ASOF:
            continue
        printed.setdefault(num, []).append({'div': div, 'date': day, 'quote': match.group(0)})
        if num not in selected or selected[num]['date'] <= day:
            selected[num] = {'div': div, 'date': day, 'quote': match.group(0)}
    alternatives = []
    for num, forms in printed.items():
        if len(forms) < 2:
            continue
        restored = []
        for entry in forms:
            notes = [norm(p.get_text(' ')) for p in entry['div'].select('div.foot p')]
            if any('reprinted in accordance' in n.lower() and
                   ('ineffective' in n.lower() or 'current version' in n.lower()) and
                   'other printed version' not in n.lower() for n in notes):
                restored.append(entry)
        if restored:
            if len(restored) != 1:
                raise ValueError('Ambiguous express Revisor restoration: ' + num)
            selected[num] = restored[0]
        else:
            # Dates do not resolve conflicting enactments or contingent commencement.
            # Preserve every printed form; do not synthesize historical chapter states.
            chosen = selected[num]
            for index, entry in enumerate(forms, 1):
                if entry['div'] is not chosen['div']:
                    alternatives.append((num, index, entry))
    if not selected:
        return (None, {'chapter': ch, 'sections': 0, 'excluded': True})
    slug = 'rsmo-chapter-' + ch.zfill(3)
    a = copy.deepcopy(old.get(slug)) if slug in old else {'slug': slug, 'short': 'RSMo ch. ' + ch, 'title': 'Revised Statutes of Missouri, Chapter ' + ch, 'url': url, 'first_law': None, 'earlier_laws': []}
    witness = max(selected.values(), key=lambda e: e['date'])
    units = {}
    images = 0
    for num, e in selected.items():
        images += len(e['div'].find_all(['img', 'svg']))
        units[key(num)] = {'label': 'RSMo ' + num, 'kind': 'section', 'text': section(e['div'])}
    for num, index, entry in alternatives:
        images += len(entry['div'].find_all(['img', 'svg']))
        unit = key(num) + '-variant-' + entry['date'] + '-' + str(index)
        units[unit] = {'label': 'RSMo ' + num + ' (alternative printed version)',
                       'kind': 'section', 'text': section(entry['div'])}
    a['versions'] = [{'from': witness['date'], 'source_url': url, 'sha256': hashlib.sha256(b).hexdigest(), 'in_force_basis': 'Latest current section effective date printed by the Revisor: ' + witness['quote'], 'units': dict(sorted(units.items()))}]
    return (a, {'chapter': ch, 'sections': len(units), 'source_images': images, 'referenced': 0, 'omitted': 0, 'date': witness['date'], 'quote': witness['quote'], 'sha256': hashlib.sha256(b).hexdigest()})

def main():
    global ASOF,CACHE
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cache',required=True)
    ap.add_argument('--base',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--as-of',required=True)
    args=ap.parse_args();ASOF=args.as_of;date.fromisoformat(ASOF);CACHE=Path(args.cache)
    c=json.loads(Path(args.base).read_text(encoding='utf-8'))
    old={a['slug']:a for a in c['acts']}
    listing=source('https://revisor.mo.gov/main/Home.aspx')
    chapters=sorted(set(re.findall(rb'OneChapter\.aspx\?chapter=(\d+)',listing)),key=int)
    acts=[]
    for ch in chapters:
        a,evidence=parse_chapter(ch.decode(),old)
        if evidence.get('source_images',0):raise ValueError('Normative images require an asset-capable build: '+ch.decode())
        if a:acts.append(a)
    homeurl='https://revisor.mo.gov/main/Home.aspx?constit=y'
    home=BeautifulSoup(source(homeurl).decode('utf-8','replace'),'lxml')
    dates={};quotes={}
    for tr in home.find_all('tr'):
        text=norm(tr.get_text(' '));m=re.match(r'^([IVXLC]+)\s+\S+.*\((\d{1,2}/\d{1,2}/\d{4})\)',text)
        if not m:continue
        roman,dt=m.groups();month,day,year=map(int,dt.split('/'));dt=date(year,month,day).isoformat()
        if dt<=ASOF and dates.get(roman,'')<dt:dates[roman]=dt;quotes[roman]=text
    for prior in c['acts']:
        if not prior['slug'].startswith('constitution-'):continue
        a=copy.deepcopy(prior);units={};raw=source(a['url'])
        soup=BeautifulSoup(raw.decode('utf-8','replace'),'lxml')
        if a['slug']=='constitution-preamble':
            em=next(e for e in soup.find_all('em') if e.get_text().startswith('We, the people'))
            units={'preamble':{'label':'Preamble','kind':'preamble','text':'# Preamble\n'+norm(em.get_text(' '))+'\n'}}
        else:
            roman=a['short'].split()[-1]
            for d in soup.find_all('div',class_='norm'):
                if d.find(['img','svg']):raise ValueError('Normative Constitution image requires asset support')
                bold=d.find('span',class_='bold');head=norm(bold.get_text(' ')) if bold else ''
                head=re.sub(r'\s*-+$','',head).strip().replace('*','').strip()
                m=re.match(r'[IVXLC]+\s+Section\s+(\S+?)\.?\s',head+' ');label=m.group(1) if m else head
                k=key(label);base=k;n=2
                while k in units:k=base+'-dup'+str(n);n+=1
                units[k]={'label':f'Art. {roman}, Section {label}','kind':'section','text':section(d)}
            if dates.get(roman,'1945')>'1945-12-31':
                a['versions'][0]['from']=dates[roman]
                a['versions'][0]['in_force_basis']='Latest current section date displayed in the Revisor Constitution listing: '+quotes[roman]
        a['versions'][0]['units']=dict(sorted(units.items()));a['versions'][0]['sha256']=hashlib.sha256(raw).hexdigest()
        acts.append(a)
    for a in acts:
        a.pop('correction',None)
        if a['slug'] in old:
            prior=old[a['slug']]['versions'][0]['units']
            for k,u in a['versions'][0]['units'].items():
                if k in prior and norm(prior[k]['text'])==norm(u['text']):u['text']=prior[k]['text']
    c['acts']=sorted(acts,key=lambda a:a['slug']);c.pop('_docs_date',None)
    Path(args.output).write_text(json.dumps(c,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    print('Current acts',len(acts),'source listed chapters',len(chapters))
if __name__=='__main__':main()
