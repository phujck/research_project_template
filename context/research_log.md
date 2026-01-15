# Research Log: The Fragility of Obviousness

## 2026-01-15: Phase II - Expansion & Formalization

### 1. Theory Expansion
*   **Context**: The initial manuscript relied on intuition ("Obviousness"). We needed to ground this in established science to survive peer review (and the "Obviousness Trap").
*   **Action**: Conducted a targeted literature sweep.
*   **Key Findings**:
    *   *Cognitive Science*: "Processing Fluency" (Reber 1999) is the psychological correlate of our computational cost metric.
    *   *AI Safety*: "Simplicity Bias" (Teney 2021) describes the exact failure mode we simulated.
    *   *Thermodynamics*: MDL (Grunwald 2004) provides the formal link between Compression and Probability.
*   **Result**: Rewrote Sections 2 (Formalization) and 3 (Methods) of `main.tex`. "Obviousness" is now defined as $O_R(P) = 1/C_{ver}$.

### 2. Manuscript Refinement
*   **Formatting**: Migrated from standard `article` class to `revtex4-2` (APS/PRL style) for a professional physics look.
*   **Styling**: Enforced strict LaTeX quoting (``...'' vs "...").
*   **Status**: Compiled successfully (Draft 2.1).

### 3. Simulation Status
*   **Current State**: Deterministic Fragility Curve (Ensemble Mean).
*   **Missing**: Statistical Confidence Intervals (Error Bars).
*   **Next**: Bootstrap verification to prove the "Fragility Gap" is statistically significant.

### 4. Continuous Simulation (The Runge Cliff)
*   **Goal**: Demonstrate universality of the trap beyond discrete logic.
*   **Method**: Polynomial Regression on a linear function with a high-frequency spike ($x=0.98$).
*   **Findings**:
    *   Low-degree models (High Obviousness) are blind to the spike (Spectral Blindness).
    *   Proprietary Analysis: This aligns with our theory via **Construction Cost**. Agents default to the standard polynomial basis because it's "free," avoiding the high cost of finding a custom spike-aware basis.
*   **Status**: Implemented (`continuous_runner.py`), Visualized (`runge_fits.pdf`), and Integrated into Manuscript (Section 4.1).
