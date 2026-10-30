"""Writes repo/README.md, LICENSE, jurisdiction.json from corpus.json."""
import json
import os

from state_lib import write_docs

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'corpus.json'), encoding='utf-8'))
const = [a for a in c['acts'] if a['slug'].startswith('constitution-')]
rs = [a for a in c['acts'] if a['slug'].startswith('rsmo-chapter-')]
n = lambda acts: sum(len(a['versions'][0]['units']) for a in acts)
rows = [('constitution-*/', 'Constitution of Missouri, the preamble and one folder per article', 1, f'{len(const)} folders, {n(const)} provisions, dated 2026-10-29'),
        ('rsmo-chapter-*/', 'Revised Statutes of Missouri: chapters 556-569 (the first part of the criminal code: general provisions, sentencing, homicide and assault, sexual offenses, kidnapping, robbery, burglary and trespass), one folder per chapter', 1,
         f'{len(rs)} chapters, {n(rs)} sections, dated 2026-10-29')]
write_docs(HERE, {
    'name': 'United States (Missouri)', 'state': 'Missouri', 'code': 'US-MO', 'slug': 'missouri',
    'domain': 'revisor.mo.gov', 'acts_table': rows,
    'source': 'The [Revised Statutes of Missouri](https://revisor.mo.gov/main/Home.aspx) and the Constitution of Missouri, as posted by the Missouri Revisor of Statutes. English. The Revisor describes the site as an uncertified and unofficial posting of RSMo, identical in text to its official database; for anything that matters, read the certified RSMo. Each unit also keeps the law line and footnote the Revisor prints under the section (the enacting bills, transfers and effective dates).',
    'dates': 'The Revisor posts the current text of each chapter and, for sections amended with a later effective date, the later version too. Each act here is one version, "oldest version available", dated 2026-10-29, the day before retrieval (2026-10-30). A section holds the latest version whose effective date had already come; versions that take effect later are left out. Each section\'s effective date is printed on the Revisor\'s page, not in this history, and later builds will add later versions on top.',
    'limits': 'A first build: the Constitution of Missouri and RSMo chapters 556-569. Chapters 570-579 (stealing, weapons and the rest of the criminal code), 442 (titles and conveyances) and 351 (corporations) were planned but are not in this build: the Revisor site answered those requests with a "Loading..." or "Server busy" page, or sent the client back to its home page, and the requests were stopped rather than repeated. All other chapters are not included. There is no history before the date above. Case-note annotations the Revisor prints are not taken.',
    'license': """Source: Missouri Revisor of Statutes, https://revisor.mo.gov/ (retrieved 2026-10-30).

Statute text is not copyrightable: under the government edicts doctrine, as the Supreme Court applied it in Georgia v.
Public.Resource.Org, Inc., 590 U.S. 255 (2020), no one holds copyright in the laws that legislators make in their
official capacity. The site's "Terms of use" page reads "TBD" and its footer carries "(c) Missouri Legislature, all rights
reserved" for the website as a whole; revisor.mo.gov has no robots.txt. Only the statute text and the law-line footnotes
of the Revisor are taken; the court-decision annotations printed after Constitution sections are not.""",
})
