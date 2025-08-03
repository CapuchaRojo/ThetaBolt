from typing import Any

from qiskit.algorithms.state_fidelities import ComputeUncompute
from qiskit.circuit.library import ZFeatureMap
from qiskit.primitives import Sampler
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels import FidelityQuantumKernel

from .base_kernel import BaseKernel


class QuantumFidelityKernel(BaseKernel):
    """Quantum Fidelity Kernel implementation."""

    def __init__(self, config: Any) -> None:
        self.config = config
        feature_map = ZFeatureMap(feature_dimension=self.config.units, reps=2)
        sampler = Sampler()
        fidelity = ComputeUncompute(sampler=sampler)
        self.kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)
        self.model = QSVC(quantum_kernel=self.kernel)

    def train(self, X_train: Any, y_train: Any, **kwargs: Any) -> None:
        print(f"Training with Quantum Kernel for data size: {len(X_train)}")
        self.model.fit(X_train, y_train)

    def predict(self, X_test: Any) -> Any:
        return self.model.predict(X_test)
