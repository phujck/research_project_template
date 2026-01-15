import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import datetime
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def generate_data(n_samples, n_bits, exception_prob=0.01):
    """
    Generates Sparse Parity data with a Black Swan exception.
    Rule: y = x[0] XOR x[1]
    Exception: If x[N-1] == 1, flip y.
    """
    X = np.random.randint(0, 2, size=(n_samples, n_bits))
    
    # Base Rule: Logical AND of first two bits (Learnable by Greedy Trees)
    y = np.logical_and(X[:, 0], X[:, 1]).astype(int)
    
    # Exception Rule: If last bit is 1, flip the label
    # We force the last bit to be 1 with probability 'exception_prob' 
    # But for a random uniform distribution, P(x[N-1]=1) is 0.5.
    # To mimic a "Black Swan", we should maybe resample X to make x[N-1]=1 rare?
    # OR, we just define the rule based on whatever x[N-1] is.
    # Let'sstick to the formal definition: The rule *is* the rule.
    # But if we want x[N-1] to be rare in Training, we must bias sampling.
    
    # Bias the training data so x[N-1] is almost always 0
    mask_rare = np.random.random(n_samples) < exception_prob
    X[:, -1] = 0 # Default to 0
    X[mask_rare, -1] = 1 # Inject rare events
    
    # Apply Exception
    exception_mask = X[:, -1] == 1
    y[exception_mask] = 1 - y[exception_mask]
    
    return X, y

def measure_obviousness(model, n_bits, depth):
    """
    Obviousness = 1 / Cost.
    Here, Cost is limited by Max Depth.
    O = 10.0 / Depth (Normalized for readability)
    """
    return 10.0 / float(depth)

def run_experiment(config):
    # Setup Output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join("simulation", "runs", f"{timestamp}_SparseParity")
    os.makedirs(run_dir, exist_ok=True)
    
    with open(os.path.join(run_dir, "config.json"), 'w') as f:
        json.dump(vars(config), f, indent=4)

    # 1. Data Generation
    print("Generating Data...")
    # Oversample the exception to ensure it's learnable (Reasonable Curiosity)
    # If the event is too rare (0.005), even a deep tree won't statistically justify the split.
    X_train, y_train = generate_data(config.n_train, config.n_bits, exception_prob=0.1)
    
    # Test set reflects Reality: Rare Black Swans
    X_test, y_test = generate_data(config.n_test, config.n_bits, exception_prob=0.01) 

    # 2. Train Models with varying "Obviousness" (Regularization Strength ccp_alpha)
    # Alpha acts as a "tax" on complexity. 
    # We sweep alpha values and average over N_TRIALS to get a smooth thermodynamic curve.
    alphas = np.linspace(0.0, 0.1, 50)
    n_trials = 20 # Ensemble size for smoothing
    
    results = []
    
    print(f"Running Ensemble Simulation ({n_trials} trials per alpha)...")
    
    for alpha in alphas:
        # Accumulators for this alpha
        err_std_sum = 0.0
        err_exc_sum = 0.0
        
        for i in range(n_trials):
            # Resample Training Data for diversity
            X_train, y_train = generate_data(config.n_train, config.n_bits, exception_prob=0.1)
            
            clf = DecisionTreeClassifier(ccp_alpha=alpha, random_state=i) # Vary seed
            clf.fit(X_train, y_train)
            
            # Metrics
            y_pred_std = clf.predict(X_test[X_test[:, -1] == 0])
            y_pred_exc = clf.predict(X_test[X_test[:, -1] == 1])
            
            # Error Rates
            mask_std = X_test[:, -1] == 0
            mask_exc = X_test[:, -1] == 1
            
            err_std_sum += (1.0 - accuracy_score(y_test[mask_std], y_pred_std))
            err_exc_sum += (1.0 - accuracy_score(y_test[mask_exc], y_pred_exc))
        
        # Average
        results.append({
            "alpha": alpha,
            "obviousness": alpha * 1000, 
            "error_std": err_std_sum / n_trials,
            "error_exc": err_exc_sum / n_trials,
            "n_leaves": 0, # Placeholder
            "depth": 0 # Placeholder
        })

    # Save Results
    with open(os.path.join(run_dir, "results.json"), 'w') as f:
        json.dump(results, f, indent=4, cls=NumpyEncoder)
        
    # 3. Plotting
    obv_vals = [r['obviousness'] for r in results]
    err_exc = [r['error_exc'] for r in results]
    
    plt.figure(figsize=(8, 6))
    plt.plot(obv_vals, err_exc, marker='o', linestyle='-', color='r')
    plt.xlabel("Obviousness (Cost-Complexity Penalty $\\alpha$)")
    plt.ylabel("Error Rate on Exceptions (F)")
    plt.title("H3: The Fragility of Obviousness (Continuum)")
    plt.grid(True)
    plt.ylim(-0.02, 0.55)
    
    plot_path = os.path.join(run_dir, "fragility_curve.pdf")
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_bits", type=int, default=20)
    parser.add_argument("--n_train", type=int, default=2000)
    parser.add_argument("--n_test", type=int, default=1000)
    parser.add_argument("--exception_prob", type=float, default=0.005, help="Rarity of Black Swan in training")
    args = parser.parse_args()
    
    run_experiment(args)
