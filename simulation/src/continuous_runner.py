import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import os

# Configuration
OUTPUT_DIR = "../figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_data(n_samples=200):
    """
    Generates data for the "Runge Cliff" scenario.
    Domain: [0, 1]
    Base Rule: y = x (Linear)
    Anomaly: Sharp Gaussian spike at x=0.98
    """
    X = np.sort(np.random.rand(n_samples, 1), axis=0)
    
    # Base Rule
    y = X.copy()
    
    # The "Cliff" / Anomaly
    # A sharp spike centered at 0.98
    spike = 10.0 * np.exp(-5000 * (X - 0.98)**2)
    y += spike
    
    return X, y

def get_partitions(X, y):
    """
    Splits data into 'Normal' (Base) and 'Exception' (Cliff) regions.
    Normal: x < 0.95
    Exception: x >= 0.95
    """
    mask_normal = X.flatten() < 0.95
    mask_exception = X.flatten() >= 0.95
    
    return (X[mask_normal], y[mask_normal]), (X[mask_exception], y[mask_exception])

def run_experiment():
    print("Generating Runge's Boundary Divergence Data...")
    X, y = generate_data(n_samples=300)
    
    # Define degrees of complexity (Obviousness = 1/degree)
    degrees = [1, 2, 5, 10, 15, 20, 30]
    n_bootstrap = 100
    
    results = []
    
    plt.figure(figsize=(12, 6))
    plt.scatter(X, y, color='black', s=5, alpha=0.3, label='Data')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(degrees)))
    
    for i, d in enumerate(degrees):
        print(f"Training Polynomial Regressor (Degree={d})...")
        
        # Create Pipeline
        # We use a small ridge penalty to prevent absolute explosion for high degrees,
        # but keep it small enough to allow overfitting if the model wants to.
        model = make_pipeline(PolynomialFeatures(d), Ridge(alpha=1e-5))
        model.fit(X, y)
        
        y_pred = model.predict(X)
        
        # Partition Errors
        (X_base, y_base), (X_exc, y_exc) = get_partitions(X, y)
        
        # Predict on partitions
        pred_base = model.predict(X_base)
        pred_exc = model.predict(X_exc)
        
        # Bootstrap for Confidence Intervals
        def get_mse_ci(y_true, y_pred):
            boot_mses = []
            for _ in range(n_bootstrap):
                idx = np.random.choice(len(y_true), size=len(y_true), replace=True)
                boot_mses.append(mean_squared_error(y_true[idx], y_pred[idx]))
            return np.mean(boot_mses), np.percentile(boot_mses, [5, 95])

        mse_base, ci_base = get_mse_ci(y_base, pred_base)
        mse_exc, ci_exc = get_mse_ci(y_exc, pred_exc)
        
        obviousness = 1.0 / d
        results.append({
            'degree': d,
            'obviousness': obviousness,
            'mse_base': mse_base,
            'mse_base_ci': ci_base.tolist(),
            'mse_exc': mse_exc,
            'mse_exc_ci': ci_exc.tolist()
        })
        
        # Plotting fit
        # Only plot a few distinct ones for clarity
        if d in [1, 5, 15, 30]:
            label = f"Degree={d} (O={obviousness:.2f})"
            plt.plot(X, y_pred, color=colors[i], linewidth=2, label=label)

    plt.title("Runge's Boundary Divergence: Polynomial Fits")
    plt.legend()
    plt.xlabel("Input Space (x)")
    plt.ylabel("Target (y)")
    plt.ylim(-2, 12) # Focus on the spike
    plt.savefig(os.path.join(OUTPUT_DIR, "runge_fits.pdf"))
    print("Saved fit plot.")
    
    # --- Plot Fragility Curve ---
    plt.figure(figsize=(8, 6))
    
    obvs = [r['obviousness'] for r in results]
    u_exc = [r['mse_exc'] for r in results]
    u_exc_lo = [r['mse_exc_ci'][0] for r in results]
    u_exc_hi = [r['mse_exc_ci'][1] for r in results]
    
    u_base = [r['mse_base'] for r in results]
    
    # Plotting against Obviousness (1/d)
    # We want X-axis to be Obviousness
    
    plt.plot(obvs, u_exc, 'r-o', linewidth=3, label='Fragility (F) on Anomaly')
    plt.fill_between(obvs, u_exc_lo, u_exc_hi, color='r', alpha=0.2, label='90% CI')
    plt.plot(obvs, u_base, 'b--o', linewidth=2, label='Base Error')
    
    plt.xlabel('Representational Fluency (1 / Degree)')
    plt.ylabel('Mean Squared Error')
    plt.title("Statistical Fragility (Runge's Boundary Divergence)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(OUTPUT_DIR, "continuous_fragility.pdf"))
    print("Saved fragility curve.")
    
    # Print Results Table
    print("\n### Simulation Results: The Runge Cliff")
    print("| Degree ($d$) | Obviousness ($1/d$) | MSE (Base) | MSE (Cliff) | Status |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    for r in results:
        status = "Blind" if r['mse_exc'] > 1.0 else "Robust"
        status = "Overfit" if r['mse_base'] > 0.1 and r['mse_exc'] < 1.0 else status
        print(f"| {r['degree']} | {r['obviousness']:.3f} | {r['mse_base']:.4f} | {r['mse_exc']:.4f} | {status} |")
    print("\n")

if __name__ == "__main__":
    run_experiment()
