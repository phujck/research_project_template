"""
Budget Sensitivity Analysis

Tests how verification effectiveness depends on audit budget size.

Research question: Does increasing budget B strengthen the mechanism?

Predictions:
- Larger B → stronger allocation shift
- Larger B → greater tail error reduction  
- Larger B → higher effectiveness ratio

Budgets tested: B ∈ [25, 50, 100, 200, 500] (1.25% to 25% of test set)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from pathlib import Path

np.random.seed(42)
Path("results").mkdir(exist_ok=True)
Path("../manuscript/figures").mkdir(parents=True, exist_ok=True)


def generate_data_rare_tail(n_samples=10000):
    """Generate Sparse Parity with rare exception."""
    X = np.random.randint(0, 2, size=(n_samples, 10))
    y = (X[:, 0] == 1) & (X[:, 1] == 1)
    exception_mask = (X[:, 9] == 1) & (X[:, 0] == 1)
    y[exception_mask] = ~y[exception_mask]
    return X, y.astype(int), exception_mask


def compute_obviousness_confidence(tree, X):
    """Confidence-based obviousness."""
    proba = tree.predict_proba(X)
    y_pred = tree.predict(X)
    confidence = proba[np.arange(len(X)), y_pred.astype(int)]
    return confidence


def allocate_audits(obviousness, budget):
    """Allocate audits: v(x) ∝ 1/O_R(x)"""
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
    """Build base and corrected models."""
    M_base = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42, max_depth=10)
    M_base.fit(X_train, y_train)
    
    X_audit = X_test[audited_mask]
    y_audit = y_test[audited_mask]
    
    if len(X_audit) > 0:
        X_combined = np.vstack([X_train, X_audit])
        y_combined = np.hstack([y_train, y_audit])
        M_corrected = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42, max_depth=10)
        M_corrected.fit(X_combined, y_combined)
    else:
        M_corrected = M_base
    
    return M_base, M_corrected


def run_experiment(alpha, budget, n_seeds=10):
    """Run experiment with given alpha and budget."""
    results = []
    
    for seed in range(n_seeds):
        np.random.seed(seed)
        
        X_train, y_train, _ = generate_data_rare_tail(n_samples=5000)
        X_test, y_test, tail_mask = generate_data_rare_tail(n_samples=2000)
        
        M_base = DecisionTreeClassifier(ccp_alpha=alpha, random_state=seed, max_depth=10)
        M_base.fit(X_train, y_train)
        
        obviousness = compute_obviousness_confidence(M_base, X_test)
        audited = allocate_audits(obviousness, budget)
        
        M_base, M_corrected = build_corrected_model(
            X_train, y_train, X_test, y_test, audited, alpha
        )
        
        y_pred_base = M_base.predict(X_test)
        y_pred_corr = M_corrected.predict(X_test)
        
        error_base = (y_pred_base != y_test)
        error_corr = (y_pred_corr != y_test)
        
        bulk_mask = ~tail_mask
        
        # Metrics
        obs_gradient = obviousness[bulk_mask].mean() - obviousness[tail_mask].mean()
        
        audits_bulk = audited[bulk_mask].sum()
        audits_tail = audited[tail_mask].sum()
        allocation_ratio = (audits_tail / (tail_mask.sum() + 1e-10)) / (audits_bulk / (bulk_mask.sum() + 1e-10))
        
        error_base_tail = error_base[tail_mask].mean()
        error_corr_tail = error_corr[tail_mask].mean()
        error_base_bulk = error_base[bulk_mask].mean()
        error_corr_bulk = error_corr[bulk_mask].mean()
        
        delta_tail = error_base_tail - error_corr_tail
        delta_bulk = error_base_bulk - error_corr_bulk
        effectiveness = delta_tail / (delta_bulk + 1e-10)
        
        results.append({
            'alpha': alpha,
            'budget': budget,
            'budget_pct': budget / len(X_test) * 100,
            'seed': seed,
            'obs_gradient': obs_gradient,
            'allocation_ratio': allocation_ratio,
            'error_base_tail': error_base_tail,
            'error_corr_tail': error_corr_tail,
            'delta_tail': delta_tail,
            'delta_bulk': delta_bulk,
            'effectiveness': effectiveness,
            'audits_tail': audits_tail,
            'audits_bulk': audits_bulk,
        })
    
    return pd.DataFrame(results)


def main():
    """Run budget sensitivity analysis."""
    
    print("Budget Sensitivity Analysis")
    print("=" * 60)
    print("Testing how effectiveness depends on audit budget size")
    print("=" * 60)
    
    # Focus on moderate compression where mechanism is clearest
    alphas = [0.01, 0.1]
    budgets = [25, 50, 100, 200, 500]  # 1.25% to 25% of test set
    n_seeds = 10
    
    all_results = []
    for alpha in alphas:
        for budget in budgets:
            print(f"\nRunning alpha={alpha}, budget={budget} ({budget/20:.1f}%)...")
            results = run_experiment(alpha, budget, n_seeds)
            all_results.append(results)
    
    df = pd.concat(all_results, ignore_index=True)
    
    # Save results
    df.to_csv("results/budget_sensitivity_results.csv", index=False)
    print("\n" + "=" * 60)
    print("PRIMARY OUTPUT: results/budget_sensitivity_results.csv")
    print("=" * 60)
    
    # Analysis
    print("\n" + "=" * 60)
    print("BUDGET SENSITIVITY ANALYSIS")
    print("=" * 60)
    
    for alpha in alphas:
        print(f"\n--- Alpha = {alpha} ---")
        subset = df[df['alpha'] == alpha]
        summary = subset.groupby('budget').agg({
            'allocation_ratio': 'mean',
            'delta_tail': 'mean',
            'effectiveness': 'mean',
        }).round(3)
        print(summary)
    
    # Create figures
    create_figures(df)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


def create_figures(df):
    """Create budget sensitivity figures."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    alphas = df['alpha'].unique()
    colors = ['blue', 'red']
    
    # 1. Allocation Ratio vs Budget
    ax = axes[0, 0]
    for i, alpha in enumerate(alphas):
        subset = df[df['alpha'] == alpha]
        summary = subset.groupby('budget')['allocation_ratio'].agg(['mean', 'std'])
        ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                    marker='o', label=f'alpha={alpha}', capsize=5, color=colors[i])
    ax.set_xlabel('Audit Budget (# points)')
    ax.set_ylabel('Allocation Ratio (Tail/Bulk)')
    ax.set_title('Allocation Shift vs Budget')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.3)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Tail Error Reduction vs Budget
    ax = axes[0, 1]
    for i, alpha in enumerate(alphas):
        subset = df[df['alpha'] == alpha]
        summary = subset.groupby('budget')['delta_tail'].agg(['mean', 'std'])
        ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                    marker='s', label=f'alpha={alpha}', capsize=5, color=colors[i])
    ax.set_xlabel('Audit Budget (# points)')
    ax.set_ylabel('Tail Error Reduction (Base - Corrected)')
    ax.set_title('Verification Benefit vs Budget')
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Effectiveness vs Budget
    ax = axes[1, 0]
    for i, alpha in enumerate(alphas):
        subset = df[df['alpha'] == alpha]
        summary = subset.groupby('budget')['effectiveness'].agg(['mean', 'std'])
        ax.errorbar(summary.index, summary['mean'], yerr=summary['std'],
                    marker='D', label=f'alpha={alpha}', capsize=5, color=colors[i])
    ax.set_xlabel('Audit Budget (# points)')
    ax.set_ylabel('Effectiveness (Delta_tail / Delta_bulk)')
    ax.set_title('Relative Effectiveness vs Budget')
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.3, label='Equal')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Tail Error: Base vs Corrected (for alpha=0.01)
    ax = axes[1, 1]
    subset = df[df['alpha'] == 0.01]
    summary_base = subset.groupby('budget')['error_base_tail'].agg(['mean', 'std'])
    summary_corr = subset.groupby('budget')['error_corr_tail'].agg(['mean', 'std'])
    ax.errorbar(summary_base.index, summary_base['mean'], yerr=summary_base['std'],
                marker='o', label='Base (no audits)', capsize=5)
    ax.errorbar(summary_corr.index, summary_corr['mean'], yerr=summary_corr['std'],
                marker='s', label='Corrected (with audits)', capsize=5)
    ax.set_xlabel('Audit Budget (# points)')
    ax.set_ylabel('Tail Error Rate')
    ax.set_title('Tail Error vs Budget (alpha=0.01)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../manuscript/figures/budget_sensitivity.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('../manuscript/figures/budget_sensitivity.png', dpi=300, bbox_inches='tight')
    print("\nFigures saved to manuscript/figures/")
    plt.close()


if __name__ == "__main__":
    main()
