from typing import Any

import reservoirpy as rpy
from reservoirpy.nodes import Reservoir, Ridge

from .base_kernel import BaseKernel


class ReservoirKernel(BaseKernel):
    """Classical Reservoir Computing kernel implementation.

    This class implements a classical reservoir computing kernel using the
    `reservoirpy` library. It is used as a fallback when quantum computation is
    not feasible or required.
    """

    def __init__(self, config: Any) -> None:
        """Initializes the ReservoirKernel.

        Args:
            config: The configuration object containing parameters for the kernel.
        """
        self.config = config
        rpy.set_seed(self.config.seed)
        self.reservoir = Reservoir(
            units=self.config.units, sr=self.config.sr, lr=self.config.lr
        )
        self.readout = Ridge(ridge=self.config.ridge)
        self.model = self.reservoir >> self.readout

    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        """Trains the classical reservoir kernel model.

        Args:
            X_train: The training data.
            y_train: The training labels.
            **kwargs: Additional keyword arguments for training, including 'warmup'.
        """
        warmup: int = kwargs.get("warmup", 50)
        print(f"Training with Classical Reservoir for data size: {len(X_train)}")
        self.model.fit(X_train, y_train, warmup=warmup)

    def predict(self, X_test: Any) -> Any:
        """Makes predictions using the trained classical reservoir kernel model.

        Args:
            X_test: The input data for prediction.

        Returns:
            The predicted output.
        """
        return self.model.run(X_test)
