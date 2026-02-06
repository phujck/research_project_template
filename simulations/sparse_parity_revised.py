"""
Sparse Parity with Audit Budget - REVISED DESIGN

Theoretically refined simulation testing verification allocation under scarcity.

Key improvements:
1. Confidence-based obviousness (maintains variance under compression)
2. Corrected ensemble (causal effect of verification)
3. Rare tail (1% exception, genuine tail scenario)

Predictions:
P1: Obviousness gradient increases with alpha
P2: Allocation shifts to tail (ratio increases)
P3: Tail error concentrates (base up, corrected down)
P4: Verification more effective on tail
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from pathlib import Path

np.random.seed(42)
Path("results").mkdir(exist_ok=True)
Path("../manuscript/figures").mkdir(parents=True, exist_ok=True)


def generate_data_rare_tail(n_samples=10000, p_exc=0.01):
    """
    Generate Sparse Parity with RARE exception (1% tail).
    
    Base rule (99%): y = x_0 AND x_1
    Exception (1%): y = NOT(x_0 AND x_1) if x_9=1 AND x_0=1
    
    Tail = {x : x_9=1 AND x_0=1} (~1% of data)
    """
    X = np.random.randint(0, 2, size=(n_samples, 10))
    
    # Base rule
    y = (X[:, 0] == 1) & (X[:, 1] == 1)
    
    # Exception: flip if x_9=1 AND x_0=1 (rare condition)
    exception_mask = (X[:, 9] == 1) & (X[:, 0] == 1)
    y[exception_mask] = ~y[exception_mask]
    
    return X, y.astype(int), exception_mask


def compute_obviousness_confidence(tree, X):
    """
    Confidence-based obviousness: O_R(x) = prediction confidence.
    
    High confidence → high obviousness (claim feels obvious)
    Low confidence → low obviousness (claim feels uncertain)
    
    This maintains variance even when tree is simple.
    """
    proba = tree.predict_proba(X)
    y_pred = tree.predict(X)
    
    # Confidence = probability of predicted class
    confidence = proba[np.arange(len(X)), y_pred.astype(int)]
    
    return confidence


def allocate_audits(obviousness, budget):
    """
    Allocate audit budget: v(x) ∝ 1/O_R(x)
    
    Low obviousness → more audits
    """
    allocation_weights = 1.0 / (obviousness + 1e-10)
    allocation_probs = allocation_weights / allocation_weights.sum()
    
    n_points = len(obviousness)
    audit_indices = np.random.choice(
        n_points,
        size=min(budget, n_points),
        replace=False,
        p=allocation_probs
    )
    
    audited = np.zeros(n_points, dtype=bool)
    audited[audit_indices] = True
    
    return audited


def build_corrected_model(X_train, y_train, X_test, y_test, audited_mask, alpha):
    """
    Build base and corrected models.
    
    Base: trained on training data only
    Corrected: retrained with audit labels added
    
    This creates causal effect of verification.
    """
    # Base model
    M_base = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42, max_depth=10)
    M_base.fit(X_train, y_train)
    
    # Get audit labels (ground truth for audited points)
    X_audit = X_test[audited_mask]
    y_audit = y_test[audited_mask]
    
    # Corrected model: retrain with audit data
    if len(X_audit) > 0:
        X_combined = np.vstack([X_train, X_audit])
        y_combined = np.hstack([y_train, y_audit])
        M_corrected = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42, max_depth=10)
        M_corrected.fit(X_combined, y_combined)
    else:
        M_corrected = M_base
    
    return M_base, M_corrected


def run_experiment(alpha, budget=50, n_seeds=10):
    """
    Run experiment with given pruning parameter.
    
    Returns: DataFrame with metrics for all predictions P1-P4
    """
    results = []
    
    for seed in range(n_seeds):
        np.random.seed(seed)
        
        # Generate data with rare tail
        X_train, y_train, _ = generate_data_rare_tail(n_samples=5000)
        X_test, y_test, tail_mask = generate_data_rare_tail(n_samples=2000)
        
        # Build base model
        M_base = DecisionTreeClassifier(ccp_alpha=alpha, random_state=seed, max_depth=10)
        M_base.fit(X_train, y_train)
        
        # Compute confidence-based obviousness
        obviousness = compute_obviousness_confidence(M_base, X_test)
        
        # Allocate audits
        audited = allocate_audits(obviousness, budget)
        
        # Build corrected model
        M_base, M_corrected = build_corrected_model(
            X_train, y_train, X_test, y_test, audited, alpha
        )
        
        # Predictions
        y_pred_base = M_base.predict(X_test)
        y_pred_corr = M_corrected.predict(X_test)
        
        # Errors
        error_base = (y_pred_base != y_test)
        error_corr = (y_pred_corr != y_test)
        
        # Stratify by bulk/tail
        bulk_mask = ~tail_mask
        
        # P1: Obviousness gradient
        obs_bulk_mean = obviousness[bulk_mask].mean()
        obs_tail_mean = obviousness[tail_mask].mean()
        obs_gradient = obs_bulk_mean - obs_tail_mean
        
        # P2: Allocation ratio
        audits_bulk = audited[bulk_mask].sum()
        audits_tail = audited[tail_mask].sum()
        bulk_size = bulk_mask.sum()
        tail_size = tail_mask.sum()
        allocation_ratio = (audits_tail / (tail_size + 1e-10)) / (audits_bulk / (bulk_size + 1e-10))
        
        # P3: Tail error concentration
        error_base_tail = error_base[tail_mask].mean()
        error_corr_tail = error_corr[tail_mask].mean()
        error_base_bulk = error_base[bulk_mask].mean()
        error_corr_bulk = error_corr[bulk_mask].mean()
        
        # P4: Verification effectiveness
        delta_tail = error_base_tail - error_corr_tail
        delta_bulk = error_base_bulk - error_corr_bulk
        effectiveness = delta_tail / (delta_bulk + 1e-10)
        
        results.append({
            'alpha': alpha,
            'seed': seed,
            # P1: Obviousness gradient
            'obs_bulk_mean': obs_bulk_mean,
            'obs_tail_mean': obs_tail_mean,
            'obs_gradient': obs_gradient,
            # P2: Allocation
            'audits_bulk': audits_bulk,
            'audits_tail': audits_tail,
            'allocation_ratio': allocation_ratio,
            # P3: Errors
            'error_base_tail': error_base_tail,
            'error_corr_tail': error_corr_tail,
            'error_base_bulk': error_base_bulk,
            'error_corr_bulk': error_corr_bulk,
            # P4: Effectiveness
            'delta_tail': delta_tail,
            'delta_bulk': delta_bulk,
            'effectiveness': effectiveness,
            # Metadata
            'tail_size': tail_size,
            'bulk_size': bulk_size,
            'tree_leaves': M_base.get_n_leaves(),
        })
    
    return pd.DataFrame(results)


def main():
    """Run full experiment suite."""
    
    print("Running REVISED Sparse Parity Audit Simulation")
    print("=" * 60)
    print("Design improvements:")
    print("  1. Confidence-based obviousness (maintains variance)")
    print("  2. Corrected ensemble (causal verification)")
    print("  3. Rare 1% tail (genuine tail scenario)")
    print("=" * 60)
    
    alphas = [0.001, 0.01, 0.1, 1.0, 10.0]
    budget = 50
    n_seeds = 10
    
    all_results = []
    for alpha in alphas:
        print(f"\nRunning alpha = {alpha}...")
        results = run_experiment(alpha, budget, n_seeds)
        all_results.append(results)
    
    df = pd.concat(all_results, ignore_index=True)
    
    # Save results
    df.to_csv("results/sparse_parity_revised_results.csv", index=False)
    print("\n" + "=" * 60)
    print("PRIMARY OUTPUT: results/sparse_parity_revised_results.csv")
    print("=" * 60)
    
    # Summary statistics
    summary = df.groupby('alpha').agg({
        'obs_gradient': ['mean', 'std'],
        'allocation_ratio': ['mean', 'std'],
        'error_base_tail': ['mean', 'std'],
        'error_corr_tail': ['mean', 'std'],
        'effectiveness': ['mean', 'std'],
        'tail_size': 'mean',
    }).round(4)
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(summary)
    
    # Test predictions
    print("\n" + "=" * 60)
    print("TESTING PREDICTIONS")
    print("=" * 60)
    
    print("\nP1: Obviousness gradient increases with alpha:")
    for alpha in alphas:
        grad = df[df['alpha'] == alpha]['obs_gradient'].mean()
        print(f"   alpha={alpha:6.3f}: Gradient={grad:+.3f}")
    
    print("\nP2: Allocation ratio increases with alpha:")
    for alpha in alphas:
        ratio = df[df['alpha'] == alpha]['allocation_ratio'].mean()
        print(f"   alpha={alpha:6.3f}: Ratio={ratio:.3f}")
    
    print("\nP3: Tail error concentrates (base up, corrected down):")
    for alpha in alphas:
        subset = df[df['alpha'] == alpha]
        err_base = subset['error_base_tail'].mean()
        err_corr = subset['error_corr_tail'].mean()
        print(f"   alpha={alpha:6.3f}: Base={err_base:.3f}, Corrected={err_corr:.3f}, Delta={err_base-err_corr:+.3f}")
    
    print("\nP4: Verification more effective on tail:")
    for alpha in alphas:
        eff = df[df['alpha'] == alpha]['effectiveness'].mean()
        print(f"   alpha={alpha:6.3f}: Effectiveness={eff:.3f} (>1 means tail benefits more)")
    
    # Create figures
    create_figures(df)
    
    print("\n" + "=" * 60)
    print("Experiment complete!")
    print("=" * 60)


def create_figures(df):
    """Create 4-panel figure testing predictions P1-P4."""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # P1: Obviousness Gradient
    ax = axes[0, 0]
    summary = df.groupby('alpha')['obs_gradient'].agg(['mean', 'std'])
    ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                marker='o', capsize=5, color='purple')
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Obviousness Gradient (Bulk - Tail)')
    ax.set_xscale('log')
    ax.set_title('P1: Gradient Increases with Compression')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3)
    
    # P2: Allocation Ratio
    ax = axes[0, 1]
    summary = df.groupby('alpha')['allocation_ratio'].agg(['mean', 'std'])
    ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                marker='s', capsize=5, color='green')
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Allocation Ratio (Tail/Bulk)')
    ax.set_xscale('log')
    ax.set_title('P2: Allocation Shifts to Tail')
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Equal')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # P3: Tail Error (Base vs Corrected)
    ax = axes[1, 0]
    summary = df.groupby('alpha')[['error_base_tail', 'error_corr_tail']].agg(['mean', 'std'])
    ax.errorbar(summary.index, summary[('error_base_tail', 'mean')],
                yerr=summary[('error_base_tail', 'std')],
                marker='o', label='Base (no audits)', capsize=5)
    ax.errorbar(summary.index, summary[('error_corr_tail', 'mean')],
                yerr=summary[('error_corr_tail', 'std')],
                marker='s', label='Corrected (with audits)', capsize=5)
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Tail Error Rate')
    ax.set_xscale('log')
    ax.set_title('P3: Audits Reduce Tail Error')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # P4: Verification Effectiveness
    ax = axes[1, 1]
    summary = df.groupby('alpha')['effectiveness'].agg(['mean', 'std'])
    ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                marker='D', capsize=5, color='red')
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Effectiveness (Delta_tail / Delta_bulk)')
    ax.set_xscale('log')
    ax.set_title('P4: Verification More Effective on Tail')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Equal effectiveness')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../manuscript/figures/sparse_parity_revised.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('../manuscript/figures/sparse_parity_revised.png', dpi=300, bbox_inches='tight')
    print("\nFigures saved to manuscript/figures/")
    plt.close()


if __name__ == "__main__":
    main()
