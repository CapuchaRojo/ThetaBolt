import numpy as np
from reservoirpy.datasets import mackey_glass, to_forecasting
from reservoirpy.hyper import plot_hyperopt_report, research
from reservoirpy.nodes import Reservoir, Ridge
from reservoirpy.observables import nrmse, rsquare


def objective(dataset, config, *, units, sr, lr, ridge, seed):
    x_train, x_test, y_train, y_test = dataset
    seed_value = seed
    losses, r2s = [], []

    for _ in range(config.get("instances_per_trial", 3)):
        reservoir = Reservoir(units=units, sr=sr, lr=lr, seed=seed_value)
        readout = Ridge(ridge=ridge)
        model = reservoir >> readout
        y_pred = model.fit(x_train, y_train).run(x_test)
        losses.append(nrmse(y_test, y_pred, norm_value=np.ptp(x_train)))
        r2s.append(rsquare(y_test, y_pred))
        seed_value += 1

    return {"loss": float(np.mean(losses)), "r2": float(np.mean(r2s))}


# Prepare dataset
X = mackey_glass(n_timesteps=2000)
x_train, x_test, y_train, y_test = to_forecasting(X, test_size=0.2)
dataset = (x_train, x_test, y_train, y_test)

# Run search
exp, trials = research(objective, dataset)

# Visualize performance
plot_hyperopt_report(exp, trials)
