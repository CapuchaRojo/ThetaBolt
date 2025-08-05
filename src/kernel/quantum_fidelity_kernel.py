from typing import Any

from qiskit.algorithms.state_fidelities import ComputeUncompute
from qiskit.circuit.library import ZFeatureMap
from qiskit.primitives import Sampler
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels import FidelityQuantumKernel

from .base_kernel import BaseKernel


class QuantumFidelityKernel(BaseKernel):
    """Quantum Fidelity Kernel implementation.

    This class implements a quantum kernel using Qiskit's FidelityQuantumKernel.
    It is designed to be used for tasks where quantum advantage might be beneficial.
    """

    def __init__(self, config: Any) -> None:
        """Initializes the QuantumFidelityKernel.

        Args:
            config: The configuration object containing parameters for the kernel.
        """
        self.config = config
        feature_map = ZFeatureMap(feature_dimension=self.config.units, reps=2)
        sampler = Sampler()
        fidelity = ComputeUncompute(sampler=sampler)
        self.kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)
        self.model = QSVC(quantum_kernel=self.kernel)

    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        """Trains the quantum kernel model.

        Args:
            X_train: The training data.
            y_train: The training labels.
            **kwargs: Additional keyword arguments for training.
        """
        print(f"Training with Quantum Kernel for data size: {len(X_train)}")
        self.model.fit(X_train, y_train)

    def predict(self, X_test: Any) -> Any:
        """Makes predictions using the trained quantum kernel model.

        Args:
            X_test: The input data for prediction.

        Returns:
            The predicted output.
        """
        return self.model.predict(X_test)