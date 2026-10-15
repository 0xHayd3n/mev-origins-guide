# Glossary and notation

Definitions below explain the vocabulary of [Seoev et al., arXiv:2604.27979v1](https://arxiv.org/abs/2604.27979v1). They describe the paper's model and reported study, not an implementation supplied by this guide. Pinned PDF pages identify where each concept enters the paper.

## Core terms

| Term | Meaning in this guide | Paper location and caution |
| --- | --- | --- |
| **MEV (Maximal Extractable Value)** | Value available through strategically choosing transaction inclusion or ordering. In the empirical study, the observed extraction event is a profitable atomic arbitrage transaction. | [Sections 1-2.3, pp. 1-3](https://arxiv.org/pdf/2604.27979v1#page=1). The paper does not empirically cover every MEV category. |
| **Opportunity** | A state in which an executable arbitrage route can earn positive profit under the selected accounting model. | [Section 2.3, p. 3](https://arxiv.org/pdf/2604.27979v1#page=3). An opportunity is a state condition, not the transaction that later extracts it. |
| **Opportunity creation** | A transaction changes state so that a profitable route emerges. | [Sections 2.3-3.1, pp. 3-4](https://arxiv.org/pdf/2604.27979v1#page=3). The paper sometimes uses creation broadly for positive contributions, including amplification. |
| **Opportunity amplification** | A state change increases the available profit of a route that was already profitable. | [Section 2.3, p. 3](https://arxiv.org/pdf/2604.27979v1#page=3). It need not be the original trigger. |
| **Extraction** | The transaction executes a profitable strategy and captures some available value. | [Section 2.3, p. 3](https://arxiv.org/pdf/2604.27979v1#page=3). Extractor and creator are different roles, even if transactions or actors can play both roles across events. |
| **Atomic arbitrage** | One all-or-nothing transaction with at least two swaps, non-negative net changes in every involved asset, and strictly positive profit after transaction fees and priority bids. | [Section 2.2, pp. 2-3](https://arxiv.org/pdf/2604.27979v1#page=2). Atomicity concerns execution of the transaction; it does not guarantee inclusion or freedom from every operational cost. |
| **Arbitrage route** | The ordered pool-swap path used to trade through a price discrepancy. | [Sections 3-4, pp. 4-7](https://arxiv.org/pdf/2604.27979v1#page=4). Retrospective evaluation of the observed route differs from searching for a new optimum in each counterfactual. |
| **State** | Account balances, smart-contract storage, pool reserves, and other execution data at a given point in the canonical transaction sequence. | [Sections 2.1 and 3.2, pp. 2 and 4](https://arxiv.org/pdf/2604.27979v1#page=2). Exact execution requires an adequately specified historical environment. |
| **State delta / perturbation** | The change caused by executing a transaction; pool reserve and price changes are central here. | [Section 2.3, p. 3](https://arxiv.org/pdf/2604.27979v1#page=3). Different attribution methods approximate or replay these changes differently. |
| **Candidate source** | A preceding transaction in the search window that interacts with at least one pool on the observed arbitrage route. | [Sections 3.2-4.1, p. 4](https://arxiv.org/pdf/2604.27979v1#page=4). A candidate can have positive, zero, or negative contribution; membership alone is not attribution. |
| **Primary source** | The transaction receiving the largest relevant contribution score under a method. | [Sections 3.3 and 4.3, pp. 4-7](https://arxiv.org/pdf/2604.27979v1#page=4). It need not be the sole contributor, and different methods can disagree. |
| **Single-source hypothesis** | The authors' hypothesis that competitive searchers tend to extract quickly, so one prior transaction will usually dominate opportunity creation. | [Sections 1 and 5.3, pp. 2 and 8-9](https://arxiv.org/pdf/2604.27979v1#page=8). The reported 96.7% criterion is one transaction contributing over 70% of total **positive** Shapley value, not all others having zero contribution. |
| **Multi-source / tied-source case** | An event with tied maximum Shapley values in the authors' reported classification. | [Section 5.3, p. 8](https://arxiv.org/pdf/2604.27979v1#page=8). This operational classification is narrower than every conceivable case with several material contributors. |
| **Pre-existing opportunity / base component** | Profit already available in the chosen initial state, before candidate contributions are added. | [Sections 3.3 and 4.3.4, pp. 4 and 7](https://arxiv.org/pdf/2604.27979v1#page=4). It is not proof that no earlier source exists outside the window. The paper also uses S0 when discussing no in-window source. |
| **Lookback window** | The historical interval in which sources are sought, up to 100 earlier blocks in the reported Polygon setup. | [Sections 3.2 and 4.3.2, pp. 4-5](https://arxiv.org/pdf/2604.27979v1#page=5). This is a chosen bound, not a universal causal horizon. |
| **Edge transaction** | The simulation method's boundary near which replayed arbitrage profit falls to at most 5% of observed profit when searching backward. | [Section 4.3.2, pp. 5-6](https://arxiv.org/pdf/2604.27979v1#page=5). It is a threshold/search device; Algorithm 1's details need clarification. |
| **Counterfactual replay** | Evaluate a specified alternate historical state or transaction sequence to ask how the observed arbitrage's profit would change. | [Sections 2.1 and 4.3.2, pp. 2 and 5-6](https://arxiv.org/pdf/2604.27979v1#page=5). Determinism does not define the intervention, dependency policy, or execution order for you. |
| **Marginal impact** | A difference between profit or coefficient values with and without a candidate's incremental effect under a stated ordering/model. | [Sections 4.3.2-4.3.4, pp. 5-7](https://arxiv.org/pdf/2604.27979v1#page=5). A chronological marginal and a Shapley average marginal are different quantities. |
| **Negative contribution** | A candidate reduces the profit allocated to the target event in the model, for example by consuming a price discrepancy. | [Figure 3 and Section 5.3, p. 8](https://arxiv.org/pdf/2604.27979v1#page=8). Negative attribution is not a statement that the transaction was malicious or socially harmful. |
| **Bot-data attribution** | Use searcher bids and predicted routes as evidence of which pending transaction was expected to create an opportunity. | [Section 4.3.1, p. 5](https://arxiv.org/pdf/2604.27979v1#page=5). This is intent/prediction data, with limited visibility and proprietary logs. |
| **Coefficient / K-value method** | Score the increase in a route's marginal price multiplier from reserve/price data. | [Section 4.3.3, pp. 6-7](https://arxiv.org/pdf/2604.27979v1#page=6). Lowercase k is a route-price proxy, not a finite-volume profit or the constant-product AMM invariant. |
| **Shapley value** | A cooperative-game allocation averaging a player's marginal value over coalitions/permutation positions. Here the players are candidate transactions and value is modeled arbitrage profit. | [Section 4.3.4, p. 7](https://arxiv.org/pdf/2604.27979v1#page=7). Fairness applies to the specified value function; it does not make that function a uniquely correct causal model. |
| **Coalition** | A subset of candidate transactions used in a Shapley value evaluation. | [Section 4.3.4 and Algorithm 3, p. 7](https://arxiv.org/pdf/2604.27979v1#page=7). Selected transactions still need a defined execution order and a policy for dependent or reverted transactions. |
| **Exact Shapley** | Enumerate coalition values rather than estimate the allocation through finite sampling. | [Sections 4.3.4 and 5.2, pp. 7-8](https://arxiv.org/pdf/2604.27979v1#page=7). "Exact" refers to the chosen game, not independently established causal truth. Coverage claims differ between Section 5.2 and Table 2. |
| **Monte Carlo Shapley** | Estimate Shapley values from sampled candidate permutations; the paper uses 1,000 samples by default. | [Algorithm 3 and Figure 4, pp. 7 and 10](https://arxiv.org/pdf/2604.27979v1#page=7). Finite sampling entails error; one convergence illustration is not a universal bound. |
| **Ground truth / triangulated benchmark** | The paper's reference combining bot evidence, Shapley computations, and manual review. | [Section 5.2, p. 8](https://arxiv.org/pdf/2604.27979v1#page=8). Direct causal truth is not observed; sources may share biases. |
| **Accuracy** | The authors' reported agreement with a chosen validation reference. | [Sections 5.2 and 5.4, pp. 8-9](https://arxiv.org/pdf/2604.27979v1#page=9). The coefficient result is described as agreement with simulation; table/reference wording is not fully consistent. |
| **Coverage** | Fraction of events for which a method returns an attribution considered valid by the study. | [Table 2, p. 9](https://arxiv.org/pdf/2604.27979v1#page=9). It is separate from accuracy, and the paper's Shapley coverage figures conflict. |
| **Protocol participation** | Frequency with which attributed opportunity transactions involve a named protocol. | [Section 5.5, p. 9](https://arxiv.org/pdf/2604.27979v1#page=9). A transaction can touch several protocols, so percentages can exceed 100% in total. It is not automatically value share or causal blame. |
| **Concentration** | Uneven distribution of attributed value across ranked units. | [Section 5.5 and Figure 6, pp. 9-10](https://arxiv.org/pdf/2604.27979v1#page=10). Preserve the unit: transaction, unique sender/address, protocol, event count, and value are not interchangeable. |

## Infrastructure and market vocabulary

| Term | Meaning here |
| --- | --- |
| **AMM** | Automated market maker: a liquidity-pool mechanism that prices trades from its state. Section 5.5 discusses multiple designs; their participation percentages overlap. |
| **Concentrated liquidity** | Liquidity supplied over selected price ranges rather than uniformly across the whole price domain. The paper reports frequent participation by such AMMs; it does not isolate the design's causal effect from all confounders. |
| **DEX** | Decentralized exchange; its pools are the venues whose price discrepancies support the studied routes. |
| **EVM** | Ethereum Virtual Machine, the execution environment underlying the sequential state model used for Polygon here. |
| **Archive node** | Historical blockchain-state infrastructure needed to recover old states and perform replay. The paper reports a modified Geth archive-node setup. |
| **Transaction trace** | Execution information, including calls/logs, used to reconstruct route interactions and protocol metadata. |
| **Mempool** | The pending-transaction view available to a searcher before finalized execution. Visibility limits bot-data coverage. |
| **Searcher / arbitrageur** | An actor seeking executable opportunities and submitting extraction transactions. A transaction-ranked chart is not automatically a ranking of unique such actors. |
| **Priority bid** | Payment or bidding expense included in the paper's profitability accounting alongside transaction fees. |
| **Slippage** | Difference between a marginal quoted exchange rate and the effective rate of a finite trade as reserves/liquidity change. The K-value proxy omits this finite-size effect. |
| **GNN / MLP / PPO** | Graph neural network / multilayer perceptron / proximal policy optimization, the model architecture and training terms described for the proprietary bot-data signal. |
| **MATIC / WMATIC** | The paper's internal profit unit and the wrapped token appearing in examples. Preserve the paper's historical labels when reporting its values. |

Sources: [scope and state model, pp. 2-4](https://arxiv.org/pdf/2604.27979v1#page=2); [method vocabulary, pp. 5-7](https://arxiv.org/pdf/2604.27979v1#page=5); [evaluation and infrastructure, pp. 8-11](https://arxiv.org/pdf/2604.27979v1#page=8).

## Symbols to keep straight

| Symbol | Meaning | Reading note |
| --- | --- | --- |
| B | A block, modeled as an ordered transaction sequence | State can persist across blocks, so an event's source need not be in the same block. |
| T_i | A transaction at a canonical position | Candidate identity and counterfactual order must remain explicit. |
| T_arb | The observed arbitrage/extraction transaction | The formal source candidates precede it. A figure may display it alongside candidates for context. |
| T_src | Primary attributed source transaction | Method-dependent output, not a declaration of exclusive contribution. |
| T_edge | Simulation search boundary | A boundary is not automatically the largest-impact source. |
| S_i | State after transaction i | Distinguish the state before versus after a transaction when computing differences. |
| S_0 | Initial state/base used for attribution | The paper uses it both in block-state formalization and no-in-window-source discussion; record its actual time/window in a reproduction. |
| Sigma(S, T) | Deterministic state-transition function | Deterministic once state, transaction, and execution environment are specified. |
| C | Candidate transaction set | Vertical bars, \|C\|, mean its size. |
| D | Lookback depth in blocks | D = 100 in the reported Polygon setup. |
| M(S, T_arb) | Profit of executing the observed arbitrage transaction in state S | The formal model names a fixed observed transaction, not an automatically reoptimized route. |
| Pi | Observed profit, or the shorter profit-function notation used in the methods | Check whether Pi denotes a number or a function at that point. |
| phi_base | Profit available in the initial state | Keep this base separate from newly attributed value. |
| phi_i | Attributed value for candidate i; computed through the cooperative game in the Shapley method | Section 3 seeks sum of candidate contributions plus base = observed profit; positive, zero, and negative contributions are possible. |
| Imp_i | Simulation's marginal profit-change score | The prose and Algorithm 1 leave indexing conventions unclear; do not silently shift the attributed transaction. |
| k(S) | Marginal route-price multiplier in state S | k > 1 indicates potential profitability before finite-size slippage and fees in this proxy. |
| Delta k_i | Change in k associated with a candidate | The coefficient method selects the largest increase. |
| V(S) | Shapley coalition value, with S now a **subset of candidates** | This S is not the blockchain state S_i. It must map the subset into a replay/profit evaluation. |
| N | Monte Carlo permutation count in Table 1/Algorithm 3 | Section 2.2 also uses N for number of swaps. These meanings are separate. |
| m | Number of transactions in simulation's edge-to-arbitrage interval | Appears in Table 1's O(log \|C\| + m) expression. |

Notation sources: [Section 3, p. 4](https://arxiv.org/pdf/2604.27979v1#page=4), [Table 1/Algorithm 1, p. 6](https://arxiv.org/pdf/2604.27979v1#page=6), and [Algorithms 2-3/Shapley definition, p. 7](https://arxiv.org/pdf/2604.27979v1#page=7). ASCII names above render the paper's mathematical symbols in a searchable form.

## Three distinctions that prevent common misreadings

**A dominant source can coexist with other contributors.** A toy allocation with positive contributions 80 and 20 has one source above 70% of positive value, but two positive contributors. Adding a -10 consumer changes net value while leaving the positive-value share 80%. This is an explanatory example, not paper data.

**A correct execution can answer an incompletely specified causal question.** Replaying a fully specified transaction sequence deterministically gives a reproducible result. Deciding which transactions to remove, whether remaining transactions revert, whether to preserve canonical order, and whether to hold the arbitrage route fixed still determines what that result means.

**An attribution score is not a reimbursement rule.** Shapley fairness refers to axioms of a specified cooperative game. The study does not establish that every attributed amount is an enforceable loss, a user's avoidable cost, or a proposed payment to an opportunity creator.

Return to the [reading map](01-reading-map.md) or inspect [figures, tables, and algorithms](06-figures-and-tables.md).
