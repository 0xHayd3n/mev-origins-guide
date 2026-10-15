# Results: what the authors report

This is a reading guide to Andrei Seoev, Dmitry Belousov, Anastasiia Smirnova, Ksenia Kurinova, Aleksei Smirnov, Denis Fedyanin, and Yury Yanovich, *The Origins of MEV: Systematic Attribution of Arbitrage Opportunity Creation at Scale*, [arXiv:2604.27979v1](https://arxiv.org/abs/2604.27979v1), April 30, 2026. The results below belong to the paper's authors. This repository did not run their attribution system, reconstruct Polygon state, or reproduce their measurements.

**Reading rule:** method scores describe the small February comparison dataset; March supplies the large-scale event count and extracted value. Some later v1 passages blur those scopes. We preserve their wording and flag the unresolved issues in [limitations](04-limitations.md), rather than silently repairing them. Page references are the PDF's printed page numbers; all refer to [the v1 PDF](https://arxiv.org/pdf/2604.27979v1).

## 1. Two evaluation datasets

| Dataset | Stated scope | Reported events and purpose | Source |
| --- | --- | --- | --- |
| Large-scale attribution | Polygon blocks 83,770,001-84,820,000; March 2-29, 2026 | 360,026 atomic arbitrage transactions; $334,799 extracted MEV; basis for protocol distribution analysis | Section 5.1, p. 8 |
| Method comparison | Polygon blocks 82,546,747-82,567,395; near 12-hour window on February 4, 2026 | 2,526 atomic arbitrage events; comparison of methods and validation of the single-source hypothesis | Section 5.1, p. 8 |

The March block range contains 1,050,000 blocks when both endpoints are included, matching the introduction's count (Section 1, p. 2). That is a guide arithmetic check of the printed endpoints, not a fresh chain query.

The paper reports USD values at execution-time oracle prices and internal computations in MATIC. Its setup uses a modified Geth archive node, transaction traces and historical snapshots, Rust components with Python analysis wrappers, and machines described as having 32 physical Intel Xeon Platinum cores at 2.5-3.5 GHz and 128 GB RAM. Attribution methods run in isolated containers (Section 5.1, p. 8). These are the authors' environment descriptions, not hardware or software provided by this repository.

## 2. How the benchmark is constructed

The February comparison uses three sources of validation (Section 5.2, p. 8):

1. **Bot consensus:** consistent targeting of an opportunity source by independent searchers. This covers 38.4% of events and omits last-in-block atomic arbitrage by design. These are live expectations about causes, which can differ from a retrospective analysis of finalized execution.
2. **Shapley attribution:** exact enumeration where the candidate set has fewer than 20 transactions, and Monte Carlo approximation elsewhere. The section states 12.0% exact coverage and 100% Monte Carlo coverage; Table 2 reports 98.1% for each. Both versions are retained below.
3. **Manual plausibility review:** 200 stratified events. The paper labels an attribution correct when it agrees with at least two validation sources. It also counts agreement on an initial-state attribution, `S0` or no in-block source, as a match.

The word **accuracy** therefore means agreement with this constructed reference. It does not establish access to an independent, directly observed causal label. Shared error between validation sources remains possible.

## 3. Reported method comparison

The following is a numerical transcription of Table 2, not a new benchmark. Its caption defines coverage as the fraction of events with a valid attribution and time as mean execution time per event. Accuracy is against triangulated ground truth, or exact Shapley for the Shapley rows (Table 2, p. 9; February dataset, 2,526 events).

| Method | Accuracy as printed | Coverage as printed | Mean time as printed |
| --- | ---: | ---: | ---: |
| Bot-data | 94.2% | 38.4% | 8 ms |
| Simulation | 91.7% | 99.1% | 12.3 ms |
| Coefficient | 77.2% | 88.4% | 0.8 ms |
| Shapley, exact | 100% | 98.1% | approximately 5 min |
| Shapley, Monte Carlo, 1,000 samples | 100% | 98.1% | 2.1 s |

Interpret these figures with three qualifications:

- **Different available subsets:** the bot's high score covers only 38.4% of events. The table does not establish that it outperforms simulation across the full dataset.
- **Different descriptions of the coefficient target:** Section 5.4 calls the coefficient method's 77.2% result agreement with simulation; the table caption describes a triangulated reference. Preserve this distinction when citing the number.
- **Shapley reference dependence:** exact Shapley defines part of the reference, so its 100% entry is not an independent accuracy test. A Monte Carlo estimate also need not numerically equal an exact Shapley vector simply because both implement the same value definition. The paper's 100% attribution score is not a guarantee of zero estimation error for every contribution.

The authors recommend coefficient screening, simulation for the main workload, Shapley when methods disagree or multiple sources appear important, and bot evidence as an external validation layer (Sections 4.2 and 5.4, pp. 5 and 9). The reported combination of 91.7% accuracy and 99.1% coverage motivates simulation's role in that workflow. This is their practical recommendation within the evaluated setting.

## 4. Single-source attribution

The paper's central empirical claim is that **96.7% of February events have one transaction responsible for more than 70% of total positive Shapley value**. The next largest contributor is described as typically below 5% (Section 5.3, pp. 8-9). This is a dominance criterion. It does not mean all other transactions have zero influence or that one transaction explains all profit in every such event.

The authors report 83 events, or 3.3%, with tied maximum Shapley values:

| Number of tied sources | Reported events |
| ---: | ---: |
| 2 | 71 |
| 3 | 8 |
| 4 | 2 |
| 6 | 2 |
| Total | 83 |

Section 5.3 associates 42 of the 83 cases, 50.6%, with equal values for all positive contributors, often in last-in-block cycles. It then describes a remaining 33 cases as last-in-block cascades. Those descriptions account for 75 cases, leaving 8 unclassified in that paragraph. They should not be presented as an exhaustive partition.

The supported takeaway is that a dominant source is common **under the paper's attribution model on its February Polygon sample**. The result does not validate a universal single-source law across all MEV categories, chains, periods, or candidate definitions.

## 5. What the Shapley examples demonstrate

**Creation and consumption can have opposite signs.** In the example from block 82,563,006, a non-arbitrage swap at transaction index 129 receives approximately +32.58 MATIC, while competing arbitrageurs at indices 130 and 168 receive approximately -12.50 and -2.75 MATIC. The positive contribution represents creating opportunity; negative contributions represent consuming available profit (Section 5.3 and Figure 3, p. 8). The figure's treatment of the final arbitrage as one of four candidates differs from the formal preceding-transaction set; see [the specification caveats](04-limitations.md#specification-questions-for-an-implementation).

**Sampling reduces the enumeration burden.** For an example identified as transaction `0xb1f2a5bb...` in block 82,554,874, Section 5.3 describes 16 potentially nonzero candidates. Exact enumeration entails 65,536 subsets, or `2^16`. The authors say sample estimates stabilize within 5% of asymptotic values after about 500 permutations and choose 1,000 samples by default. Figure 4 shows means and one standard deviation over 100 runs for four example contributions (Section 5.3, p. 9; Figure 4, p. 10).

This example supports an empirical convergence observation, not a general error bound for every event. Relative error also needs care for zero or near-zero values. Figure 4's caption describes two negative values, an exactly zero value, and a near-zero value, while the positive example in the main text is about +0.0415; retain the actual signs when discussing the plot.

**Complex participation can still have a dominant creator.** Figure 5 depicts the same block and truncated event identifier with 17 connected transactions, including competing arbitrageurs and a main arbitrage at index 346. The authors use this case to illustrate a dominant source amid many interactions (Section 5.3, p. 9; Figure 5, p. 10). Do not infer full transaction hashes from the abbreviated labels or equate the figure's connected-node count with the preceding-candidate count without checking the underlying data.

## 6. Protocol participation and concentration

Section 5.5 opens by saying that simulation was applied to the 360,026 March events. Its AMM paragraph then labels 220,262 opportunity-creating transactions as belonging to the February comparison dataset; Figure 6 repeats that February label. This scope conflict prevents a confident assignment of the following distribution statistics to either dataset. They remain **reported v1 statistics with unresolved dataset labeling** (Section 5.5, pp. 9-10; Figure 6, p. 10).

The authors report identifiable AMMs in 96.5% of opportunity-creating transactions, spanning 18 protocols. The associated count is malformed in the PDF as `212,62`; this guide does not invent a missing digit. The reported participation frequencies are:

| AMM | Reported share of opportunity transactions involving it |
| --- | ---: |
| Uniswap V3 | 58.0% |
| Algebra | 29.6% |
| Uniswap V4 | 28.9% |
| Uniswap V2 | 23.2% |
| DODO | 8.2% |

These are overlapping transaction participation frequencies. An opportunity transaction may interact with several AMMs, so the percentages can exceed 100% in total. They are not mutually exclusive shares of extracted dollar value. The paper interprets the prominence of concentrated-liquidity AMMs as suggesting frequent arbitrageable price imbalances; it does not isolate AMM design as a causal treatment against liquidity, flow, volume, or user composition (Section 5.5, p. 9).

For concentration, Section 5.5 and Figure 6 report that the top 1% of arbitrageurs or arbitrage transactions account for about 80% of extracted value, and that the highest-ranked 1% of opportunity creators have a similar concentration. The unit is inconsistent: prose uses arbitrageurs and address-level concentration, while the figure's axes and legend use transactions. Its legend gives 360,026 arbitrage transactions and 220,264 opportunity transactions; the caption gives 220,262 opportunity transactions. This guide does not convert that into a verified address-level statistic.

The paper also reports roughly 1.6 successfully executed arbitrage transactions per opportunity-creating transaction. For scale, the printed counts `360,026 / 220,262` yield about 1.635, which is compatible with the rounded ratio but does not resolve the dataset-label conflict. Executed transactions do not measure all attempted bids, failed transactions, or unseen competition (Section 5.5, p. 10).

Section 8 additionally states that the top 5% of protocols generate 73% of value (p. 12). Section 5.5 and Figure 6 do not show a matching protocol-value table from which to check that claim. Keep it distinct from the top-1%-of-transactions claim and from AMM participation frequencies.

## 7. Runtime: preserve both statements

Section 5.4 reports approximately **80 hours** to process the full March dataset with simulation and says this is consistent with the per-event mean. Table 2's simulation mean is **12.3 ms/event** (p. 9).

The guide's arithmetic check is:

```text
360,026 events * 12.3 ms/event
= 4,428.3198 seconds
= 73.80533 minutes
= 1.23009 hours
```

The aggregate does not follow directly from the printed mean and event count. A broader scope, initialization, data retrieval, preprocessing, or different timing boundary might matter, but v1 does not supply a breakdown that establishes any of those explanations. Neither 80 hours nor 74 minutes should be advertised as a reproduced end-to-end runtime.

## 8. What a careful reader can conclude

The paper makes a useful distinction between extracting MEV and attributing the on-chain state changes that created its opportunity. Its reported comparison favors simulation as a cost-coverage compromise, and its Shapley analysis suggests dominant creators are common in the February sample. The precise coverage, protocol-distribution denominator, concentration unit, and end-to-end timing need clarification before being used as benchmark targets or generalized design claims.

For machine-readable numerical statements, see [results.json](../data/results.json). Its conflict records are part of the data: do not discard them when summarizing the table.
