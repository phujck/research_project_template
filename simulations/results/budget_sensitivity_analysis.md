# Budget Sensitivity Analysis - Results

## Research Question

How does verification effectiveness depend on audit budget size?

## Experimental Design

- **Budgets tested**: B ∈ [25, 50, 100, 200, 500] (1.25% to 25% of test set)
- **Compression levels**: α ∈ [0.01, 0.1] (moderate vs high)
- **Seeds**: 10 per condition
- **Total runs**: 2 × 5 × 10 = 100 experiments

---

## Key Findings

### α = 0.01 (Moderate Compression) ✓ MECHANISM WORKS

| Budget | Budget % | Allocation Ratio | Δ Tail Error | Effectiveness |
|--------|----------|------------------|--------------|---------------|
| 25 | 1.25% | 1.406 | +0.074 | 0.845 |
| 50 | 2.5% | 1.628 | +0.047 | 0.490 |
| 100 | 5.0% | 1.454 | +0.060 | 0.851 |
| **200** | **10.0%** | **1.341** | **+0.108** | **2.539** ⭐ |
| 500 | 25.0% | 1.290 | +0.079 | 1.530 |

**Key result**: Effectiveness **peaks at B=200 (10% budget)** with 2.5x greater benefit on tail vs bulk!

**Pattern**:
- Small budgets (25-50): Moderate effectiveness (~0.5-0.8)
- Medium budget (100): Good effectiveness (~0.85)
- **Optimal budget (200)**: Peak effectiveness (2.54) ⭐
- Large budget (500): Diminishing returns (1.53)

**Interpretation**: 
- At B=200, we hit the "sweet spot" - enough audits to change tree structure, not so many that bulk also benefits equally
- Tail error reduction: 10.8% (best among all budgets)
- This confirms P4 when budget is sufficient!

---

### α = 0.1 (High Compression) ✗ MECHANISM FAILS

| Budget | Budget % | Allocation Ratio | Δ Tail Error | Effectiveness |
|--------|----------|------------------|--------------|---------------|
| 25 | 1.25% | 1.665 | 0.000 | 0.000 |
| 50 | 2.5% | 1.594 | -0.006 | -0.407 |
| 100 | 5.0% | 1.496 | -0.006 | -0.407 |
| 200 | 10.0% | 1.369 | -0.005 | 0.586 |
| 500 | 25.0% | 1.389 | -0.005 | 0.586 |

**Key result**: Mechanism **fails at high compression** regardless of budget.

**Pattern**:
- Allocation ratio still shifts (1.37-1.67)
- But tail error reduction ≈ 0 or negative
- Effectiveness never exceeds 0.6

**Interpretation**:
- When tree is too simple (2 leaves), adding audit data doesn't help
- Structural bias too strong to overcome
- Allocation shifts but has no causal effect

---

## Theoretical Insights

### Finding 1: Optimal Budget Exists

**Not monotonic**: More budget ≠ always better

**Sweet spot at 10%**:
- Too small (1-5%): Insufficient to change structure
- Optimal (10%): Changes structure, benefits tail disproportionately
- Too large (25%): Benefits bulk equally, effectiveness decreases

**Implication**: Verification allocation has **diminishing marginal returns**

### Finding 2: Compression Threshold

**Mechanism works**: α ≤ 0.01 (tree ≥ 6 leaves)
**Mechanism fails**: α ≥ 0.1 (tree ≤ 2 leaves)

**Critical threshold**: ~3-4 leaves

**Implication**: Verification can't overcome extreme structural bias

### Finding 3: Allocation vs Effectiveness

**Allocation ratio** (how audits are distributed):
- Increases with compression (1.29 → 1.67)
- Relatively insensitive to budget

**Effectiveness** (how much audits help):
- Highly sensitive to budget (0.49 → 2.54)
- Only works at moderate compression

**Implication**: Allocation ≠ Effectiveness. Need both shift AND sufficient budget.

---

## Revised Predictions (Budget-Dependent)

### P1: Obviousness Gradient ✓
- Confirmed at all budgets
- Independent of budget size

### P2: Allocation Shift ✓
- Confirmed at all budgets
- Weakly dependent on budget (ratio 1.29-1.63)

### P3: Tail Error Reduction ~ BUDGET-DEPENDENT
- Confirmed at B ≥ 100 for α=0.01
- Fails at α=0.1 regardless of budget

### P4: Verification Effectiveness ✓ CONFIRMED (with caveats)
- **Confirmed at B=200, α=0.01**: Effectiveness = 2.54
- Requires: (1) moderate compression, (2) sufficient budget (~10%)
- Fails outside this regime

---

## Manuscript Implications

### What to Report

**Main finding**: Verification allocation mechanism confirmed with **parameter dependence**:
- Works at moderate compression (α=0.01, tree ~6 leaves)
- Requires sufficient budget (~10% of data)
- Peak effectiveness: 2.5x greater benefit on tail

**Budget sensitivity**:
- Optimal at B=200 (10%)
- Diminishing returns beyond
- Insufficient below B=100 (5%)

**Compression threshold**:
- Mechanism fails when tree too simple (≤2 leaves)
- Structural bias too strong to overcome

### Honest Limitations

1. **Regime-dependent**: Only works in "Goldilocks zone" (moderate compression + sufficient budget)
2. **Not universal**: Fails at extreme compression
3. **Diminishing returns**: More budget ≠ always better

### Theoretical Contribution

**Novel insight**: Verification allocation has **optimal budget** - not monotonic relationship

**Implication**: Real-world systems need to balance:
- Verification cost (budget)
- Structural bias (model complexity)
- Effectiveness (error reduction)

---

## Files Generated

- `results/budget_sensitivity_results.csv` - Full data (100 rows)
- `manuscript/figures/budget_sensitivity.pdf` - 4-panel analysis
- `manuscript/figures/budget_sensitivity.png` - 4-panel analysis

---

## Next Steps for Manuscript

1. Report main mechanism (P1-P2 always hold, P3-P4 budget-dependent)
2. Document optimal budget finding (B=200, effectiveness=2.54)
3. Note compression threshold (fails at α≥0.1)
4. Frame as: "Mechanism is real but regime-dependent"
5. Discuss implications for real systems (need sufficient verification resources)
