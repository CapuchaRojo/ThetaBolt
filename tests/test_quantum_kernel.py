import numpy as np

from src.kernel.config_loader import load_config
from src.kernel.kernel_manager import KernelManager
from src.kernel.quantum_fidelity_kernel import QuantumFidelityKernel
from src.kernel.reservoir_kernel import ReservoirKernel


def test_dynamic_kernel_selection() -> None:
    # Load the configuration
    config = load_config([])
    config.use_quantum = True  # Enable quantum pathway

    # --- Test 1: Small dataset should use Quantum Kernel ---
    X_train_small = np.sin(np.linspace(0, 10, 50)).reshape(-1, 1)
    y_train_small = (np.cos(np.linspace(0, 10, 50)) > 0).astype(int)
    X_test_small = np.sin(np.linspace(10, 12, 10)).reshape(-1, 1)

    kernel_manager_q = KernelManager(config=config)
    kernel_manager_q.train(X_train_small, y_train_small)
    # Verify that the selected kernel is the quantum one
    assert isinstance(kernel_manager_q.kernel, QuantumFidelityKernel)
    predictions = kernel_manager_q.predict(X_test_small)
    assert predictions is not None

    # --- Test 2: Large dataset should fall back to Classical Reservoir ---
    X_train_large = np.sin(np.linspace(0, 20, 200)).reshape(-1, 1)
    y_train_large = np.cos(np.linspace(0, 20, 200)).reshape(
        -1, 1
    )  # Continuous for reservoir
    X_test_large = np.sin(np.linspace(20, 22, 20)).reshape(-1, 1)

    kernel_manager_c = KernelManager(config=config)
    kernel_manager_c.train(X_train_large, y_train_large)
    # Verify that the selected kernel is the classical one
    assert isinstance(kernel_manager_c.kernel, ReservoirKernel)
    predictions = kernel_manager_c.predict(X_test_large)
    assert predictions is not None


def test_swarm_functionality() -> None:
    # Load the configuration
    config = load_config([])

    # Initialize the kernel manager
    kernel_manager = KernelManager(config=config)

    # Test swarm start and stop
    kernel_manager.start_swarm()
    # Add assertions to check if the swarm has started correctly
    # For example, check if agents are running
    kernel_manager.stop_swarm()
    # Add assertions to check if the swarm has stopped correctly
    # For example, check if agents are no longer running
