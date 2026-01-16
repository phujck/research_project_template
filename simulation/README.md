# Simulation Documentation: The Geometry of Rational Blindness

This directory contains the empirical core of the project, instantiating the theory of Rational Blindness across discrete and continuous domains.

## 1. Sparse Parity (`src/main.py`)
- **Objective**: Demonstrate that as compression pressure ($\alpha$) increases, agents rationally divest from rare tail events.
- **Parameters**: 20 bits, $p_{exc} = 0.01$, CART pruning.
- **Statistical Methology**: $N=100$ bootstrap iterations.
- **Paper Link**: This simulation generates **Figure 1: The Error Geometry**.

## 2. Runge's Boundary Divergence (`src/continuous_runner.py`)
- **Objective**: Show the "representational double-bind" in continuous domains.
- **Parameters**: Polynomial regression with degree $d$ sweep. Gaussian spike at $x=0.98$.
- **Statistical Methology**: $N=100$ bootstrap MSE calculation.
- **Paper Link**: This simulation generates **Figure 2: Runge's Boundary Divergence**.

## 3. Shortcut Selection (`src/shortcut_learning.py`)
- **Objective**: Isolate the three behavioural regimes (Robust, Blind, Collapsed) under distribution shift.
- **Regimes**:
    - **Robust**: Prioritises invariant features ($Acc \approx 100\%$).
    - **Blind**: Follows fluent shortcuts, failing on OOD shift ($Acc \approx 8\%$).
    - **Collapsed**: Prunes all features under extreme pressure ($Acc \approx 50\%$).
- **Paper Link**: This simulation generates **Figure 3: The Shortcut Trap**.

## Running Simulations
Use the top-level management script:
```powershell
./manage.ps1 sim             # Run Sparse Parity
./manage.ps1 sim-continuous  # Run Runge's Boundary Divergence
```
For Shortcut Selection, run directly:
```powershell
py simulation/src/shortcut_learning.py
```
