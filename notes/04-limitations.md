# Limitations and unresolved v1 details

These notes separate the authors' stated limits from this guide's reading checks and implementation questions. They refer to Seoev et al., *The Origins of MEV*, [arXiv:2604.27979v1](https://arxiv.org/abs/2604.27979v1), April 30, 2026. Page numbers are printed PDF pages in [the v1 paper](https://arxiv.org/pdf/2604.27979v1).

This repository explains the paper. It has not run a Polygon archive node, obtained the authors' bot logs, implemented their pipeline, reproduced their results, or established corrections to the paper. An inconsistency below is an unresolved reading issue, not a claim to know the authors' intended replacement number.

## Limits the authors acknowledge

### Constructed ground truth

The reference combines bot consensus, exact or approximate Shapley, and expert review. Agreement between those sources can share systematic errors. The authors explicitly acknowledge this in Section 5.6 (pp. 10-11). Their 200 manually reviewed events are plausibility checks, not direct observation of a unique causal source. A 100% exact-Shapley score against a reference partly defined by exact Shapley should not be read as independent validation (Sections 5.2-5.4, pp. 8-9).

### Polygon and a short historical window

The evaluation covers Polygon in February-March 2026. Block time, gas pricing, searcher competition, pool design, and transaction ordering can alter attribution patterns elsewhere. EVM compatibility makes porting conceivable; it does not establish that the 96.7% dominant-source statistic or the performance numbers transfer to Ethereum, other EVM chains, or later periods (Section 5.6, pp. 10-11).

### Atomic arbitrage only

The model targets atomic arbitrage satisfying the paper's multi-swap, nonnegative asset-balance, and positive post-cost profit criteria. Liquidations, sandwiches, top-of-block opportunities, and cross-chain behavior have different causal structures. Section 5.5 mentioning liquidation interactions as a protocol category does not turn the evaluated outcome into liquidation MEV attribution (Sections 2.2 and 3.3, pp. 2-4; Section 5.6, pp. 10-11).

### Retrospective methods and unavailable bot internals

Simulation, coefficient, and Shapley methods analyze finalized history. The bot method instead reflects real-time intent and partial mempool visibility, including missed last-in-block opportunities. The paper says the production bot logs come from an affiliated company's proprietary infrastructure and will not be released. It says other attribution components will be released upon publication; that statement is a future artifact commitment in v1, not proof that this repository contains them or that they have been independently rerun (Sections 4.2-4.3.1, pp. 4-5; Section 6, p. 11).

## Confirmed differences within v1

These differences were checked against the PDF text and the rendered evaluation pages, including Table 2 and Figures 4-6. They are preserved, not reconciled by assumption.

| Issue | Printed statements | Consequence for this guide |
| --- | --- | --- |
| Exact Shapley coverage | Section 5.2, p. 8: 12.0% for candidate sets smaller than 20. Table 2, p. 9: 98.1%. | No single verified exact-coverage value is asserted. Both are recorded with their locators. |
| Monte Carlo coverage | Section 5.2, p. 8: 100% of events. Table 2, p. 9: 98.1%. | The table value cannot silently replace the prose value, or vice versa. |
| Coverage partition | Section 5.2, p. 8 gives 12.0% exact, then describes remaining events as 2% with at least 20 candidates and 23% assigned to initial state `S0`. | Those percentages total 37%; the described partition does not account for the whole dataset as written. The categories' intended relationship needs clarification. |
| Protocol-analysis dataset | Section 5.1, p. 8: February comparison has 2,526 arbitrage events; March has 360,026. Section 5.5, p. 9 opens with March, then calls 220,262 creator transactions February data; Figure 6, p. 10 repeats February. | The dataset and denominator of protocol and concentration results remain unresolved. Creator transactions and arbitrage events are distinct units, so the counts alone do not prove which label is wrong; no mapping or scope explanation resolves them in v1. |
| Opportunity-transaction count | Section 5.5 and Figure 6 caption: 220,262. Figure 6 legend, p. 10: 220,264 unique opportunity transactions. | The difference of two is retained; neither is silently corrected. |
| AMM-involving count | Section 5.5, p. 9 prints `212,62` alongside 96.5% and 18 protocols. | Treat the count as malformed, not as a known integer. The reported percentage is preserved. |
| Runtime arithmetic | Section 5.4, p. 9: approximately 80 hours for 360,026 March events, called consistent with 12.3 ms/event. Multiplication gives approximately 74 minutes. | Timing scopes are insufficiently explained. The arithmetic is a guide check, not an alternative measured runtime. |
| Multi-source subcategories | Section 5.3, p. 8: 83 tied-maximum cases; 42 with equal positive contributors, then a remaining 33. | The described subcategories total 75, leaving 8 unspecified. The separate tied-source-size table does sum to 83. |
| Coefficient accuracy target | Table 2, p. 9 describes a triangulated accuracy reference; Section 5.4 describes 77.2% agreement with simulation. | Identify the target explicitly instead of calling the number a universally comparable accuracy score. |
| Concentration unit | Section 5.5 speaks of arbitrageurs and address-level concentration. Figure 6 plots transaction percentiles and labels unique transactions. | The reported top-1%/80% result does not establish a verified address- or entity-level concentration metric. |
| Protocol-value concentration | Section 8, p. 12 states top 5% of protocols generate 73% of value. Section 5.5 gives overlapping AMM participation frequencies, and Figure 6 concerns transaction concentration. | Keep this conclusion-only number separate; the displayed evaluation does not provide its matching protocol-value breakdown. |

The first two differences are especially consequential for claims about scalability. Exact Shapley is described as feasible only for fewer than 20 candidates; a jump from 12.0% to 98.1% changes how much of the study supposedly benefits from exact enumeration. Initial-state matches could affect reported agreement, but v1 does not give a calculation that proves they explain the conflicting percentages.

For runtime, a different end-to-end timing scope could explain some difference. Initialization, archive reads, scanning all blocks, or additional processing are possible questions to ask the authors; they are not established explanations. Using parallel hardware does not by itself reconcile a much larger aggregate time with a small per-event mean.

## Specification questions for an implementation

The following are guide interpretations or requests for clarification. They are not additional experiments.

### What counterfactual is actually evaluated?

Deterministic replay produces a definite result only after defining an initial state, transaction subset, execution order, and failure semantics. Section 4.3.4 defines a coalition value from executing its selected transactions; Algorithm 3 samples permutations to estimate marginal contributions (p. 7). A reproducible implementation must specify whether each coalition is replayed in original chain order or sampled order, and how nonce dependencies, absent prior transactions, reverted calls, balance dependencies, and block context are handled. These choices matter even when the VM itself is deterministic.

The formal candidate set contains transactions preceding the extraction (Section 3.3, p. 4). Section 5.3's Figure 3 description calls the main extraction at index 199 one of four candidates (p. 8); Figure 5 counts 17 connected transactions while the convergence text discusses 16 candidates (pp. 9-10). The figures may be counting the terminal arbitrage as a displayed node, but that is not a documented resolution of the candidate terminology. Do not add the extraction to the player set solely because it appears in a diagram.

### When is binary search valid?

Simulation searches backwards for a 95% profit drop using binary search, then computes marginal impacts (Section 4.3.2, pp. 5-6). Binary search requires a suitable monotone predicate or a documented procedure that handles non-monotone histories. Competing arbitrage can consume profit, and the Shapley examples explicitly contain negative contributions. A reader should therefore ask what guarantees the threshold-search behavior, how repeated threshold crossings are handled, and whether the implementation falls back to a scan. Deterministic replay alone does not imply monotonic profit.

Algorithm 1's early-return condition after finding the edge also needs care against the prose's threshold definition (p. 6). A future implementation should test initial-state opportunities and boundary cases against a clearly specified intended behavior, rather than assume the pseudocode is a complete executable specification.

### Which opportunity and value are being attributed?

The methods evaluate profit for an observed arbitrage transaction or route under alternative states. That is a conditional attribution target. It does not automatically reveal the globally optimal arbitrage that any searcher could invent in each counterfactual, nor does it count opportunities that nobody extracted. Candidate filtering by pools on the observed route further bounds the search space (Sections 3.2-4.3.2, pp. 4-6).

The initial-state component `S0` also matters: a pre-existing opportunity is not necessarily created by a source inside the chosen search window. Section 5.2 says initial-state attributions account for 23% of events but less than 4% of profit (p. 8). This is a statement about the window and the specified model, not proof that such value has no origin.

### What does single-source mean?

More than 70% of **positive** Shapley value is a different denominator from total net profit, especially when some players have negative contributions. A dominant maximum does not make all other causes irrelevant. Tied maximums identify one reported form of multi-source attribution; the paper does not provide a proof that every non-tied event has only one economically meaningful contributor (Section 5.3, pp. 8-9).

### What does Monte Carlo accuracy guarantee?

Section 5.3 and Figure 4 present convergence for an example and report stabilization within 5% after about 500 samples, with 1,000 used by default (pp. 9-10). They do not give a uniform per-event error guarantee, stopping rule, rank-confidence interval, or full distribution of errors. Relative error is not well-defined at a true value of zero. Even stable contribution estimates can change the largest-contributor ranking when candidates are close. The displayed standard deviation bands describe sampling variability for the illustrated case.

The Figure 4 caption describes two negative, one exactly zero, and one near-zero contribution, while the section lists a positive value near +0.0415. This labeling mismatch should not be used to redefine a contribution's sign. Figure 4's vertical axis is USD; Figure 3's explanatory values are MATIC. Keep units attached to each example.

### What can protocol participation establish?

AMM participation frequencies overlap and do not equal exclusive shares of MEV dollars. The protocol metadata comes from traces and contract-address registries; coverage and registry completeness affect grouping (Sections 5.1 and 5.5, pp. 8-10). An association between concentrated liquidity and frequent opportunity transactions does not isolate the effect of AMM design from usage, liquidity, trade sizes, or asset mix.

Similarly, the reported executed-arbitrage/creator ratio of approximately 1.6 does not measure all submitted bids, reverts, dropped attempts, or off-chain search effort. Describing it as standard multi-bid behavior is the authors' interpretation, not a direct measurement of total competitive pressure (Section 5.5, p. 10).

## What would be needed for reproduction

A reproduction effort would need inputs and decisions beyond these notes:

- Historical Polygon state for the stated block ranges and any required preceding window; execution traces, pool identification, contract metadata, and valuation inputs.
- The exact software revision and archive-node modifications; replay and counterfactual semantics; pool adapter support; fee and bid accounting; initial-state handling; and the 5% edge criterion.
- Exact event and creator identifiers, full hashes, and source-attribution outputs, including unresolved and initial-state cases.
- The validation sampling protocol, consensus rules, event-level reference labels, and separate denominators for each method and coverage category.
- Monte Carlo seeds, permutation counts and ordering semantics, convergence/error diagnostics, and tie handling.
- A timing breakdown separating block ingestion, preprocessing, state reads, attribution, aggregation, and hardware parallelism.
- An explanation or correction for the conflicting coverage values, dataset labels, counts, and concentration units listed above.
- Independent replacement bot data, or a clearly scoped evaluation without it, because the authors state that their proprietary bot component will not be released.

The paper's ethics statement discusses dual use and favors retrospective aggregated analysis (Section 9, p. 12). This guide follows that explanatory scope. It does not supply a live trading service or certify a reproduction.
