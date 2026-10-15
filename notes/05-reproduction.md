# Reproduction status and a credible replication plan

Reading notes on [*The Origins of MEV: Systematic Attribution of Arbitrage Opportunity Creation at Scale*, arXiv:2604.27979v1](https://arxiv.org/abs/2604.27979v1), by Andrei Seoev, Dmitry Belousov, Anastasiia Smirnova, Ksenia Kurinova, Aleksei Smirnov, Denis Fedyanin, and Yury Yanovich. See the [README](../README.md) for attribution and guide scope. All page locators below refer to v1.

## What this repository establishes

This is a reading guide. It contains explanations, source locators, arithmetic checks, and questions for a future implementation. It does **not** contain the authors' archive node, detector, Rust/C++ pipeline, bot model, searcher logs, event dataset, protocol registry, or a completed replication. No on-chain attribution experiment, method-accuracy benchmark, or runtime reproduction was performed for this guide.

Keep three evidence classes separate:

| Evidence class | What it means here |
| --- | --- |
| Author-reported result | A number or behavior described in the paper, with its original evaluation scope. |
| Guide check | A source comparison, consistency review, or transparent arithmetic calculation. |
| Future reproduction requirement | Work an independent implementation would need to complete; no claim that it has happened. |

## What the paper says was built

Section 5.1 describes a modified Geth archive node exposing historical state snapshots and transaction traces; a Rust pipeline with Python analysis wrappers; and machines with 32 physical Intel Xeon Platinum cores at 2.5-3.5 GHz and 128 GB RAM. Methods run in isolated containers. Section 6 additionally mentions C++ in performance-critical components. These are compatible descriptions at different detail levels, but do not provide buildable source or version pins by themselves. [PDF pp. 8 and 11](https://arxiv.org/pdf/2604.27979v1#page=8).

Section 6 states that non-proprietary components are containerized and that simulation, coefficient, and Shapley components **will be released upon publication**. That is a release statement in the preprint, not evidence that this guide retrieved or executed a public artifact. The affiliated company's bot execution/bidding logs are explicitly withheld as proprietary. An independent bot comparison would therefore require a different recorded searcher dataset and would not recreate the original coverage conditions. [Section 6, PDF p. 11](https://arxiv.org/pdf/2604.27979v1#page=11).

## Preserve the two principal evaluation windows

| Purpose | Reported block interval, inclusive | Reported scope |
| --- | --- | --- |
| Method comparison and single-source analysis | 82,546,747-82,567,395 | February 4, 2026, approximately 12 hours; 2,526 atomic arbitrage events. |
| Large-scale attribution and distribution analysis | 83,770,001-84,820,000 | March 2-29, 2026; 1,050,000 blocks; 360,026 events; $334,799 extracted MEV at execution-time USD prices. |

These are the paper's stated date/block mappings, not independent timestamp validation by this repository. The inclusive interval lengths are 20,649 blocks and 1,050,000 blocks respectively. The paper's separate mention of a two-million-block edge-distance analysis in Section 4.3.2 should not be silently treated as either principal window. [Sections 4.3.2 and 5.1, PDF pp. 5 and 8](https://arxiv.org/pdf/2604.27979v1#page=5).

## V1 issues that a replication must resolve

The following checks identify uncertainty in the published specification. They do not substitute corrected numbers or infer an undocumented implementation.

| Issue | What v1 reports | Why it matters |
| --- | --- | --- |
| Exact Shapley coverage | Section 5.2: 12.0%; Table 2: 98.1%. Both refer to the February study. | The denominator and eligibility policy cannot be reconstructed reliably from those conflicting values. |
| Monte Carlo coverage | Section 5.2: 100%; Table 2: 98.1%. | A reproduction needs to distinguish successful computation, valid attribution, and baseline/no-source outcomes. |
| Section 5.2 event accounting | The text gives 12.0% exact coverage and then mentions 2% computationally intractable events and 23% attributed to the starting state. | These figures do not explain a complete partition of the February events as written. Do not infer the missing share. |
| Protocol-analysis population | Section 5.5 opens with the March dataset, then labels 220,262 creator transactions as belonging to the February comparison, which Section 5.1 says has only 2,526 arbitrage events. Figure 6 repeats the February attribution, while its legend lists 220,264 opportunity transactions. | The dataset label, count, and unit need clarification. A count of many candidate transactions is conceivable, but the text calls them opportunity creators and does not explain that interpretation. |
| Whole-dataset runtime | Section 5.4 reports approximately 80 hours for simulation on 360,026 March events and calls it consistent with a mean of 12.3 ms/event. | Multiplying those two quantities gives about 74 minutes, not 80 hours. Different pipeline costs could explain it, but are not reconciled in the paper. |
| Simulation pseudocode | Algorithm 1's threshold return and marginal indexing do not clearly match its surrounding explanation. | Transcribing it directly could produce different source hashes. See [method details](02-methods.md#read-algorithm-1-with-care). |
| Coefficient cost | Table 1 gives $O(1)$, while Algorithm 2 scans candidates. | Per-update and whole-event costs must be separately specified. |
| Shapley value function | The paper defines profit after executing a coalition but does not fully define ordering, invalid transactions, retained background state, or fixed-versus-reoptimized execution. | Implementations can compute different games while all calling the output a Shapley value. |

Source locators: [Section 5.2, PDF p. 8](https://arxiv.org/pdf/2604.27979v1#page=8); [Table 2 and Sections 5.4-5.5, PDF p. 9](https://arxiv.org/pdf/2604.27979v1#page=9); [Figure 6, PDF p. 10](https://arxiv.org/pdf/2604.27979v1#page=10); [Table 1 and Algorithms 1-3, PDF pp. 6-7](https://arxiv.org/pdf/2604.27979v1#page=6).

The runtime arithmetic is a **guide check**, not a performance measurement:

```text
360,026 events x 0.0123 seconds/event = 4,428.3198 seconds
4,428.3198 / 60 = 73.80533 minutes
4,428.3198 / 3,600 = 1.23009 hours
80 hours / 360,026 events = approximately 0.800 seconds/event
```

The gap is roughly 65 times. Archive I/O, detection, trace preparation, repeated runs, or a larger timing scope are possible explanations, but this repository has no evidence selecting one. The 12.3 ms figure is a February method-comparison mean; the 80-hour figure concerns the March run. That difference in workload is relevant, yet it does not establish their claimed numerical consistency.

## A staged independent replication

The following is a proposed engineering plan, not a delivered implementation.

### Stage 1: freeze sources and acquire a verifiable chain view

Record the exact paper version, any author artifact URL and commit if one becomes available, licences, chain ID, archive-client build, historical chain configuration, and block hashes. Acquire the reported windows plus enough preceding history for the 100-block search. Verify date mappings from block timestamps rather than assuming labels are correct. Record reorg/finality handling and every unavailable state or trace.

A useful input manifest would identify each event by block hash, transaction hash, transaction index, execution status, route pools, token addresses and decimals, and the chosen state anchor. Such a manifest should be public only when its inputs and redistribution rights permit it.

### Stage 2: validate detection and profit accounting first

Implement the paper's three atomic-arbitrage criteria before attempting source attribution. Reconcile successful swaps, token flows, gas, priority bids, internal transfers, and the chosen normalization currency. Document the USD price source and timestamp convention independently from the MATIC calculation. Avoid counting a fee twice when computing net profit.

Validate ordinary replay against canonical receipts/logs and observed balances before running counterfactuals. Record discrepancies instead of forcing the event count to match 2,526 or 360,026. Decisions about token behavior, protocol versions, and unsupported pools can change event inclusion and must be reported. [Sections 2.2, 3.2-3.3, and 5.1, PDF pp. 3-4 and 8](https://arxiv.org/pdf/2604.27979v1#page=3).

### Stage 3: publish a precise counterfactual contract

Before measuring agreement, specify:

- The exact initial state and block environment for a same-block or multi-block query.
- Candidate discovery and treatment of noncandidate transactions.
- Whether a historical prefix, removal-with-suffix replay, or another intervention is being evaluated.
- Whether the observed arbitrage calldata, amount, and route remain fixed; if optimization is added, describe it as a separate variant.
- Handling of transaction dependencies, invalid nonces, insufficient balances, reverts, missing state, and unsupported contracts.
- The profit value for unsuccessful hypothetical execution and the treatment of fees/bids under a changed position.
- The definition of a pre-existing opportunity, no-source result, and unattributable event.
- A reviewed resolution of Algorithm 1's threshold and indexing issues, with any departure from the printed v1 algorithm disclosed.

Deterministic replay is necessary for repeatability. It does not eliminate these modeling choices. A canonical-order coalition and a reordered coalition can have different values even when both execute deterministically.

### Stage 4: implement and verify the four interfaces separately

| Component | Minimum independent checks |
| --- | --- |
| Coefficient | Protocol-specific reserve/price updates; route direction; candidate scan; positive maximum and tie behavior; distinguish infinitesimal rate from finite-size profit. |
| Simulation | Compare edge search with a complete position scan on small cases; exercise multiple threshold crossings; verify transaction/hash indexing and terminal boundaries; retain all local impacts for inspection. |
| Exact Shapley | Cache explicit coalition values for small candidate sets; verify efficiency against $V(C)-V(\varnothing)$ and symmetry/dummy examples; inspect negative contributions. |
| Monte Carlo Shapley | Record seeds and permutation policy; compare against exact values on feasible cases; report uncertainty and source-ranking stability, especially near zero or ties. |
| Bot reference | Record source/route/bid tuples, threshold, observation window, and missingness; preserve the distinction between predicted intent and finalized outcome. |

For a transparent illustrative implementation, small synthetic fixtures could cover one clear creator, a tied interaction, a negative contributor, a baseline-only case, and a dependency-induced failure. Such fixtures would validate the implementation's stated semantics; they would not reproduce empirical Polygon results.

### Stage 5: reconstruct validation without circular labels

The paper triangulates bot evidence, Shapley attribution, and expert review of 200 stratified events, with agreement of at least two sources defining correctness. An independent report should publish the event-level eligibility and matching rules, stratification and sampling procedure, manual-review rubric, and which references were available for each event. It should state whether baseline/no-source matches are counted and how ties or multiple-source sets are compared. [Section 5.2, PDF p. 8](https://arxiv.org/pdf/2604.27979v1#page=8).

Report numerator and denominator for every metric. In particular, distinguish exact-computable events, Monte Carlo-computed events, valid source assignments, baseline assignments, unsupported events, and failed executions. Do not treat agreement with the same Shapley definition as independent proof of causal correctness. Table 2's 77.2% coefficient accuracy also needs careful comparison: Section 5.4 describes it as agreement with simulation, while the table caption describes a triangulated reference for non-Shapley methods. Preserve the chosen comparator explicitly. [Table 2 and Section 5.4, PDF p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).

### Stage 6: measure costs and distributions with clear units

Measure method kernel time, state/trace access, preprocessing/detection, and total elapsed time separately. Record machine count, actual CPU allocation, parallelism, warm/cold caches, hardware, failures, and event-level latency distribution. Compare February and March workloads only after describing their differences. The printed asymptotic summaries omit some replay and I/O costs and should not be used to derive a hardware-independent throughput claim.

For protocol results, record the registry version, unknown-address share, multi-protocol labeling rules, and whether the unit is a transaction, sender address, protocol, event, or attributed value. The reported AMM participation percentages overlap; adding them as a disjoint market-share distribution would be incorrect. Keep March distribution analyses separate from February method comparisons until the v1 population inconsistency is resolved. [Sections 5.4-5.6, PDF pp. 9-10](https://arxiv.org/pdf/2604.27979v1#page=9).

## Conditions for calling a future result a reproduction

A credible report would provide executable public code with immutable versions, a data/state acquisition manifest, a complete counterfactual specification, deterministic small-case checks, event-level validation denominators, and benchmark scope. It would separate matched claims from deviations, unresolved source inconsistencies, unavailable proprietary references, and results that fail to match.

Until those artifacts and checks exist, the defensible outcome is a source-grounded understanding of the paper and a replication plan. That is the status of this repository.
