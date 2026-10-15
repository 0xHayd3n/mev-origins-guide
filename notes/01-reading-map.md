# Reading map

This guide follows **arXiv:2604.27979v1, submitted April 30, 2026**, by Andrei Seoev, Dmitry Belousov, Anastasiia Smirnova, Ksenia Kurinova, Aleksei Smirnov, Denis Fedyanin, and Yury Yanovich. Use the [version-pinned paper](https://arxiv.org/abs/2604.27979v1) and [14-page PDF](https://arxiv.org/pdf/2604.27979v1). Page numbers below are PDF page numbers, which match the paper's printed numbering.

These are explanatory reading notes. The measurements, system implementation, and experiments described here are the authors' reports; this repository does not reproduce them.

## The question to carry through the paper

Start with an **observed, profitable atomic arbitrage transaction**. Which earlier transaction changed the relevant pool states enough to make that extraction possible, and how should its contribution be measured?

The paper changes the unit of attention from the transaction that **takes** an opportunity to the transaction that **creates or enlarges** it. A swap can create an imbalance; a later arbitrage can consume it. Both may have attribution values, including negative ones. The primary source is the largest contributor under a chosen method, not necessarily the only transaction that matters. [Sections 2.3-3.3, pp. 3-4](https://arxiv.org/pdf/2604.27979v1#page=3).

## Choose a reading route

| Reader's goal | Suggested route | What to check before drawing conclusions |
| --- | --- | --- |
| Understand the main idea | Abstract and sections 1-3, then sections 5.3 and 8 | The scope is atomic arbitrage on Polygon, and the 96.7% claim concerns a dominant positive contributor in the February sample. |
| Understand how attribution works | Sections 3-4, Figure 2, Algorithms 1-3 | Fix the profit function, initial state, candidate set, route, ordering, and transaction failure policy. The paper's pseudocode is not a validated implementation. |
| Evaluate the evidence | Sections 5.1-5.6, Tables 1-2, Figures 3-6 | Separate February method comparison from March scale analysis; inspect the unresolved numerical and denominator issues. |
| Plan an independent reproduction | Sections 3.2, 4.3, 5.1-5.2, and 6 | An archive state/replay engine, event detector, metadata, and explicit counterfactual semantics are prerequisites; proprietary bot logs are unavailable from this guide. |
| Use this guide as an agent | Read [AGENTS.md](../AGENTS.md), then this page and [the figure/table inventory](06-figures-and-tables.md) | Preserve version and page citations, reported-vs-derived labels, and the paper's inconsistencies. |

## Section-by-section map

| Paper location | PDF pages | What it contributes | Reading question |
| --- | --- | --- | --- |
| Abstract | 1 | Frames transaction-level opportunity attribution and introduces four methods. | Is the claim about opportunity creation or extraction? |
| 1. Introduction | 1-2 | Motivates the supply side of MEV, states the single-source hypothesis, and lists formalization, methods, system, and empirical contributions. | Does a headline "single source" mean exclusive causation or primary contribution? Section 5.3 makes the empirical criterion more specific. |
| 2. Background and Scope | 2-3 | Establishes the execution model, eligible events, and core vocabulary. | What is held fixed when evaluating a counterfactual? |
| 2.1. Blockchain as a Deterministic State Machine | 2 | Explains why an ordered EVM transaction sequence can be replayed, and discusses other execution architectures conceptually. | Deterministic execution helps evaluate a specified intervention; has the intervention itself been specified completely? |
| 2.2. Atomic Arbitrage: Definition and Rationale | 2-3 | Requires at least two swaps, non-negative net changes for all involved assets, and strictly positive profit after fees and priority bids; Figure 1 is the example. | Are token accounting, fee treatment, and route execution consistent? |
| 2.3. Core Definitions | 3 | Distinguishes extraction, opportunity, and state delta; explains amplification of an existing opportunity. | Does the source create a new profitable state or merely increase existing profit? |
| 3. Problem Formulation | 4 | Defines the attribution task, inputs, outputs, and scope. | Are all contributions, including a pre-existing base, accounted for? |
| 3.1. Goal: Attribute MEV Opportunity to a Source Transaction | 4 | Seeks the preceding transaction or set of transactions responsible for an observed profit. | Is identifying a primary source enough for the downstream use? |
| 3.2. System Model and Inputs | 4 | Models ordered state transitions and a lookback of up to 100 earlier blocks; requires historical state, transaction traces, and the observed MEV event. | What initial state and historical window are being used? |
| 3.3. Desired Outputs and Scope | 4 | Defines candidate transactions touching route pools, a base-profit-plus-contributions decomposition, source IDs, values, and sender/protocol aggregation. | Which relevant effects might the pool-intersection filter exclude? |
| 4. Attribution Methodology | 4-7 | Gives an offline pipeline and four methods. | Which method answers the desired question at acceptable cost? |
| 4.1. Overview and Pipeline | 4 | Detect arbitrage, collect prior pool-interacting candidates, attribute value, and aggregate. | How do candidate collection and metadata influence the final distribution? |
| 4.2. Method Summary and Trade-offs | 4-5 | Separates live bot intentions from retrospective analysis; recommends coefficient screening, simulation for primary attribution, and Shapley for difficult cases. | Does a prediction agree with the eventual finalized execution? |
| 4.3.1. Bot Data-Based Attribution | 5 | Uses production searcher bids and predicted routes as an external validation signal; describes a GNN/MLP agent trained with PPO. | Which opportunities were visible to the bots, and how independent is the signal? |
| 4.3.2. Simulation-Based Attribution | 5-6 | Filters candidates, searches backward for a 5%-profit edge, scans marginal impacts, and picks the largest positive one; Figure 2 and Algorithm 1. | Is profit monotone enough for binary search, and are the edge/return and marginal-index conventions clear? |
| 4.3.3. Coefficient-Based Attribution | 6-7 | Tracks the largest increase in an infinitesimal route price multiplier, also called the K-value method; Algorithm 2. | Does a marginal price proxy reflect finite trade size, liquidity depth, slippage, and fees? |
| 4.3.4. Shapley-Based Attribution | 7 | Allocates a coalition's value through average marginal contributions; exact enumeration for small candidate sets and Monte Carlo sampling for larger ones; Algorithm 3. | How are selected transactions ordered and dependent or reverted transactions handled? |
| 5. Evaluation | 7-11 | Reports datasets, validation, examples, performance, concentration, and limitations. | Which sample, unit, and validation denominator support each statistic? |
| 5.1. Experimental Setup | 7-8 | Defines the March scale dataset and February comparison window, archive-node setup, and hardware. | Keep the 360,026 March events separate from 2,526 February events. |
| 5.2. Ground Truth and Validation Strategy | 8 | Triangulates bot consensus, Shapley attribution, and expert review of 200 stratified events. | The validation sources are benchmarks with potential shared errors; the reported Shapley coverage differs from Table 2. |
| 5.3. Shapley Attribution: Examples and Convergence | 8-9 | Explains signed contributions, dominant vs. tied sources, a sampled convergence example, and a complex interaction graph; Figures 3-5. | Does the evidence demonstrate dominance, exact exclusivity, or agreement within one model? |
| 5.4. Method Comparison: Accuracy, Performance, and Cost | 9 | Compares accuracy/agreement, coverage, and mean time in Table 2, and recommends the hybrid workflow. | The 77.2% coefficient result is described as agreement with simulation, while Table 2 uses a broader accuracy heading. |
| 5.5. MEV Creation by Protocol | 9-10 | Reports AMM participation, concentration, and an approximately 1.6 executed-arbitrage-to-opportunity ratio; Figure 6. | Are protocol participation, transaction concentration, addresses, opportunity counts, and value shares being distinguished? |
| 5.6. Limitations | 10-11 | Acknowledges triangulated truth, one-chain/time-window limits, and the exclusion of other MEV categories. | What would change on another chain or for another form of MEV? |
| 6. System Implementation | 11 | Describes modular Rust/C++ components and Python analysis wrappers, containerization, and proprietary bot logs; promises non-proprietary artifacts upon publication. | A stated future release is not an available artifact or a reproduction performed by this guide. |
| 7. Related Work | 11-12 | Positions the paper relative to MEV measurement, ordering analysis, root-cause attribution, Shapley methods, and systems research. | Which comparison is directly about MEV attribution, and which is a methodological analogy? |
| 7.1. MEV Measurement and Quantification | 11 | Connects the work to MEV measurement and the adopted atomic-arbitrage detector. | Opportunity attribution depends on upstream detection choices. |
| 7.2. Counterfactual Analysis and Transaction Ordering | 11 | Distinguishes aggregate ordering effects and source scanning from contribution attribution. | Does a method locate a trigger or allocate value? |
| 7.3. Attribution, Root-Cause Analysis, and Shapley Value in Systems | 11 | Draws connections to CIRCA, CF-Shapley, and ShapleyIQ. | Does the analogy justify the particular blockchain coalition semantics? |
| 7.4. Methodological Parallels in Systems Research | 11-12 | Discusses fault injection, simulation, adaptive validation, fair allocation, and consensus. | These are conceptual parallels, not experimental evidence for this paper's metrics. |
| 7.5. Identified Gap: Transaction-Level Attribution of MEV Creation | 12 | Restates the claimed gap between extraction measurement and causal attribution. | Can exact execution of a chosen counterfactual be separated from the validity of the causal interpretation? |
| 8. Conclusion | 12 | Repeats the main empirical and practical claims and proposes real-time, broader-MEV, and multi-chain extensions. | Check the conclusion's headline claims against the detailed evidence and caveats. |
| 9. Ethics Statement | 12 | Discusses public blockchain analysis and the dual use of attribution insights. | The repository remains a retrospective reading guide. |
| References [1]-[33] | 13-14 | Lists the cited literature. | Consult original sources before treating a citation's characterization as independently verified. |

All locations in the map refer to the [pinned v1 PDF](https://arxiv.org/pdf/2604.27979v1), especially [methods, pp. 4-7](https://arxiv.org/pdf/2604.27979v1#page=4), [evaluation, pp. 8-10](https://arxiv.org/pdf/2604.27979v1#page=8), and [implementation/conclusion, pp. 11-12](https://arxiv.org/pdf/2604.27979v1#page=11).

## A compact mental model

An earlier swap changes a pool's reserves. That may create a profitable cyclic trade, or increase the profitability of a route that already existed. Other transactions can add to or consume that opportunity before the observed arbitrage executes. Attribution measures contributions relative to an initial state and a chosen profit model. The base profit belongs in the accounting even when no source inside the lookback window can be identified. [Sections 2.3-3.3, pp. 3-4](https://arxiv.org/pdf/2604.27979v1#page=3).

For a purely illustrative example, suppose a fixed route has profit 2 before the candidate window, 12 after transaction A, and 9 after transaction B. The chronological profit changes are +10 for A and -3 for B, with 2 pre-existing. This arithmetic is an explanation of signed changes, not paper data and not a Shapley calculation. Shapley would average each candidate's marginal effect across specified coalitions, which can differ from its chronological change.

## Keep these cautions beside the paper

- **Dominance is not exclusivity.** Section 5.3 reports that 96.7% of February events have one transaction contributing more than 70% of total positive Shapley value. This permits smaller positive and negative contributions from others. [pp. 8-9](https://arxiv.org/pdf/2604.27979v1#page=8).
- **The two datasets have different roles.** The March scale analysis reports 1,050,000 blocks, 360,026 arbitrage events, and $334,799 extracted value. The February comparison reports 2,526 events. Section 5.5 and Figure 6 nevertheless attach a 220,262 opportunity-transaction count to February; do not silently assign that count to March. [Sections 5.1 and 5.5, pp. 8-10](https://arxiv.org/pdf/2604.27979v1#page=8).
- **Shapley coverage is internally inconsistent.** Section 5.2 reports 12.0% exact and 100% Monte Carlo coverage; Table 2 reports 98.1% for both. Its additional categories do not reconcile those statements. [Section 5.2, p. 8](https://arxiv.org/pdf/2604.27979v1#page=8); [Table 2, p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).
- **The runtime scope needs clarification.** The paper reports 12.3 ms per simulation event and approximately 80 hours for 360,026 March events. Multiplying those event counts and means gives about 74 minutes, a guide-derived arithmetic check. Additional pipeline or infrastructure costs might explain a different total, but the paper does not provide a reconciliation. [Section 5.4, p. 9](https://arxiv.org/pdf/2604.27979v1#page=9).
- **Some examples have labeling or counting issues.** Figure 1's diagram says BUSD where the caption says USDC. Figure 6's legend gives 220,264 opportunity transactions where its caption says 220,262. Section 5.3's 83 tied-source events include 42 in one subtype and a stated "remaining 33," leaving eight unexplained by that split. [Figure 1, p. 3](https://arxiv.org/pdf/2604.27979v1#page=3); [Section 5.3, p. 8](https://arxiv.org/pdf/2604.27979v1#page=8); [Figure 6, p. 10](https://arxiv.org/pdf/2604.27979v1#page=10).
- **Determinism does not remove modeling choices.** Coalition ordering, transaction dependencies, failure handling, search thresholds, and whether the route is held fixed affect the attribution question. Treat the paper's algorithms as descriptions requiring clarification before implementation. [Sections 3-4, pp. 4-7](https://arxiv.org/pdf/2604.27979v1#page=4).

For a visual inventory, continue with [Figures, tables, and algorithms](06-figures-and-tables.md). For terminology and symbols, use the [glossary](07-glossary.md).
