import reservoirpy as rpy
from qiskit.circuit.library import ZFeatureMap
from qiskit.primitives import Sampler
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from reservoirpy.nodes import Reservoir, Ridge
from reservoirpy.observables import rmse

from ..agents.dispatch_agent import DispatchAgent
from ..agents.message_bus import MessageBus
from ..agents.monitor_agent import MonitorAgent
from ..agents.swarm_agent import SwarmAgent
from .config_loader import load_config


class QATPKernel:
    def __init__(self, config=None):
        self.config = config or load_config()
        self.model = None  # Will hold either QSVC or ESN

        self.message_bus = MessageBus()
        self.dispatch_agent = DispatchAgent(self.message_bus)
        self.monitor_agent = MonitorAgent(self.message_bus)
        self.swarm = [
            SwarmAgent(self.message_bus) for _ in range(self.config.num_agents)
        ]

    def start_swarm(self):
        self.dispatch_agent.start()
        for agent in self.swarm:
            agent.start()

    def stop_swarm(self):
        for agent in self.swarm:
            agent.stop()

    def train(self, X_train, y_train, warmup=50):
        use_quantum_kernel = (
            self.config.use_quantum and len(X_train) <= self.config.quantum_threshold
        )

        if use_quantum_kernel:
            print(f"Training with Quantum Kernel for data size: {len(X_train)}")
            feature_map = ZFeatureMap(feature_dimension=self.config.units, reps=2)
            sampler = Sampler()
            fidelity = ComputeUncompute(sampler=sampler)
            kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)
            self.model = QSVC(quantum_kernel=kernel)
            self.model.fit(X_train, y_train)
        else:
            print(f"Training with Classical Reservoir for data size: {len(X_train)}")
            rpy.set_seed(self.config.seed)
            reservoir = Reservoir(
                units=self.config.units, sr=self.config.sr, lr=self.config.lr
            )
            readout = Ridge(ridge=self.config.ridge)
            self.model = reservoir >> readout
            # Adjust warmup to be appropriate for the dataset size
            adjusted_warmup = min(warmup, len(X_train) - 1) if len(X_train) > 1 else 0
            self.model.fit(X_train, y_train, warmup=adjusted_warmup)

    def predict(self, X_test):
        if self.model is None:
            raise RuntimeError(
                "Model has not been trained yet. Please call train() first."
            )
        # The prediction method is different for the two models
        if isinstance(self.model, QSVC):
            return self.model.predict(X_test)
        else:
            return self.model.run(X_test)

    def evaluate(self, y_true, y_pred):
        return rmse(y_true, y_pred)
