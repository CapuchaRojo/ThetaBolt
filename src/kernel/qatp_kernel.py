import reservoirpy as rpy
from qiskit.circuit.library import ZFeatureMap
from qiskit.primitives import Sampler
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.fidelity import ComputeUncompute
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

        if self.config.use_quantum:
            feature_map = ZFeatureMap(feature_dimension=self.config.units, reps=2)
            sampler = Sampler()
            fidelity = ComputeUncompute(sampler=sampler)
            self.kernel = FidelityQuantumKernel(
                fidelity=fidelity, feature_map=feature_map
            )
        else:
            rpy.set_seed(self.config.seed)
            self.reservoir = Reservoir(
                units=self.config.units, sr=self.config.sr, lr=self.config.lr
            )
            self.readout = Ridge(ridge=self.config.ridge)
            self.esn = self.reservoir >> self.readout

        self.message_bus = MessageBus()
        self.dispatch_agent = DispatchAgent(self.message_bus)
        self.monitor_agent = MonitorAgent(self.message_bus)
        self.swarm = [
            SwarmAgent(self.message_bus) for _ in range(self.config.num_agents)
        ]

    def start_swarm(self):
        for agent in self.swarm:
            agent.start()

    def stop_swarm(self):
        for agent in self.swarm:
            agent.stop()

    def train(self, X_train, y_train, warmup=50):
        if self.config.use_quantum:
            self.qsvc = QSVC(quantum_kernel=self.kernel)
            self.qsvc.fit(X_train, y_train)
        else:
            self.esn.fit(X_train, y_train, warmup=warmup)

    def predict(self, X_test):
        if self.config.use_quantum:
            return self.qsvc.predict(X_test)
        else:
            return self.esn.run(X_test)

    def evaluate(self, y_true, y_pred):
        return rmse(y_true, y_pred)
