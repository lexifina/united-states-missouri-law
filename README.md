# United States (Missouri): law history in git

The law of Missouri as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution-*/` | Constitution of Missouri, the preamble and one folder per article | 1 | 15 folders, 403 provisions, dated 2026-10-29 |
| `rsmo-chapter-*/` | Revised Statutes of Missouri: every chapter on the Revisor's list, one folder per chapter | 1 | 457 chapters: 556-569 dated 2026-10-29 (first build), the rest dated 2026-11-02 |

**Source.** The [Revised Statutes of Missouri](https://revisor.mo.gov/main/Home.aspx) and the Constitution of Missouri, as posted by the Missouri Revisor of Statutes. English. The Revisor describes the site as an uncertified and unofficial posting of RSMo, identical in text to its official database; for anything that matters, read the certified RSMo. Each unit also keeps the law line and footnote the Revisor prints under the section (the enacting bills, transfers and effective dates).

## Dates

The Revisor posts the current text of each chapter and, for sections amended with a later effective date, the later version too. Each act here is one version, "oldest version available", dated the day before retrieval: 2026-10-29 for the first build's chapters (retrieved 2026-10-30), 2026-11-02 for the rest (retrieved 2026-11-03). A section holds the latest version whose effective date had already come; versions that take effect later are left out. Each section's effective date is printed on the Revisor's page, not in this history, and later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@revisor.mo.gov.invalid`). In this first build no dated history is available, so every commit is credited to the publisher as "oldest version available". The committer is always Lexifina.

## Limits

The Constitution of Missouri and every RSMo chapter on the Revisor's home list (chapters with no section in force are left out). There is no history before the dates above. Case-note annotations the Revisor prints are not taken.
