# Figures, tables, and algorithms

The [arXiv v1 PDF](https://arxiv.org/pdf/2604.27979v1) contains **6 numbered figures, 2 numbered tables, and 3 numbered algorithms**. This inventory paraphrases what each item is intended to communicate and records cautions visible in the paper. No paper image or PDF is redistributed here. Numerical values are authors' reports unless explicitly labeled as guide-derived checks; none has been reproduced by this repository.

## Figure 1 - A two-pool atomic arbitrage

**Location:** Section 2.2, [PDF p. 3](https://arxiv.org/pdf/2604.27979v1#page=3).

The diagram follows stablecoin and WMATIC flows between a receiver, a Uniswap V3 pool, and a Uniswap V2 pool. Its purpose is to make the atomic-arbitrage detector concrete: multiple swaps, no negative net change in any involved asset, and positive profit after costs. The caption identifies Polygon block 58,329,504, transaction prefix `0xc6591b9...`, and a profit of 0.3121 WMATIC, reported as $0.24 at execution time.

Read this as an extraction example. It does not, by itself, identify the earlier transaction that created the imbalance. The diagram displays equal stablecoin transfers and WMATIC amounts 5.3139 and 5.0018, whose difference is 0.3121; that subtraction is a guide-derived check of the displayed flows, not a separate accounting of fees.

**Source caution:** The diagram labels the stablecoin **BUSD**, while the caption describes **USDC** pool pairs. The guide leaves the token identity unresolved and does not turn the truncated transaction prefix into an invented full hash.

## Figure 2 - Simulation attribution as a pipeline

**Location:** Section 4.3.2, [PDF p. 6](https://arxiv.org/pdf/2604.27979v1#page=6).

The diagram connects three steps:

1. Keep preceding transactions that touch pools on the observed arbitrage route.
2. Search backward for an edge where replaying the arbitrage yields at most 5% of its observed profit, using up to 100 blocks of lookback in the Polygon setup.
3. Compute signed marginal profit changes in a backward pass and select the largest positive source contribution, with a nearest-to-arbitrage tie break.

The threshold identifies a search boundary. It is not a finding that every opportunity is exactly 95% created by one transaction. The figure is best read alongside the surrounding prose and Algorithm 1; their edge-return and marginal-index conventions require clarification before code is written. Negative impacts elsewhere in the paper also show why the monotonicity needed for a binary search should not be assumed without verification.

## Figure 3 - Positive creation and negative consumption

**Location:** Sections 5.2-5.3, [PDF p. 8](https://arxiv.org/pdf/2604.27979v1#page=8).

The example concerns block 82,563,006. It shows a non-arbitrage transaction at index 129, related arbitrage transactions at indices 130 and 168, and a main arbitrage transaction at index 199. The main attribution highlighted in the caption is +32.58 MATIC for transaction 129. The prose gives negative contributions of approximately -12.50 and -2.75 MATIC for competing arbitrageurs.

The useful distinction is the sign: a transaction can contribute by expanding an opportunity, while a competing arbitrage can consume part of it. A graph with several nonzero values can still have one dominant positive creator. Read an edge's value with its destination; the drawing includes links to related arbitrages as well as the main one, so summing every number on the entire figure is not a single-event decomposition.

**Source caution:** Section 5.3 calls all four displayed transactions candidates while also including the executed target arbitrage itself. Section 3's candidate definition concerns preceding transactions. Treat the four displayed nodes as the event illustration's participants, rather than assume the target is a candidate source under the formal definition.

## Figure 4 - Monte Carlo Shapley convergence

**Location:** Section 5.3, [PDF p. 10](https://arxiv.org/pdf/2604.27979v1#page=10); interpretation on [p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).

Four panels plot estimated Shapley value against the number of sampled permutations for a transaction prefix `0xb1f2a5bb...` in block 82,554,874. The dashed line is an exact reference; plotted estimates and bands summarize the mean and one standard deviation over 100 runs. The panels include a strong positive contribution, negative contributions near zero, and an exactly zero contribution. The vertical axis is labeled in USD; the paper's internal attribution computations are in MATIC.

Section 5.3 describes 16 candidates with potentially nonzero values, meaning 2^16 = 65,536 subsets for exact enumeration. The authors report estimates stabilizing within 5% after about 500 samples in this example and choose 1,000 samples as their default.

**Interpretation caution:** This is a reported convergence illustration, not an independent convergence experiment or a uniform error guarantee for every event. Relative error is particularly hard to interpret at or extremely close to zero; the displayed bands convey absolute variation there. Sampling preserves the target Shapley definition only in expectation/as sampling converges, rather than making a finite sample numerically identical to exact enumeration.

## Figure 5 - A complex interaction graph can have a primary source

**Location:** Section 5.3, [PDF p. 10](https://arxiv.org/pdf/2604.27979v1#page=10); interpretation on [p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).

This wider graph shows transactions from block 82,554,874, described by the caption using transaction prefix `0xb1f2a5bb...`. The diagram's main arbitrage node is index 346; related arbitrages and non-arbitrage transactions connect through positive and negative Shapley values. Section 5.3 describes a 17-candidate structure and says one transaction still dominates.

It illustrates why candidate count and primary-source count are different concepts: many transactions can interact with a route while one receives the largest positive attribution. It does not establish that the remaining transactions have zero effect.

**Source caution:** Figure 4's prose refers to 16 potentially nonzero candidates, while Figure 5 refers to 17 candidates/transactions. The guide reports the labels without assuming identical inclusion rules. The figure provides shortened hashes rather than full event identifiers, which limits an independent chain lookup from the figure alone.

## Figure 6 - Cumulative concentration

**Location:** Section 5.5, [PDF p. 10](https://arxiv.org/pdf/2604.27979v1#page=10); discussion starts on [p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).

The chart sorts high-value arbitrage transactions and opportunity-creating transactions and plots cumulative MEV volume against the top percentage of transactions. Both curves approach approximately 80% of value around the top 1%, according to the caption. The text also gives an approximately 1.6:1 ratio of **successfully executed** arbitrage transactions to opportunity-creating transactions. This does not count all submitted bids, reverted attempts, mempool competition, or unique searchers.

**Source cautions:**

- The x-axis refers to transactions. The surrounding text calls the blue population "arbitrageurs" and discusses address-level concentration. A transaction-ranked chart does not by itself prove a unique-address concentration statistic.
- The chart legend says 360,026 arbitrage transactions and **220,264** opportunity transactions. The caption and surrounding prose use **220,262** opportunity transactions.
- The caption associates those opportunities with **February**, while Section 5.1 gives only 2,526 February comparison events and Section 5.5 opens by describing the 360,026-event **March** analysis. No detailed mapping reconciles the event and opportunity populations. Do not silently relabel the figure as March or derive a precise dataset-level ratio from the inconsistent counts.
- This is transaction concentration, distinct from the conclusion's top-5%-of-protocols/73%-of-value claim. The latter is a separate reported statement, not a value read from this graph.

## Table 1 - Method design trade-offs

**Location:** Section 4.2, [PDF p. 6](https://arxiv.org/pdf/2604.27979v1#page=6).

The table compares data needs, stated complexity, candidate-set scale, and intended role. It recommends bot data for validation, coefficient attribution for screening, simulation for primary attribution, exact Shapley for small-set reference calculations, and Monte Carlo Shapley for approximate reference calculations.

| Method | What the table is conveying | Qualification when using it |
| --- | --- | --- |
| Bot data | A cheap lookup/inference stage after loading, requiring bids and route predictions; limited by bot coverage | Model training, ingestion, and observing the relevant event are outside a constant-time attribution label. |
| Coefficient | Very cheap reserve/price-based scoring; labeled O(1) | Algorithm 2 loops through candidates. O(1) is at most a possible per-candidate/fixed-route interpretation; the table does not establish O(1) total event cost. |
| Simulation | O(log \|C\| + m) search and scan, requiring historical execution | Replay cost, state access, and conditions for a valid binary search also matter; m is the edge-to-arbitrage range size. |
| Exact Shapley | Exponential enumeration, O(2^\|C\|), intended for \|C\| < 20 | These are high-level enumeration counts, not complete costs of evaluating every coalition. |
| Monte Carlo Shapley | O(N \|C\|), where N is sampled permutations | Each marginal value still requires a defined coalition evaluation; sampling uncertainty and infrastructure cost remain. |

The table's candidate-size suggestions are reported operating ranges, not mathematical correctness boundaries or measured limits reproduced here.

## Table 2 - Reported method comparison

**Location:** Section 5.4, [PDF p. 9](https://arxiv.org/pdf/2604.27979v1#page=9). The sample is the **2,526 February events**.

The authors report 94.2% bot accuracy at 38.4% coverage, 91.7% simulation accuracy at 99.1% coverage, and a coefficient score of 77.2% at 88.4% coverage. They report mean times of 8 ms, 12.3 ms, and 0.8 ms per event respectively; exact Shapley is approximately 5 minutes and Monte Carlo Shapley with 1,000 samples is 2.1 seconds. The two Shapley rows each show 100% accuracy and 98.1% coverage.

**Source cautions:** Section 5.2 says exact Shapley coverage is 12.0% and Monte Carlo coverage is 100%, which does not agree with the table. Section 5.4 describes the coefficient's 77.2% as agreement with simulation, although the caption describes accuracy against triangulated ground truth or exact Shapley. Treat the ground-truth/reference labels and denominators as requiring clarification. The Shapley rows' 100% scores are within the authors' reference scheme; they do not demonstrate independently known real-world causation or zero finite-sample error.

Section 5.4 also reports 80 hours to process the March dataset and says this is consistent with 12.3 ms/event. A guide-derived multiplication, 360,026 x 0.0123 seconds, yields approximately 4,428 seconds (74 minutes). A different end-to-end scope may be involved, but it is not documented sufficiently to reconcile the statement.

## Algorithms 1-3 - What they specify, and what they leave open

| Item | Location | Intended computation | Before treating it as executable logic |
| --- | --- | --- | --- |
| Algorithm 1: Simulation-Based Attribution | [p. 6](https://arxiv.org/pdf/2604.27979v1#page=6) | Filter; find a low-profit boundary; compare successive replay profits; return the largest positive-impact source | Clarify the threshold search direction and the line-15 `None` return, which appears to reject the low-profit condition being searched for; initialize the profit at the upper boundary and settle the impact index. Verify monotonicity or use a search that handles reversals. |
| Algorithm 2: Coefficient-Based Attribution (K-Value Method) | [p. 7](https://arxiv.org/pdf/2604.27979v1#page=7) | Apply candidate reserve changes in chronological order; compare route coefficients; choose the largest increase with a most-recent tie break | Define coefficient construction for each AMM, route direction, pre-candidate state, and transaction dependencies; account for the loop when discussing total complexity. A price multiplier is not a realized finite-trade profit. |
| Algorithm 3: Shapley-Based Attribution (Monte Carlo Approximation) | [p. 7](https://arxiv.org/pdf/2604.27979v1#page=7) | Sample candidate permutations, accumulate coalition marginal values, average them, and choose the maximum | Specify how a coalition is replayed, which order it uses, what happens on failure, and how the base value is treated. A sampled permutation used to average marginal contributions does not automatically establish a valid EVM execution order. |

The algorithms are descriptions in the paper. This repository does not validate them, repair them into an implementation, or claim their reported experimental results as its own.

Continue with the [reading map](01-reading-map.md) or [glossary](07-glossary.md).
