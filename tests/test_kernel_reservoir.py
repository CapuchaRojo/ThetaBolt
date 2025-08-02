import json
import os

import numpy as np
from jsonargparse import ArgumentParser

from src.kernel.qatp_kernel import QATPKernel


def test_reservoir_esn_learning():
    config = {
        "units": 50,
        "sr": 0.9,
        "lr": 0.3,
        "ridge": 1e-4,
        "seed": 42,
        "num_agents": 10,
    }
    with open("test_config.json", "w") as f:
        json.dump(config, f)

    parser = ArgumentParser()
    parser.add_argument("--config", action="config")
    parser.add_argument("--units", type=int)
    parser.add_argument("--sr", type=float)
    parser.add_argument("--lr", type=float)
    parser.add_argument("--ridge", type=float)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_agents", type=int, default=10)
    parser.add_argument("--use_quantum", type=bool, default=False)
    config = parser.parse_args(["--config", "test_config.json"])

    t = np.linspace(0, 10, 500)
    X = np.sin(t).reshape(-1, 1)
    y = np.cos(t).reshape(-1, 1)

    split = int(0.8 * len(t))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    kernel = QATPKernel(config=config)

    kernel.train(X_train, y_train, warmup=20)

    y_pred = kernel.predict(X_test)

    error = kernel.evaluate(y_test, y_pred)

    os.remove("test_config.json")

    assert error < 0.15
