import reservoirpy as rpy
from reservoirpy.nodes import Reservoir, Ridge
from reservoirpy.observables import rmse

from ..agents.dispatch_agent import DispatchAgent
from ..agents.message_bus import MessageBus
from ..agents.monitor_agent import MonitorAgent
from ..agents.swarm_agent import SwarmAgent
from .config_loader import load_config


class QATPKernel:
    def __init__(self, config=None):
        config = config or load_config()

        rpy.set_seed(config.seed)

        self.reservoir = Reservoir(units=config.units, sr=config.sr, lr=config.lr)
        self.readout = Ridge(ridge=config.ridge)
        self.esn = self.reservoir >> self.readout

        self.message_bus = MessageBus()
        self.dispatch_agent = DispatchAgent(self.message_bus)
        self.monitor_agent = MonitorAgent(self.message_bus)
        self.swarm = [SwarmAgent(self.message_bus) for _ in range(config.num_agents)]

    def start_swarm(self):
        for agent in self.swarm:
            agent.start()

    def stop_swarm(self):
        for agent in self.swarm:
            agent.stop()

    def train(self, X_train, y_train, warmup=50):
        self.esn.fit(X_train, y_train, warmup=warmup)

    def predict(self, X_test):
        return self.esn.run(X_test)

    def evaluate(self, y_true, y_pred):
        return rmse(y_true, y_pred)
