from typing import Any

import reservoirpy as rpy
from reservoirpy.nodes import Reservoir, Ridge

from .base_kernel import BaseKernel


class ReservoirKernel(BaseKernel):
    """Classical Reservoir Computing kernel."""

    def __init__(self, config: Any) -> None:
        self.config = config
        rpy.set_seed(self.config.seed)
        self.reservoir = Reservoir(
            units=self.config.units, sr=self.config.sr, lr=self.config.lr
        )
        self.readout = Ridge(ridge=self.config.ridge)
        self.model = self.reservoir >> self.readout

    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        warmup: int = kwargs.get("warmup", 50)
        print(f"Training with Classical Reservoir for data size: {len(X_train)}")
        self.model.fit(X_train, y_train, warmup=warmup)

    def predict(self, X_test: Any) -> Any:
        return self.model.run(X_test)
