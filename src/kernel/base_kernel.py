from abc import ABC, abstractmethod
from typing import Any


class BaseKernel(ABC):
    """Abstract base class for all kernel implementations.

    This class defines the interface for kernel models, ensuring that all kernel
    implementations provide `train` and `predict` methods.
    """

    @abstractmethod
    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        """Trains the kernel model.

        Args:
            X_train: The training data.
            y_train: The training labels.
            **kwargs: Additional keyword arguments for training.
        """
        pass

    @abstractmethod
    def predict(self, X_test: Any) -> Any:
        """Makes predictions using the trained model.

        Args:
            X_test: The input data for prediction.

        Returns:
            The predicted output.
        """
        pass
