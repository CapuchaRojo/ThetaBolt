import numpy as np
from qiskit_machine_learning.algorithms import QSVC

from src.kernel.config_loader import load_config
from src.kernel.qatp_kernel import QATPKernel


def test_dynamic_kernel_selection():
    # Load the configuration
    config = load_config([])
    config.use_quantum = True  # Enable quantum pathway

    # --- Test 1: Small dataset should use Quantum Kernel ---
    X_train_small = np.sin(np.linspace(0, 10, 50)).reshape(-1, 1)
    y_train_small = (np.cos(np.linspace(0, 10, 50)) > 0).astype(int)
    X_test_small = np.sin(np.linspace(10, 12, 10)).reshape(-1, 1)

    quantum_kernel = QATPKernel(config=config)
    quantum_kernel.train(X_train_small, y_train_small)
    # Verify that the model trained is indeed the quantum one
    assert isinstance(quantum_kernel.model, QSVC)
    predictions = quantum_kernel.predict(X_test_small)
    assert predictions is not None

    # --- Test 2: Large dataset should fall back to Classical Reservoir ---
    X_train_large = np.sin(np.linspace(0, 20, 200)).reshape(-1, 1)
    y_train_large = np.cos(np.linspace(0, 20, 200)).reshape(
        -1, 1
    )  # Continuous for reservoir
    X_test_large = np.sin(np.linspace(20, 22, 20)).reshape(-1, 1)

    classical_fallback_kernel = QATPKernel(config=config)
    classical_fallback_kernel.train(X_train_large, y_train_large)
    # Verify that the model trained is the classical one
    from reservoirpy.model import Model

    assert isinstance(classical_fallback_kernel.model, Model)
    predictions = classical_fallback_kernel.predict(X_test_large)
    assert predictions is not None


def test_swarm_functionality():
    # Load the configuration
    config = load_config([])

    # Initialize the kernel (either classical or quantum)
    kernel = QATPKernel(config=config)

    # Test swarm start and stop
    kernel.start_swarm()
    # Add assertions to check if the swarm has started correctly
    # For example, check if agents are running
    kernel.stop_swarm()
    # Add assertions to check if the swarm has stopped correctly
    # For example, check if agents are no longer running
