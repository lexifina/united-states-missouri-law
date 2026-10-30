# United States (Missouri): law history in git

The law of Missouri as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution-*/` | Constitution of Missouri, the preamble and one folder per article | 1 | 15 folders, 403 provisions, dated 2026-10-29 |
| `rsmo-chapter-*/` | Revised Statutes of Missouri: chapters 556-569 (the first part of the criminal code: general provisions, sentencing, homicide and assault, sexual offenses, kidnapping, robbery, burglary and trespass), one folder per chapter | 1 | 12 chapters, 262 sections, dated 2026-10-29 |

**Source.** The [Revised Statutes of Missouri](https://revisor.mo.gov/main/Home.aspx) and the Constitution of Missouri, as posted by the Missouri Revisor of Statutes. English. The Revisor describes the site as an uncertified and unofficial posting of RSMo, identical in text to its official database; for anything that matters, read the certified RSMo. Each unit also keeps the law line and footnote the Revisor prints under the section (the enacting bills, transfers and effective dates).

## Dates

The Revisor posts the current text of each chapter and, for sections amended with a later effective date, the later version too. Each act here is one version, "oldest version available", dated 2026-10-29, the day before retrieval (2026-10-30). A section holds the latest version whose effective date had already come; versions that take effect later are left out. Each section's effective date is printed on the Revisor's page, not in this history, and later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@revisor.mo.gov.invalid`). In this first build no dated history is available, so every commit is credited to the publisher as "oldest version available". The committer is always Lexifina.

## Limits

A first build: the Constitution of Missouri and RSMo chapters 556-569. Chapters 570-579 (stealing, weapons and the rest of the criminal code), 442 (titles and conveyances) and 351 (corporations) were planned but are not in this build: the Revisor site answered those requests with a "Loading..." or "Server busy" page, or sent the client back to its home page, and the requests were stopped rather than repeated. All other chapters are not included. There is no history before the date above. Case-note annotations the Revisor prints are not taken.
