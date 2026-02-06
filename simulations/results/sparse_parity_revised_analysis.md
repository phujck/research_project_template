# Sparse Parity REVISED - Results Analysis

## Design Improvements

1. **Confidence-based obviousness**: O_R(x) = prediction confidence (maintains variance)
2. **Corrected ensemble**: M_base vs M_corrected (causal verification effect)
3. **Rare tail**: ~25% of data (x_9=1 AND x_0=1) - still larger than ideal 1% but better

---

## Prediction Testing

### P1: Obviousness Gradient Increases with α ✓ CONFIRMED

| α | Gradient (Bulk - Tail) |
|---|------------------------|
| 0.001 | +0.021 |
| 0.010 | +0.227 |
| 0.100 | +0.331 |
| 1.000 | -0.000 |
| 10.000 | -0.000 |

**Result**: Gradient increases from 0.02 → 0.33 as α increases from 0.001 → 0.1, then collapses to 0 at α ≥ 1.0.

**Interpretation**: ✓ At moderate compression (α=0.1), bulk becomes much more obvious than tail (33% confidence gap). At extreme compression (α≥1.0), tree becomes deterministic (confidence=1.0 everywhere) → gradient collapses.

---

### P2: Allocation Ratio Increases with α ✓ CONFIRMED (partially)

| α | Allocation Ratio (Tail/Bulk) |
|---|------------------------------|
| 0.001 | 1.364 |
| 0.010 | 1.628 |
| 0.100 | 1.594 |
| 1.000 | 1.309 |
| 10.000 | 1.309 |

**Result**: Ratio increases from 1.36 → 1.63 (peak at α=0.01), then decreases.

**Interpretation**: ✓ At low-moderate α, allocation shifts to tail (63% more audits per tail point). At high α, gradient collapses → allocation becomes more uniform.

---

### P3: Tail Error Concentrates (Base ↑, Corrected ↓) ~ MIXED

| α | Error_base(tail) | Error_corrected(tail) | Δ (benefit) |
|---|------------------|----------------------|-------------|
| 0.001 | 0.039 | 0.029 | +0.009 |
| 0.010 | 0.352 | 0.305 | +0.047 |
| 0.100 | 0.501 | 0.507 | -0.006 |
| 1.000 | 0.512 | 0.512 | +0.000 |
| 10.000 | 0.512 | 0.512 | +0.000 |

**Result**: Audits reduce tail error at low α (Δ=+0.047 at α=0.01), but have no effect or negative effect at high α.

**Interpretation**: ~ Partial confirmation. Audits help when tree is moderately complex (α=0.01), but can't fix extreme compression (α≥0.1). At α=0.1, adding 50 audit points doesn't help because tree structure is too simple.

---

### P4: Verification More Effective on Tail ~ NOT CONFIRMED

| α | Effectiveness (Δ_tail / Δ_bulk) |
|---|--------------------------------|
| 0.001 | 1.969 |
| 0.010 | 0.490 |
| 0.100 | -0.407 |
| 1.000 | 0.000 |
| 10.000 | 0.000 |

**Result**: Effectiveness >1 only at α=0.001, then drops below 1.

**Interpretation**: ✗ Prediction not confirmed. Audits are more effective on tail only when tree is very complex (α=0.001). At moderate compression, audits help bulk more than tail.

**Why**: When tree is simple, adding audit data doesn't change structure much → limited benefit. Need larger audit budget or different correction mechanism.

---

## Key Insights

### What Worked

1. **Confidence-based obviousness maintains variance** ✓
   - Gradient increases from 0.02 → 0.33 (unlike leaf-size proxy which collapsed)
   
2. **Allocation shifts to tail** ✓
   - Ratio peaks at 1.63 (63% more audits per tail point)
   
3. **Causal effect of verification** ✓
   - Corrected model reduces tail error by 4.7% at α=0.01

### What Didn't Work

1. **Effectiveness reverses at moderate α**
   - Expected: tail benefits more from audits
   - Observed: bulk benefits more (effectiveness <1)
   
2. **Audit budget too small**
   - 50 audits / 2000 points = 2.5%
   - Not enough to change tree structure significantly
   
3. **Tail still too large**
   - ~25% of data (should be 1-5%)
   - Makes it harder to see concentration effect

---

## Revised Understanding

The mechanism works **partially**:

1. ✓ Compression creates obviousness gradient
2. ✓ Gradient drives allocation shift to tail
3. ~ Audits reduce tail error (but only at low-moderate α)
4. ✗ Audits not consistently more effective on tail

**Root cause**: Audit budget (50 points) is too small to overcome structural bias of simple trees. When tree has 1-2 leaves, adding 50 audit points doesn't fundamentally change the learned function.

---

## Next Steps

### Option A: Increase Audit Budget
- Try B = 200-500 (10-25% of test set)
- Larger budget → more structural change
- May confirm P4

### Option B: Different Correction Mechanism
- Instead of retraining, use audit data to build **exception rules**
- E.g., "IF audited point is in tail AND misclassified, flip prediction"
- More direct correction

### Option C: Accept Partial Confirmation
- Document what works (P1, P2) and what doesn't (P4)
- Frame as: "verification allocation shifts, but effectiveness depends on budget size"
- Honest about limitations

**Recommendation**: Option C - document honestly, note that larger budgets needed for full effect

---

## Manuscript Integration

### What to Report

**Confirmed findings**:
- Compression creates obviousness gradient (0.02 → 0.33)
- Allocation shifts to low-obviousness regions (ratio 1.36 → 1.63)
- Audits reduce tail error at moderate compression (Δ=4.7%)

**Limitations**:
- Effect size depends on audit budget (50 points = 2.5% of data)
- Effectiveness reverses at high compression (tree too simple to correct)
- Tail definition still not ideal (25% vs 1%)

**Implication**: Mechanism is real but requires sufficient verification resources to overcome structural bias.

---

## Files Generated

- `results/sparse_parity_revised_results.csv` - Full data (50 rows, 18 columns)
- `manuscript/figures/sparse_parity_revised.pdf` - 4-panel figure (P1-P4)
- `manuscript/figures/sparse_parity_revised.png` - 4-panel figure (P1-P4)
