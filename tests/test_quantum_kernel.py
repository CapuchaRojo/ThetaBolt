import numpy as np

from src.kernel.config_loader import load_config
from src.kernel.qatp_kernel import QATPKernel


def test_quantum_vs_classical_kernel():
    # Load the configuration
    config = load_config()

    # Generate synthetic data
    t = np.linspace(0, 10, 100)
    X_train = np.sin(t).reshape(-1, 1)
    y_train = np.cos(t).reshape(-1, 1)
    X_test = np.sin(np.linspace(10, 12, 20)).reshape(-1, 1)

    # Test classical kernel
    config.use_quantum = False
    classical_kernel = QATPKernel(config=config)
    classical_kernel.train(X_train, y_train)
    classical_predictions = classical_kernel.predict(X_test)
    assert classical_predictions is not None

    # Test quantum kernel
    config.use_quantum = True
    quantum_kernel = QATPKernel(config=config)
    quantum_kernel.train(X_train, y_train)
    quantum_predictions = quantum_kernel.predict(X_test)
    assert quantum_predictions is not None


def test_swarm_functionality():
    # Load the configuration
    config = load_config()

    # Initialize the kernel (either classical or quantum)
    kernel = QATPKernel(config=config)

    # Test swarm start and stop
    kernel.start_swarm()
    # Add assertions to check if the swarm has started correctly
    # For example, check if agents are running
    kernel.stop_swarm()
    # Add assertions to check if the swarm has stopped correctly
    # For example, check if agents are no longer running
