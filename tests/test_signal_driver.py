from src.agents.signal_driver import read_environment


def test_env_signal() -> None:
    """Tests the read_environment function.

    This test verifies that the read_environment function returns a list.
    """
    data = read_environment()
    assert isinstance(data, list)
