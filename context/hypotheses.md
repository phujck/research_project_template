# Scientific Hypotheses

## H1: The Erasure of Difficulty (McCaul's Bias)
**Claim**: Agents minimizing verification cost will systematically underestimate the complexity of a problem $P$ after learning an optimal representation $R^*$.
**Formalism**:
Let $C(P|R)$ be the cost of verifying $P$ given $R$.
Let $W(R)$ be the work required to discover $R$.
The bias $\Delta$ is defined as:
$$ \Delta = C(P|R_{naive}) - (C(P|R^*) + \epsilon W(R^*)) $$
If $\epsilon \to 0$ (ignoring discovery cost), then $\Delta$ is positive and large, leading to "false triviality".

## H2: Hallucination via Smoothness
**Claim**: In AI systems, propositions $P$ that lie on high-likelihood manifolds in representation space (High "Obviousness") are accepted as True, regardless of their verification cost in Ground Truth space.
**Formalism**:
$$ \text{Trust}(P) \propto P(P|R) $$
$$ \text{Truth}(P) = \mathbb{I}(\text{Verify}(P)) $$
The error arises when $\text{Trust}(P) \gg \text{Truth}(P)$.
