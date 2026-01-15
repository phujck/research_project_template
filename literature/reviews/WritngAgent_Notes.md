# Literature Review Summary: The Coupled Story

## Legitimising the Primitives
The literature across Cognitive Science, Economics, and Sociology provides robust evidence for our project's primitives:
- **Fluency as Signal**: Reber (2004) and Hasher (1977) establish that ease of processing (Fluency) is used as a proxy for truth/validity.
- **Verification Policy**: Sims (2003) demonstrates that bounded agents adopt a verification policy that ignores info based on processing constraints (Rational Inattention).
- **Fluency Leaks Backward**: Camerer (1989) and Fischhoff (1975) prove that once knowledge is acquired, its construction cost is retrospectively underestimated.
- **Social Obsolescence**: Merton (1968) identifies the social end-state of this process as "Obliteration by Incorporation."

## The Coupled Story Gap
While each field holds a piece of the puzzle, none captures the full feedback loop of the **Obviousness Trap**:
1. **Representation**: A toolkit (e.g., a standard basis) is built.
2. **Fluency**: Claims in that basis achieve low construction cost ($C_{cons} \to 0$).
3. **Verification Policy**: The agent rationally budgets zero verification for high-fluency claims.
4. **Tail Error Geometry**: Errors concentrate in the regions the representation doesn't compress (the unverified tails).

## Our Contribution
We provide:
1. **The Coupling**: A unified formal model linking representation cost to verification policy.
2. **The Cost Formalisation**: $O_R(P) = 1/C_{cons}$ as the bridge between information theory and psychology.
3. **The Toy-World Demonstration**: Proof-of-concept simulations (Sparse Parity and Runge Cliff) showing that optimal average performance under this policy *guarantees* tail fragility.

## Key Sources for Drafting
- **Bookkeeping Failure**: Support with **Ohlsson (1992)** (restructuring), **Ash (2012)** (hindsight of insight), and **Howard (1979)** (response-shift bias). Match the "Principle of Obviousness" to the formal model $C_{R0} \to C_{R1}$.
- **Shortcut Learning**: Results confirm the "Obviousness Trap" via three behavioural regimes:
    1.  **Robust ($Acc=1.0$)**: At low $\alpha$ (high $C$), the model maintains a "Mixed (Core Dominant)" representation, preserving ground-truth invariants.
    2.  **Blind ($Acc_{shift} \approx 0.09$)**: At moderate $\alpha$ (the trap), the model switches to "Blind (Shortcut Only)." It maintains near-perfect training fluency ($Acc \approx 0.994$) but is $100\%$ fragile under distribution shift.
    3.  **Collapsed**: At extreme $\alpha$, all representational signal is pruned.
    This demonstrates that efficiency pressure directly manufactures rational blindness by incentivising the divestment from expensive core features.

> [!NOTE]
> All drafting must now use British English spelling per the global directive in `context/AGENTS.md`.
