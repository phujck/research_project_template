import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

# --- 1. Data Generation ---
def generate_shortcut_data(n, shift=False, corr_train=0.99, corr_shift=0.1):
    z_core = np.random.randint(0, 2, n)
    corr = corr_shift if shift else corr_train
    # Shortcut matches core with probability corr
    z_short = np.where(np.random.random(n) < corr, z_core, 1 - z_core)
    
    # X = [z_core, z_short]
    X = np.stack([z_core, z_short], axis=1)
    y = z_core
    return X, y

def describe_behaviour(clf, alpha):
    """
    Analyses model coefficients to determine feature dominance.
    """
    coef = clf.coef_[0]
    core_w = abs(coef[0])
    short_w = abs(coef[1])
    
    if core_w > 0 and short_w == 0:
        return "Robust (Uses Core Only)"
    elif core_w == 0 and short_w > 0:
        return "Blind (Uses Shortcut Only)"
    elif core_w > 0 and short_w > 0:
        if core_w > short_w:
            return "Mixed (Core Dominant)"
        else:
            return "Mixed (Shortcut Dominant)"
    else:
        return "Collapsed (No Features)"

# --- 2. Simulation ---
def run_shortcut_experiment():
    n_train = 1000
    n_test = 500
    n_bootstrap = 100
    
    Cs = np.logspace(-3, 1, 20)
    alphas = 1.0 / Cs
    
    X_train, y_train = generate_shortcut_data(n_train, shift=False)
    X_test_std, y_test_std = generate_shortcut_data(n_test, shift=False)
    X_test_shift, y_test_shift = generate_shortcut_data(n_test, shift=True)
    
    acc_train = []
    acc_train_ci = []
    acc_shift = []
    acc_shift_ci = []
    behaviours = []
    
    for C in Cs:
        # Scale: z_short is "loud" (1.0), z_core is "quiet" (0.1)
        X_train_scaled = X_train.copy().astype(float)
        X_train_scaled[:, 0] *= 0.1 # Core is expensive/quiet
        X_train_scaled[:, 1] *= 1.0 # Shortcut is cheap/loud
        
        X_test_std_scaled = X_test_std.copy().astype(float)
        X_test_std_scaled[:, 0] *= 0.1
        X_test_std_scaled[:, 1] *= 1.0
        
        X_test_shift_scaled = X_test_shift.copy().astype(float)
        X_test_shift_scaled[:, 0] *= 0.1
        X_test_shift_scaled[:, 1] *= 1.0

        clf = LogisticRegression(penalty='l1', C=C, solver='liblinear')
        clf.fit(X_train_scaled, y_train)
        
        # Bootstrap for Confidence Intervals
        def get_acc_ci(X, y_true):
            boot_accs = []
            y_pred_all = clf.predict(X)
            for _ in range(n_bootstrap):
                idx = np.random.choice(len(y_true), size=len(y_true), replace=True)
                boot_accs.append(accuracy_score(y_true[idx], y_pred_all[idx]))
            return np.mean(boot_accs), np.percentile(boot_accs, [5, 95])

        mean_t, ci_t = get_acc_ci(X_test_std_scaled, y_test_std)
        mean_s, ci_s = get_acc_ci(X_test_shift_scaled, y_test_shift)
        
        acc_train.append(mean_t)
        acc_train_ci.append(ci_t.tolist())
        acc_shift.append(mean_s)
        acc_shift_ci.append(ci_s.tolist())
        
        behaviour = describe_behaviour(clf, 1.0/C)
        behaviours.append(behaviour)
        
        print(f"Alpha: {1.0/C:7.2f} | Train: {acc_train[-1]:.3f} | Shift: {acc_shift[-1]:.3f} | Behaviour: {behaviour}")
        
    # --- 4. Plotting ---
    plt.figure(figsize=(10, 6))
    
    t_lo = [r[0] for r in acc_train_ci]
    t_hi = [r[1] for r in acc_train_ci]
    s_lo = [r[0] for r in acc_shift_ci]
    s_hi = [r[1] for r in acc_shift_ci]
    
    plt.plot(alphas, acc_train, 'b-o', label='Accuracy ($D_{train}$)')
    plt.fill_between(alphas, t_lo, t_hi, color='b', alpha=0.1)
    
    plt.plot(alphas, acc_shift, 'r-s', label='Accuracy ($D_{shift}$)')
    plt.fill_between(alphas, s_lo, s_hi, color='r', alpha=0.1)
    
    plt.xscale('log')
    plt.xlabel('Compressive Pressure ($\\alpha$)')
    plt.ylabel('Accuracy')
    plt.title('Statistical Fragility in Shortcut Selection')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = "simulation/runs/shortcut_fragility.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    # Also save to manuscript figures
    fig_path = os.path.join("manuscript", "figures", "shortcut_fragility.pdf")
    os.makedirs(os.path.dirname(fig_path), exist_ok=True)
    plt.savefig(fig_path)
    print(f"Plot saved to {output_path} and {fig_path}")

if __name__ == "__main__":
    run_shortcut_experiment()
