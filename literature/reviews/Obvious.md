---
citekey: "McCaulObvious"
title: "McCaul's Principle of Obviousness"
authors: ["Author Name"]
year: 2026
venue: "Draft"
status: "Summarized"
tags: ["cognitive science", "information theory", "representation"]
---

# Abstract
The paper argues that humans routinely collapse the distinction between (i) obviousness in a particular representation, (ii) triviality across representations, and (iii) truth. It proposes **McCaul's Principle**: once a representation $R$ has made a result $P$ cheap to see (low cost $C_R(P)$), agents misremember its prior difficulty and reclassify it as trivial, erasing the work embodied in the representation.

# Key Findings
- **Obviousness ($O_R(P)$)**: Defined as the inverse cost of verifying $P$ given representation $R$. High compression $\rightarrow$ High Obviousness.
- **Triviality ($T(P)$)**: Defined as the minimum cost over *all* accessible representations.
- **The Error**: Agents substitute $O_{R_{current}}(P)$ for $T(P)$.
- **Implication**: This explains under-attribution of credit in science and "hallucination acceptance" in AI (fluent = obvious = true).

# Methodology
- **Formalism**:
    - Let $W$ be the world/state space.
    - Let $R: W \to \mathcal{C}$ be a representation (compression map).
    - Cost function $C_R(P)$: Cognitive/Computational cost to verify $P$ using $R$.
- **Hypothesis Testing**:
    - Proposed logic for experiments (Pre/Post difficulty ratings).
    - AI Experiment: "Fluent" hallucinations are checked less ($V(P) \approx 0$).

# Relevance to Project
- This is the **Core Theory** of our project.
- **Simulation Goal**: We need to simulate agents finding representations.
- **Key Equation**:
$$ O_R(P) \propto \frac{1}{C_R(P)} $$
$$ \text{Bias} = O_{R_{final}}(P) - O_{R_{initial}}(P) $$

# Notes & Quotes
- "Hallucinations are answers that are obvious in representation space and untested in reality space."
- "The results it made possible look trivial within that formalism."
