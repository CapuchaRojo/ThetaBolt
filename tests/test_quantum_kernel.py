import numpy as np

from src.kernel.config_loader import load_config
from core.controller import Controller
from src.kernel.quantum_fidelity_kernel import QuantumFidelityKernel
from src.kernel.reservoir_kernel import ReservoirKernel


def test_dynamic_kernel_selection() -> None:
    """Tests the dynamic kernel selection logic of the Controller.

    This test verifies that the Controller correctly selects between the Quantum
    Kernel and the Classical Reservoir based on the dataset size and configuration.
    """
    # Load the configuration
    config = load_config([])
    config.use_quantum = True  # Enable quantum pathway

    # --- Test 1: Small dataset should use Quantum Kernel ---
    X_train_small = np.sin(np.linspace(0, 10, 50)).reshape(-1, 1)
    y_train_small = (np.cos(np.linspace(0, 10, 50)) > 0).astype(int)
    X_test_small = np.sin(np.linspace(10, 12, 10)).reshape(-1, 1)

    controller_q = Controller(config=config)
    controller_q.train(X_train_small, y_train_small)
    # Verify that the selected kernel is the quantum one
    assert isinstance(controller_q.kernel, QuantumFidelityKernel)
    predictions = controller_q.predict(X_test_small)
    assert predictions is not None

    # --- Test 2: Large dataset should fall back to Classical Reservoir ---
    X_train_large = np.sin(np.linspace(0, 20, 200)).reshape(-1, 1)
    y_train_large = np.cos(np.linspace(0, 20, 200)).reshape(
        -1, 1
    )  # Continuous for reservoir
    X_test_large = np.sin(np.linspace(20, 22, 20)).reshape(-1, 1)

    controller_c = Controller(config=config)
    controller_c.train(X_train_large, y_train_large)
    # Verify that the selected kernel is the classical one
    assert isinstance(controller_c.kernel, ReservoirKernel)
    predictions = controller_c.predict(X_test_large)
    assert predictions is not None


def test_swarm_functionality() -> None:
    """Tests the swarm functionality of the Controller.

    This test verifies that the Controller can start and stop the agent swarm.
    """
    # Load the configuration
    config = load_config([])

    # Initialize the controller
    controller = Controller(config=config)

    # Test swarm start and stop
    controller.start_swarm()
    # Add assertions to check if the swarm has started correctly
    # For example, check if agents are running
    controller.stop_swarm()
    # Add assertions to check if the swarm has stopped correctly
    # For example, check if agents are no longer running
