# Source and verification record

Checked **October 15, 2026**. This guide is pinned to **arXiv:2604.27979v1**, not an automatically updating paper URL.

## Primary source identity

| Field | Verified source |
| --- | --- |
| Title | *The Origins of MEV: Systematic Attribution of Arbitrage Opportunity Creation at Scale* |
| Authors, in order | Andrei Seoev; Dmitry Belousov; Anastasiia Smirnova; Ksenia Kurinova; Aleksei Smirnov; Denis Fedyanin; Yury Yanovich |
| Version and date | v1, April 30, 2026 |
| Extent | 14 PDF pages, including references on pp. 13–14 |
| Record | [Official arXiv v1 abstract and submission history](https://arxiv.org/abs/2604.27979v1) |
| PDF | [Official v1 PDF](https://arxiv.org/pdf/2604.27979v1) |
| HTML | [Official experimental HTML](https://arxiv.org/html/2604.27979v1) |
| DOI | [10.48550/arXiv.2604.27979](https://doi.org/10.48550/arXiv.2604.27979) |
| Licence | arXiv's v1 record links to [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

The arXiv DOI identifies the work generally. The versioned URLs identify the exact version read. Do not use the incomplete `https://doi.org/` in the PDF's ACM reference template as a publication DOI or infer SIGCOMM acceptance from the template.

## What was actually read

The complete 14-page official v1 PDF was downloaded and read locally, with visual inspection of the methods, table, and figure pages. The public HTML was used as a navigation aid. Section/page locators in this repository refer to the PDF; its 1-based pages match its printed pages.

Public v1 PDF inspected:

- Size: **945,083 bytes**.
- SHA-256: `89d7a8d0d7f03dfac6863747ba07326ba9369c1d3607afb65edd5eb743b4faa6`.
- 14 readable pages; title, authors, arXiv v1 marker, and content match the supplied Library paper text.

The supplied attachment was also read through Library text access. Its supported local transfer failed on the consuming Windows executor because the current transfer helper requires `os.setxattr`, which that Python environment does not provide. One supported local retry was attempted. A completed, metadata-preserving Library materialization was therefore **not established**. The official PDF was used as the disclosed fallback. Its size matches the attachment's recorded size, but **attachment byte equivalence was not verified**; no attachment hash is asserted. Private identifiers and transfer details are intentionally absent from this public repository.

The source PDF, renders, and extracted text were used for reading only and are not committed.

## Code, data, and reproducibility

The v1 PDF §6, p. 11 says non-proprietary retrospective attribution components **will be released upon publication**. It says production bot logs are proprietary and cannot be released with those artifacts. No author-designated project, code repository, or downloadable experimental dataset URL was identified in the v1 PDF or its arXiv record during this check. The arXiv record's general code-finder widgets are not author-designated artifact links.

This is a bounded check of those primary sources, not proof that no later implementation or artifact exists anywhere. Metadata keeps unverified project/code/data URLs `null`. Add them only after an author or institutional source establishes provenance, and record the check date.

The guide did not replay transactions, train the bot, access proprietary logs, run Shapley experiments, validate protocol registries, or reproduce measurements. Its static validator checks the guide's contents. Its runtime and count calculations are explicitly labelled arithmetic, not experimental measurements.

## Rights boundary

The [arXiv v1 record](https://arxiv.org/abs/2604.27979v1) links to [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the licence link was followed and confirmed during this task. [Full legal code](https://creativecommons.org/licenses/by/4.0/legalcode).

The companion paraphrases, reorganizes selected reported facts, explains notation and diagrams in new form, and adds identified commentary about uncertainty. These adaptations credit all seven authors and link the source/version and licence. See [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSE.md](LICENSE.md). Original validation code/configuration is separately [MIT-licensed](LICENSE-CODE). No paper PDF or original figure assets are redistributed.

## Presentation references

The public [corpusmap-guide](https://github.com/0xHayd3n/corpusmap-guide) and [mass-guide](https://github.com/0xHayd3n/mass-guide) were inspected for the maintainer's reading-guide scope: clear author credit, a usable README, deeper source-linked notes, agent routing, structured metadata, and an explicit absence of experimental reproduction. They are presentation references, not evidence for this paper's research claims.

## Known source conflicts

The guide retains conflicting Shapley coverage values, the unreconciled runtime statement, creator population/date/count inconsistencies, malformed AMM count, Figure 6's mixed units, a missing eight-case accounting in §5.3, algorithm/complexity ambiguities, and the conclusion-only protocol-concentration claim. See the [discrepancy record](notes/04-limitations.md) and [reported results](notes/03-results.md). None has been silently repaired or treated as a correction authorized by the authors.
