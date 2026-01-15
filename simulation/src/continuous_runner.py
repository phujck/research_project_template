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
    print("Generating Runge Cliff Data...")
    X, y = generate_data(n_samples=300)
    
    # Define degrees of complexity (Obviousness = 1/degree)
    degrees = [1, 2, 5, 10, 15, 20, 30]
    
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
        
        mse_base = mean_squared_error(y_base, pred_base)
        mse_exc = mean_squared_error(y_exc, pred_exc)
        
        obviousness = 1.0 / d
        results.append({
            'degree': d,
            'obviousness': obviousness,
            'mse_base': mse_base,
            'mse_exc': mse_exc
        })
        
        # Plotting fit
        # Only plot a few distinct ones for clarity
        if d in [1, 5, 15, 30]:
            label = f"Doc={d} (O={obviousness:.2f})"
            plt.plot(X, y_pred, color=colors[i], linewidth=2, label=label)

    plt.title("The Runge Cliff: Polynomial Fits")
    plt.legend()
    plt.xlabel("Input Space (x)")
    plt.ylabel("Target (y)")
    plt.ylim(-2, 12) # Focus on the spike
    plt.savefig(os.path.join(OUTPUT_DIR, "runge_fits.pdf"))
    print("Saved fit plot.")
    
    # --- Plot Fragility Curve ---
    plt.figure(figsize=(8, 6))
    
    degs = [r['degree'] for r in results]
    obvs = [r['obviousness'] for r in results]
    u_base = [r['mse_base'] for r in results]
    u_exc = [r['mse_exc'] for r in results]
    
    # Plotting against Obviousness (1/d)
    # We want X-axis to be Obviousness
    
    plt.plot(obvs, u_exc, 'r-o', linewidth=3, label='Error on Anomaly (Fragility)')
    plt.plot(obvs, u_base, 'b--o', linewidth=2, label='Error on Base Case')
    
    plt.xlabel('Obviousness (1 / Degree)')
    plt.ylabel('Mean Squared Error')
    plt.title('The Continuous Fragility Curve')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_xaxis() # Low degree (high obviousness) on right? 
    # Wait, Obviousness = 1/d. 
    # High d (Complexity) -> Low Obviousness -> Left.
    # Low d (Simple) -> High Obviousness -> Right.
    # So if we plot x=Obviousness, 0 is Left, 1 is Right.
    # We want to show High Obviousness -> High Fragility.
    
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
