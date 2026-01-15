# Theory: Shortcut Learning and the Obviousness Trap

This document formalises the third simulation demonstrating how representational ease leads to rational blindness under distribution shift.

## 1. Feature Definition
We consider a problem space where a target $y$ is determined by two features:
- **Core Feature ($z_{core}$)**: The true causal invariant. Learning/using this feature is "expensive" in the current representation.
- **Shortcut Feature ($z_{short}$)**: A spurious correlant. Learning/using this feature is "cheap" (high obviousness).

## 2. Representational Costs
We define the construction costs as:
- $C_{cons}(z_{short}) = 1$
- $C_{cons}(z_{core}) = 1 + \alpha$

Where $\alpha \ge 0$ represents the **Compression Pressure** or the extra effort required to move from the "obvious" primitive to the "robust" core.

## 3. Policy and Verification
Following the paper's central thesis:
1. **Obviousness $O_R$**: $O_R(z_{short}) > O_R(z_{core})$ for any $\alpha > 0$.
2. **Verification Budget $v(P)$**: The agent follows the rule $v(P) \propto 1/O_R(P)$.
3. **Consequence**: As the signal of cheapness ($O_R$) increases for the shortcut, the verification effort $v$ on the mapping $z_{short} \to y$ collapses toward zero.

## 4. The Trap (Distribution Shift)
In the training environment ($D_{train}$), $Corr(z_{short}, z_{core}) \approx 1$. The representation is efficient and accurate.
In the shifted environment ($D_{shift}$), $Corr(z_{short}, z_{core}) \to 0$.

Because the agent has budgeted zero verification for the "obvious" shortcut, it cannot detect that the relationship has broken. It remains in a state of **Rational Blindness**, producing the predicted error geometry:
- **Head Accuracy**: High on $D_{train}$.
- **Tail Fragility**: $100\%$ error on the subset where $z_{short} \neq z_{core}$ in $D_{shift}$.

## 5. Formal Link to Paper
This simulation directly instantiates the "bookkeeping failure": the agent fails to track that its high performance in $D_{train}$ is bought by a representational shortcut, misclassifying the "easy" heuristic as a "safe" invariant.
