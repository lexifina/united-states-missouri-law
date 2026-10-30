# How this repository was made (United States (Missouri))

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Revised Statutes of Missouri (Revisor of Statutes) | <https://revisor.mo.gov/main/Home.aspx> | 2026-10-30 | Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site is an uncertified, unofficial posting by the Revisor; its Terms of Use page reads "TBD" and its footer claims "all rights reserved" for the site. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution-preamble` | Constitution of Missouri, Preamble | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-01` | Constitution of Missouri, Article I | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-02` | Constitution of Missouri, Article II | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-03` | Constitution of Missouri, Article III | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-04` | Constitution of Missouri, Article IV | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-05` | Constitution of Missouri, Article V | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-06` | Constitution of Missouri, Article VI | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-07` | Constitution of Missouri, Article VII | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-08` | Constitution of Missouri, Article VIII | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-09` | Constitution of Missouri, Article IX | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-10` | Constitution of Missouri, Article X | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-11` | Constitution of Missouri, Article XI | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-12` | Constitution of Missouri, Article XII | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-13` | Constitution of Missouri, Article XIII | 1 | 2026-10-29 to 2026-10-29 |
| `constitution-art-14` | Constitution of Missouri, Article XIV | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-556` | Revised Statutes of Missouri, Chapter 556 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-557` | Revised Statutes of Missouri, Chapter 557 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-558` | Revised Statutes of Missouri, Chapter 558 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-559` | Revised Statutes of Missouri, Chapter 559 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-561` | Revised Statutes of Missouri, Chapter 561 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-562` | Revised Statutes of Missouri, Chapter 562 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-563` | Revised Statutes of Missouri, Chapter 563 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-565` | Revised Statutes of Missouri, Chapter 565 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-566` | Revised Statutes of Missouri, Chapter 566 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-567` | Revised Statutes of Missouri, Chapter 567 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-568` | Revised Statutes of Missouri, Chapter 568 | 1 | 2026-10-29 to 2026-10-29 |
| `rsmo-chapter-569` | Revised Statutes of Missouri, Chapter 569 | 1 | 2026-10-29 to 2026-10-29 |

The build made 27 commits:

| Commits | Kind |
| ---: | --- |
| 27 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 27 tags.

## Dates

Each commit is dated at noon (America/Chicago) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Each act is the oldest version available, dated the day before retrieval; each section is the version whose effective date had already come. https://revisor.mo.gov/main/Home.aspx

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `76209bd31e6e039b7e8fc0f68f1db085cc9623ac05944d29b6a90938e28dc3eb` (1244475 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Each act is a single "oldest version available": the Revisor posts the current text, with no dated history of the whole chapter.
- Every act is dated 2026-10-29, the day before retrieval (2026-10-30): the site states each section is posted on its effective date, so the page is current on the retrieval day, and commits are dated noon local time, which on the retrieval day would lie in the future of the build.
- Where a chapter prints several versions of a section (an amendment with a later effective date), the unit holds the latest version whose effective date is on or before the retrieval day. Sections whose only version takes effect later, and the later versions of sections, are not included (3 section numbers in this build).
- One act per chapter and one per article of the Constitution; one unit per section number. Each unit also keeps the footnote lines the Revisor prints under the section: the law line citing the enacting bills and the transfer or effective-date note.
- Case-note annotations printed after Constitution sections (lines that begin with a year in parentheses, such as "(1954) Held that ...") are not taken.
- RSMo chapters 570-579 (stealing, weapons and the rest of the criminal code), 442 (titles and conveyances) and 351 (corporations) are not in this build: the Revisor site answered each request for those chapters with its "Loading..." or "Server busy" page, or sent the client back to its home page, and the requests were stopped there rather than repeated.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
