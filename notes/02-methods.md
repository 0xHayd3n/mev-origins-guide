# How the attribution methods work

Reading notes on [*The Origins of MEV: Systematic Attribution of Arbitrage Opportunity Creation at Scale*, arXiv:2604.27979v1](https://arxiv.org/abs/2604.27979v1), by Andrei Seoev, Dmitry Belousov, Anastasiia Smirnova, Ksenia Kurinova, Aleksei Smirnov, Denis Fedyanin, and Yury Yanovich. See the [README](../README.md) for the guide's scope and attribution. Page references below are PDF pages in v1. This guide explains the paper; it does not implement or reproduce its system.

## 1. What is being attributed?

The input is an **observed atomic arbitrage transaction**, not every theoretically possible opportunity on the chain. The question is which preceding transactions created or enlarged the pool imbalance that the observed transaction captured. The authors separate opportunity creation from extraction: a user swap can create an opportunity, while an arbitrageur's later transaction extracts it. Another arbitrageur may consume part of the available profit before the focal transaction executes. [Sections 2.2-2.3, PDF pp. 2-3](https://arxiv.org/pdf/2604.27979v1#page=2).

Their atomic-arbitrage identification rule requires:

1. At least two swaps.
2. A nonnegative net balance change for every involved asset.
3. Strictly positive profit after transaction fees and priority bids.

The paper expresses net profit as the sum of asset balance changes valued in a base currency, less fees and bids. It uses MATIC for internal calculations and execution-time oracle prices for reported USD totals. Consequently, on-chain balance accounting and USD valuation are distinct steps; the claim that replay is deterministic does not by itself specify an oracle or valuation convention. [Section 2.2, PDF p. 3; Section 5.1, PDF p. 8](https://arxiv.org/pdf/2604.27979v1#page=3).

This scope excludes liquidations, sandwich attacks, cross-chain execution, unextracted opportunities, and a claim to measure all MEV. A lending interaction can still be a *source transaction* for a later atomic arbitrage; that does not mean liquidation extraction was included in the detected event class. [Sections 3.3 and 5.5-5.6, PDF pp. 4 and 9-10](https://arxiv.org/pdf/2604.27979v1#page=4).

## 2. State, candidates, and an additive target

The authors model a block as an ordered sequence of transactions. Using their notation:

$$
S_j = \Sigma(S_{j-1}, T_j), \qquad
\Pi = \mathcal{M}(S_{k-1}, T_{arb}).
$$

Here, $S_j$ is the state after transaction $T_j$; $T_{arb}$ is the observed arbitrage at position $k$; and $\mathcal{M}$ evaluates its profit in a supplied state. Required inputs are an archive state, an ordered transaction trace with calldata/logs, and the observed arbitrage's execution path and profit. The search may extend up to $D=100$ earlier blocks. [Sections 3.2-3.3, PDF p. 4](https://arxiv.org/pdf/2604.27979v1#page=4).

Candidates $C$ are preceding transactions that interact with pools used by the observed arbitrage. The desired decomposition is:

$$
\phi_{base}=\mathcal{M}(S_0,T_{arb}), \qquad
\Pi=\phi_{base}+\sum_{T_i\in C}\phi_i.
$$

The baseline matters: profit already available in the starting state should not be credited to a newly considered transaction. The desired event output includes a primary source hash, attributed value, and sender/protocol metadata for aggregation. The additive formulation is a target for value attribution; a primary-source indicator alone, as used in the bot or coefficient methods, does not establish a complete additive allocation. [Section 3.3, PDF p. 4](https://arxiv.org/pdf/2604.27979v1#page=4).

**Guide interpretation:** pool intersection is a tractability filter, not a proof that all possible dependencies have been retained. Funding, approvals, contract deployment, oracle updates, and indirect state dependencies can affect execution without looking like a swap on a route pool. A reproduction must say whether such dependencies are preserved as background state, included as candidates, or deliberately excluded. It must also specify the initial-state anchor when the search crosses block boundaries; the block-level $S_0$ notation alone does not resolve that operational choice.

## 3. Bot-data attribution: evidence from searcher intent

The bot method uses a searcher's recorded decision that a candidate transaction would trigger an arbitrage route. A bid above a minimal threshold $\epsilon$, tied to a source transaction and predicted route, supplies a positive attribution indicator. This is evidence of what the searcher expected before execution. It can disagree with a finalized-block counterfactual without either record being fabricated. [Section 4.3.1, PDF p. 5](https://arxiv.org/pdf/2604.27979v1#page=5).

The described implementation uses a graph neural network over pool topology and reserves, followed by an MLP value head. It is trained with PPO on historical Polygon data; the stated reward is realized profit less gas and priority bids. The paper reports a design target below 10 ms per candidate and a measured bot-method mean of 8 ms/event. These descriptions do not supply model weights, complete training parameters, or the proprietary bidding logs. [Sections 4.3.1 and 5.4, PDF pp. 5 and 9](https://arxiv.org/pdf/2604.27979v1#page=5).

The authors use bot evidence as an external validation layer. Coverage is limited by their real-time visibility and bot design, including missing last-in-block arbitrage. Section 6 identifies the affiliated company's production searcher logs as proprietary and says this component cannot be released. The method should therefore be understood as a limited reference signal, not universal ground truth. [Sections 5.2 and 6, PDF pp. 8 and 11](https://arxiv.org/pdf/2604.27979v1#page=8).

## 4. Simulation attribution: find the largest local profit change

The intended procedure has three stages. [Section 4.3.2, PDF pp. 5-6; Algorithm 1 and Figure 2, PDF p. 6](https://arxiv.org/pdf/2604.27979v1#page=5).

1. **Filter:** retain preceding transactions that touch the arbitrage route's pools.
2. **Locate an edge:** search backward for a position where simulated profit has fallen to at most 5% of the observed profit. Search starts in the same block and can extend to 100 earlier blocks on Polygon. The paper reports that 99.3% of attributable opportunities had an edge within seven blocks in an analysis described as spanning two million blocks; that stated scope differs from the two principal evaluation windows.
3. **Inspect local changes:** traverse backward between the edge and the focal arbitrage, compute changes in hypothetical arbitrage profit, and choose the largest positive impact. The prose resolves equal maxima in favor of the transaction nearest to the arbitrage.

For intuition, define $P_j=\mathcal{M}(S_j,T_{arb})$, the focal arbitrage's hypothetical profit immediately after position $j$. Then $P_j-P_{j-1}$ describes the change associated with moving across transaction $T_j$ on the observed chronological path. This explanatory notation is **not a corrected implementation** of Algorithm 1. The paper instead prints an impact indexed as $\mathrm{Imp}_i=\Pi_{i+1}-\Pi_i$, while describing $\Pi_i$ as the profit after $T_i$; an implementer must resolve that indexing before assigning hashes.

This is a sequence of profit evaluations on historical prefixes. It should not be silently equated with separately deleting each candidate while retaining and replaying the entire later suffix. Those counterfactuals can differ when transactions interact. The paper's broader causal discussion mentions removal and reordering, but Algorithm 1 concretely evaluates prefixes followed by the focal arbitrage. [Sections 4.1 and 4.3.2, PDF pp. 4-6](https://arxiv.org/pdf/2604.27979v1#page=4).

### Read Algorithm 1 with care

The printed v1 procedure leaves material questions:

- **Threshold return condition:** line 15 returns `None` when profit at the selected edge is *below* 5%, although the prose describes finding a profit drop to at most 5% as the edge-search objective. The strict inequality also differs from the search's non-strict comparison. This guide does not guess the intended correction.
- **Search assumptions:** binary search requires a suitable boundary predicate. Profit need not change monotonically as preceding swaps create opportunities and competing arbitrage consumes them. The paper does not establish a monotonicity condition or document a fallback for multiple threshold crossings.
- **Indexing:** the after-transaction profit notation and the forward difference used as a transaction's impact do not clearly agree, including the terminal comparison near $T_{arb}$.
- **Starting state:** the handling of pre-existing profit, a failed search, and an edge across multiple blocks needs a precise common state anchor. The prose distinguishes pre-existing opportunities; the pseudocode alone does not settle every case.

These are specification limitations, not evidence that the reported implementation necessarily used the literal printed logic. No author implementation was executed for this guide.

## 5. Coefficient attribution: a quick price-direction proxy

The K-value method evaluates a route's infinitesimal price multiplier $k$ from pool reserves/prices. In the simplified setting without slippage or fees, $k>1$ suggests a potentially profitable cycle. The method scans candidates chronologically and selects the transaction with the largest positive change:

$$
\delta k_i=k(S_i)-k(S_{i-1}), \qquad
T_{src}=\arg\max_{T_i\in C}\delta k_i.
$$

Algorithm 2 favors the later transaction on a tie. Pool price information is obtained from logs or callbacks, avoiding full historical EVM replay. The tradeoff is substantial: this proxy omits liquidity depth, finite trade size, nonlinear slippage, and transaction fees. A large improvement in an infinitesimal exchange rate need not create the largest realizable net profit. [Section 4.3.3 and Algorithm 2, PDF pp. 6-7](https://arxiv.org/pdf/2604.27979v1#page=6).

**Cost qualification:** Table 1 labels coefficient complexity $O(1)$, but Algorithm 2 loops over $C$ and computes route coefficients at each step. The table does not explain whether $O(1)$ refers to a single candidate update with a fixed route. It should not be read as a demonstrated constant-time whole-event scan independent of candidate count or route length. Likewise, the protocol-specific reserve/price update rules are not fully specified by the abstract `compute_k` interface.

## 6. Shapley attribution: distribute interaction effects

Candidates become players in a cooperative game. $V(A)$ is the profit of the focal arbitrage after executing a coalition $A\subseteq C$. Each candidate receives its weighted average marginal contribution across coalitions:

$$
\phi_i=\sum_{A\subseteq C\setminus\{T_i\}}
\frac{|A|!(|C|-|A|-1)!}{|C|!}
\left[V(A\cup\{T_i\})-V(A)\right].
$$

Unlike selecting a single local maximum, this allocation can share value among interdependent transactions. Negative values are meaningful: a competing arbitrage may remove profit that the focal event could otherwise have captured. The authors use the largest Shapley value to select a primary source while retaining the full contribution vector. [Section 4.3.4 and Algorithm 3, PDF p. 7; Figure 3, PDF p. 8](https://arxiv.org/pdf/2604.27979v1#page=7).

Exact evaluation is exponential. The paper uses exact enumeration for $|C|<20$ and Monte Carlo permutation sampling for larger sets. In Algorithm 3, each sampled permutation determines the order in which candidates **enter the coalition for accounting**; the algorithm accumulates $V(A\cup\{T_i\})-V(A)$ and averages over $N$ samples. That accounting order is not automatically an instruction to reorder EVM transaction execution. Defining the execution of each coalition remains a separate requirement.

For a fixed, well-defined deterministic value function, exact Shapley values sum to $V(C)-V(\varnothing)$; adding the baseline recovers $V(C)$. This mathematical property does not make the chosen candidate set, replay semantics, or profit function empirically correct. It also does not make a finite Monte Carlo estimate exact. The authors report stabilization within 5% after about 500 samples for their illustrated event and choose 1,000 samples. The example is useful evidence of convergence on that case, not a universal relative-error guarantee, particularly for values close to zero. [Section 5.3 and Figure 4, PDF pp. 9-10](https://arxiv.org/pdf/2604.27979v1#page=9).

### Coalition semantics are part of the method

Section 4.3.4 defines coalition value conceptually but does not provide a complete operational contract for:

- The execution order of transactions retained in a coalition.
- Transactions whose nonce, balance, approval, deployment, or state dependencies were removed.
- Reverted or otherwise invalid counterfactual executions.
- Which noncandidate transactions remain in the background and how their state is replayed.
- Whether the observed arbitrage's calldata and amount remain fixed or a route/amount is reoptimized.

Those choices change $V(A)$ and therefore the resulting attribution. A deterministic chain provides reproducible execution **after these choices are fixed**; it does not choose the counterfactual model for the analyst. The fixed observed transaction in Sections 3.2-3.3 is the safest reading of the formal input, but it should not be expanded into an unstated guarantee that every method optimizes arbitrary routes in every coalition.

## 7. Costs, evaluation, and the proposed hybrid

Table 1 gives the following method-level scaling descriptions. They are the authors' summaries, with simulation/coalition evaluation costs hidden inside the abstractions. They are not full archive I/O or end-to-end pipeline bounds. [Table 1, PDF p. 6](https://arxiv.org/pdf/2604.27979v1#page=6).

| Method | Table 1 complexity | Practical caveat |
| --- | --- | --- |
| Bot data | $O(1)$ after model loading | Coverage and access depend on the bot; training and data capture are outside this summary. |
| Coefficient | $O(1)$ | Algorithm 2 nevertheless scans candidates; per-update versus whole-event scope is unclear. |
| Simulation | $O(\log \lvert C\rvert+m)$ | $m$ is the edge-to-arbitrage range; each probe requires a profit evaluation and historical state access. |
| Exact Shapley | $O(2^{\lvert C\rvert})$ | Number of coalition values grows exponentially; replay and marginal accumulation add work. |
| Monte Carlo Shapley | $O(N\lvert C\rvert)$ | Counts sampled marginal steps; each step still requires a defined coalition value. |

The proposed workflow is coefficient screening, simulation for routine primary attribution, and Shapley analysis for disagreements or suspected multiple contributors, with bot records as an optional external check. Table 1 suggests coefficient analysis around candidate sizes up to 1,000, simulation up to 200, exact Shapley below 20, and Monte Carlo Shapley up to 50. These are practical ranges presented by the authors, not correctness limits proven for every chain. [Sections 4.2 and 5.4, PDF pp. 5 and 9](https://arxiv.org/pdf/2604.27979v1#page=5).

The methods' reported validation uses triangulated references rather than an independently observed causal label. In particular, 100% Shapley accuracy is a comparison to the chosen Shapley reference, not proof of universal causal correctness. V1 also reports conflicting exact/Monte Carlo coverage values between Section 5.2 and Table 2, and an unreconciled runtime comparison. Preserve those distinctions when citing costs or coverage; see [the reproduction notes](05-reproduction.md).

## 8. What the single-source result does and does not say

On the February comparison sample of 2,526 events, the authors report that 96.7% have a dominant transaction accounting for more than 70% of **positive** Shapley value. They classify 83 events with tied maximum values as multiple-source cases. This is a dominance criterion for their selected candidate game, not proof that every other transaction has zero contribution, that negative contributions are absent, or that every atomic arbitrage on other networks has one cause. [Sections 5.3-5.4, PDF pp. 8-9](https://arxiv.org/pdf/2604.27979v1#page=8).

The practical inference is that choosing one primary contributor can summarize many observed cases in this dataset. The full vector, baseline, candidate window, and uncertainty remain necessary when interactions matter.
