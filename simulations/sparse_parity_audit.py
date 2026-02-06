"""
Sparse Parity with Audit Budget

Tests the core mechanism: under finite verification budgets, agents allocate
less effort to low-construction-cost claims, causing tail errors to concentrate.

Design:
- CART with pruning parameter alpha (compression)
- Finite audit budget B = 100 verification queries
- Allocation policy: v(x) proportional to 1/O_R(x) where O_R(x) = obviousness
- Measure: error on audited vs unaudited, bulk vs tail
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Create output directories
Path("results").mkdir(exist_ok=True)
Path("../manuscript/figures").mkdir(parents=True, exist_ok=True)


def generate_sparse_parity_data(n_samples=10000, n_bits=10):
    """
    Generate Sparse Parity data with exception set.
    
    Target: y = x_0 AND x_1 if x_{N-1}=0, else NOT(x_0 AND x_1)
    Tail set: {x : x_{N-1} = 1} (exception condition)
    """
    X = np.random.randint(0, 2, size=(n_samples, n_bits))
    
    # Base rule: x_0 AND x_1
    base_rule = (X[:, 0] == 1) & (X[:, 1] == 1)
    
    # Exception: flip if x_{N-1} = 1
    exception_mask = X[:, n_bits-1] == 1
    y = base_rule.copy()
    y[exception_mask] = ~base_rule[exception_mask]
    
    return X, y.astype(int), exception_mask


def compute_obviousness(tree, X):
    """
    Compute obviousness O_R(x) for each point.
    
    O_R(x) = (# training points in leaf) / (total training points)
    High O_R → claim is "obvious" (many similar examples)
    Low O_R → claim is "non-obvious" (rare, exception-like)
    """
    # Get leaf IDs for test points
    leaf_ids = tree.apply(X)
    
    # Get number of samples in each leaf from training
    n_node_samples = tree.tree_.n_node_samples
    
    # Map each test point to its leaf's sample count
    obviousness = np.array([n_node_samples[leaf_id] for leaf_id in leaf_ids], dtype=float)
    obviousness = obviousness / obviousness.sum()  # Normalize
    
    return obviousness


def allocate_audits(obviousness, budget):
    """
    Allocate audit budget using policy: v(x) proportional to 1/O_R(x)
    
    Returns: boolean array indicating which points are audited
    """
    # Inverse obviousness (less obvious → more audits)
    allocation_weights = 1.0 / (obviousness + 1e-10)
    allocation_probs = allocation_weights / allocation_weights.sum()
    
    # Sample audit indices
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


def run_experiment(alpha, budget=100, n_seeds=10):
    """
    Run single experiment with given pruning parameter and budget.
    
    Returns: DataFrame of metrics
    """
    results = []
    
    for seed in range(n_seeds):
        np.random.seed(seed)
        
        # Generate data
        X_train, y_train, _ = generate_sparse_parity_data(n_samples=5000)
        X_test, y_test, tail_mask_test = generate_sparse_parity_data(n_samples=2000)
        
        # Train CART with pruning
        tree = DecisionTreeClassifier(
            ccp_alpha=alpha,
            random_state=seed,
            max_depth=10
        )
        tree.fit(X_train, y_train)
        
        # Compute obviousness on test set
        obviousness = compute_obviousness(tree, X_test)
        
        # Allocate audits
        audited = allocate_audits(obviousness, budget)
        
        # Get predictions
        y_pred = tree.predict(X_test)
        
        # Compute errors
        errors = (y_pred != y_test)
        
        # Metrics
        bulk_mask = ~tail_mask_test
        
        results.append({
            'alpha': alpha,
            'seed': seed,
            'error_audited': errors[audited].mean() if audited.sum() > 0 else np.nan,
            'error_unaudited': errors[~audited].mean() if (~audited).sum() > 0 else np.nan,
            'error_bulk': errors[bulk_mask].mean(),
            'error_tail': errors[tail_mask_test].mean(),
            'audits_to_bulk': audited[bulk_mask].sum(),
            'audits_to_tail': audited[tail_mask_test].sum(),
            'bulk_size': bulk_mask.sum(),
            'tail_size': tail_mask_test.sum(),
            'tree_leaves': tree.get_n_leaves(),
        })
    
    return pd.DataFrame(results)


def main():
    """Run full experiment suite."""
    
    print("Running Sparse Parity Audit Budget Experiments...")
    print("=" * 60)
    
    # Experiment parameters
    alphas = [0.001, 0.01, 0.1, 1.0, 10.0]
    budget = 100
    n_seeds = 10
    
    # Run experiments
    all_results = []
    for alpha in alphas:
        print(f"\nRunning alpha = {alpha}...")
        results = run_experiment(alpha, budget, n_seeds)
        all_results.append(results)
    
    df = pd.concat(all_results, ignore_index=True)
    
    # Save results (PRIMARY OUTPUT FOR ANALYSIS)
    df.to_csv("results/sparse_parity_audit_results.csv", index=False)
    print("\n" + "=" * 60)
    print("PRIMARY OUTPUT: results/sparse_parity_audit_results.csv")
    print("=" * 60)
    print("This CSV contains all raw data for analysis:")
    print("  - error_audited, error_unaudited")
    print("  - error_bulk, error_tail")
    print("  - audits_to_bulk, audits_to_tail")
    print("  - allocation ratios, tree complexity")
    
    # Compute summary statistics
    summary = df.groupby('alpha').agg({
        'error_audited': ['mean', 'std'],
        'error_unaudited': ['mean', 'std'],
        'error_bulk': ['mean', 'std'],
        'error_tail': ['mean', 'std'],
        'audits_to_bulk': 'mean',
        'audits_to_tail': 'mean',
        'tree_leaves': 'mean',
    }).round(4)
    
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(summary)
    
    # Compute allocation ratio
    df['allocation_ratio'] = (df['audits_to_tail'] / df['tail_size']) / (df['audits_to_bulk'] / df['bulk_size'])
    
    # Create visualizations
    create_figures(df)
    
    # Print key findings
    print("\n" + "=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    
    print(f"\n1. Error on unaudited > audited:")
    for alpha in alphas:
        subset = df[df['alpha'] == alpha]
        err_aud = subset['error_audited'].mean()
        err_unaud = subset['error_unaudited'].mean()
        print(f"   alpha={alpha:6.3f}: Audited={err_aud:.3f}, Unaudited={err_unaud:.3f}, Delta={err_unaud-err_aud:.3f}")
    
    print(f"\n2. Allocation ratio (tail/bulk) decreases with alpha:")
    for alpha in alphas:
        ratio = df[df['alpha'] == alpha]['allocation_ratio'].mean()
        print(f"   alpha={alpha:6.3f}: Ratio={ratio:.3f}")
    
    print(f"\n3. Tail error increases with alpha:")
    for alpha in alphas:
        tail_err = df[df['alpha'] == alpha]['error_tail'].mean()
        print(f"   alpha={alpha:6.3f}: Tail error={tail_err:.3f}")
    
    print("\n" + "=" * 60)
    print("Experiment complete!")
    print("=" * 60)


def create_figures(df):
    """Create visualization figures."""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Error: Audited vs Unaudited
    ax = axes[0, 0]
    summary = df.groupby('alpha')[['error_audited', 'error_unaudited']].agg(['mean', 'std'])
    alphas = summary.index
    
    ax.errorbar(alphas, summary[('error_audited', 'mean')], 
                yerr=summary[('error_audited', 'std')],
                marker='o', label='Audited', capsize=5)
    ax.errorbar(alphas, summary[('error_unaudited', 'mean')], 
                yerr=summary[('error_unaudited', 'std')],
                marker='s', label='Unaudited', capsize=5)
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Error Rate')
    ax.set_xscale('log')
    ax.set_title('Error: Audited vs Unaudited')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Allocation Ratio
    ax = axes[0, 1]
    summary_ratio = df.groupby('alpha')['allocation_ratio'].agg(['mean', 'std'])
    ax.errorbar(summary_ratio.index, summary_ratio['mean'], 
                yerr=summary_ratio['std'],
                marker='o', color='purple', capsize=5)
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Allocation Ratio (Tail/Bulk)')
    ax.set_xscale('log')
    ax.set_title('Verification Allocation Shifts Away from Tail')
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Equal allocation')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Bulk vs Tail Error
    ax = axes[1, 0]
    summary_err = df.groupby('alpha')[['error_bulk', 'error_tail']].agg(['mean', 'std'])
    ax.errorbar(summary_err.index, summary_err[('error_bulk', 'mean')], 
                yerr=summary_err[('error_bulk', 'std')],
                marker='o', label='Bulk', capsize=5)
    ax.errorbar(summary_err.index, summary_err[('error_tail', 'mean')], 
                yerr=summary_err[('error_tail', 'std')],
                marker='s', label='Tail', capsize=5, color='red')
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Error Rate')
    ax.set_xscale('log')
    ax.set_title('Error Geometry: Bulk down, Tail up')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Tree Complexity
    ax = axes[1, 1]
    summary_leaves = df.groupby('alpha')['tree_leaves'].agg(['mean', 'std'])
    ax.errorbar(summary_leaves.index, summary_leaves['mean'], 
                yerr=summary_leaves['std'],
                marker='o', color='green', capsize=5)
    ax.set_xlabel('Pruning Parameter alpha')
    ax.set_ylabel('Number of Leaves')
    ax.set_xscale('log')
    ax.set_title('Tree Complexity Decreases with alpha')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../manuscript/figures/sparse_parity_audit.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('../manuscript/figures/sparse_parity_audit.png', dpi=300, bbox_inches='tight')
    print("\nFigures saved to manuscript/figures/")
    plt.close()


if __name__ == "__main__":
    main()
