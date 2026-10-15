# Contributing

Improve the reading guide with original explanations and exact evidence. Every substantive research claim needs a v1 section, PDF page, and table/figure/algorithm locator where applicable. Link to the official source. Separate reported findings, interpretation, and derived arithmetic.

Read [AGENTS.md](AGENTS.md), [source record](SOURCES.md), and [limitations](notes/04-limitations.md) first. Preserve the paper's internal discrepancies until an author correction or explicitly compared later version resolves them. Do not silently adjust counts, percentages, pseudocode, units, or dataset labels.

This repository is documentation. An independent implementation or experiment must be clearly identified with its own protocol, dependencies, provenance, and results. Do not change the current reproduction status merely because the content validator passes.

Keep PDFs, full extracted paper text, copied figure images, private attachments, raw blockchain data, bot logs, keys, transfer metadata, and unrelated files out of Git. Cite and link external material; adding any asset requires verified rights and attribution. Guide prose and data use CC BY 4.0; original validation code uses MIT; see [licence](LICENSE.md).

Before submitting:

```sh
python scripts/validate.py
git diff --check
```

Explain what changed, which primary source supports it, and how you checked links and numerical transcription. Changes to a newer paper version should include a version comparison and an updated [source record](SOURCES.md).
