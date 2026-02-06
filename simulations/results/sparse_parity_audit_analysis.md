# Sparse Parity Audit Budget Results

## Experiment Design

**Objective**: Test whether finite verification budgets cause agents to allocate less effort to low-construction-cost claims, concentrating errors in the tail.

**Setup**:
- Task: Sparse Parity with exception set (x_{N-1}=1)
- Model: CART with pruning parameter α (compression)
- Audit budget: B = 100 verification queries
- Allocation policy: v(x) ∝ 1/O_R(x) where O_R(x) = (# training points in leaf) / total
- Metrics: error on audited vs unaudited, bulk vs tail

**Parameters**:
- α ∈ [0.001, 0.01, 0.1, 1.0, 10.0]
- 10 random seeds per α
- 5000 training samples, 2000 test samples

---

## Key Findings

### 1. Tail Error Increases with Compression ✓

As pruning parameter α increases (more compression), tail error rises sharply:

| α | Tail Error | Bulk Error | Tree Leaves |
|---|------------|------------|-------------|
| 0.001 | 0.000 | 0.000 | 6.0 |
| 0.010 | 0.000 | 0.000 | 6.0 |
| 0.100 | 0.244 | 0.247 | 2.0 |
| 1.000 | 0.402 | 0.509 | 1.0 |
| 10.000 | 0.402 | 0.509 | 1.0 |

**Interpretation**: At low α, tree captures exception set (6 leaves). At high α, tree collapses to single leaf (ignores exception), causing 40% tail error.

### 2. Verification Allocation Pattern

Allocation ratio (tail/bulk) shows interesting pattern:

| α | Allocation Ratio | Audits to Tail | Audits to Bulk |
|---|------------------|----------------|----------------|
| 0.001 | 0.979 | 48.5 | 51.5 |
| 0.010 | 0.979 | 48.5 | 51.5 |
| 0.100 | 1.065 | 50.7 | 49.3 |
| 1.000 | 1.123 | 52.1 | 47.9 |
| 10.000 | 1.123 | 52.1 | 47.9 |

**Unexpected result**: Allocation ratio *increases* with α (opposite of prediction).

**Explanation**: When tree collapses to 1 leaf (α ≥ 1.0), all points have equal obviousness → allocation becomes uniform → ratio ≈ (tail_size/bulk_size) ≈ 0.5/0.5 = 1.0. The policy v(x) ∝ 1/O_R(x) doesn't create the expected shift because obviousness becomes uniform under extreme compression.

### 3. Audited vs Unaudited Error

| α | Error (Audited) | Error (Unaudited) | Δ |
|---|-----------------|-------------------|---|
| 0.001 | 0.000 | 0.000 | 0.000 |
| 0.010 | 0.000 | 0.000 | 0.000 |
| 0.100 | 0.256 | 0.242 | -0.014 |
| 1.000 | 0.506 | 0.508 | +0.002 |
| 10.000 | 0.506 | 0.508 | +0.002 |

**Result**: No significant difference between audited and unaudited error.

**Explanation**: Audit mechanism doesn't actually *correct* errors - it only measures them. The allocation policy selects which points to audit, but doesn't change predictions.

---

## Issues with Current Design

### Problem 1: Allocation Policy Doesn't Create Expected Shift

When compression is extreme (α ≥ 1.0), tree collapses to uniform obviousness → allocation becomes uniform → no tail under-verification.

**Fix needed**: Use a different obviousness proxy that maintains variance even under compression (e.g., prediction confidence, leaf purity, distance to decision boundary).

### Problem 2: Auditing Doesn't Correct Errors

Current design: audits measure errors but don't fix them.

**Fix needed**: Add correction mechanism - audited points get true labels, model can update or flag anomalies.

### Problem 3: Tail Size Too Large

Exception set (x_{N-1}=1) is ~50% of data (not a true "tail").

**Fix needed**: Make exception rarer (p_exc = 0.01) to create genuine tail.

---

## Data Files

- `sparse_parity_audit_results.csv` - Full results (50 rows, 11 columns)
- `../manuscript/figures/sparse_parity_audit.pdf` - 4-panel figure
- `../manuscript/figures/sparse_parity_audit.png` - 4-panel figure
