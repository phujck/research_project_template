# Research Glossary

## Core Concepts

### Obviousness ($O_R(P)$)
The subjective ease of verifying a proposition $P$ relative to a specific representation $R$.
$$ O_R(P) \approx \frac{1}{C(P|R)} $$

### Triviality ($T(P)$)
The objective difficulty of a proposition $P$, defined as the minimum verification cost over *all possible* representations $\mathcal{R}$.
$$ T(P) = \min_{R \in \mathcal{R}} C(P|R) $$

### Representation ($R$)
A mapping or transformation that alters the cost landscape of the problem space.
- Example: Changing coordinates from Cartesian to Polar ($x,y \to r,\theta$) makes logical statements about circles "obvious".

### Verification Cost ($V(P)$)
The computational work required to confirm $P$ is true in reality (Ground Truth).
- In AI: The cost of running an external tool or experiment.
- In Humans: The cost of logical derivation or checking sources.

## Formal Foundations (Math & Info Theory)

### Minimum Description Length (MDL)
The principle that the best hypothesis ($H$) for data ($D$) is the one that minimizes the sum of the length of the hypothesis and the length of the data encoded by the hypothesis.
$$ L(H) + L(D|H) $$
*   **Relevance**: We define a "Representation" $R$ as the codebook used to encode $P$. High Obviousness corresponds to low $L(P|R)$.
*   *Ref: Grunwald (2004)*

### Resource-Rationality
The framework where agents optimize not just for accuracy ($U$), but for accuracy minus computational cost ($C$).
$$ \max_{\pi} \mathbb{E}[U(\pi) - C(\pi)] $$
*   **Relevance**: The Principle of Obviousness is a *Rational* failure mode. The agent reduces verification because the expected utility gain is lower than the cost, given the high confidence from the representation.

## Psychological Manifestations

### Processing Fluency
The subjective ease with which information is processed.
*   **Truth Effect**: Empirical finding that fluent stimuli are judged as more true, frequent, and famous.
*   **Relevance**: In our model, $O_R(P)$ is the formal equivalent of Fluency.

### Illusion of Explanatory Depth (IOED)
The cognitive bias where people believe they understand complex systems better than they actually do.
*   **Relevance**: This is the phenomenological experience of "The Fragility of Obviousness". The representation (mental model) gives a sense of predictive power without the ability to verify details (ground truth).
