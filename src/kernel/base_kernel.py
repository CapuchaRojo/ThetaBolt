from abc import ABC, abstractmethod
from typing import Any


class BaseKernel(ABC):
    """Abstract base class for all kernel implementations."""

    @abstractmethod
    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        """Train the kernel model."""
        pass

    @abstractmethod
    def predict(self, X_test: Any) -> Any:
        """Make predictions using the trained model."""
        pass
