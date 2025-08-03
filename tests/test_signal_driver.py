from src.agents.signal_driver import read_environment


def test_env_signal() -> None:
    data = read_environment()
    assert isinstance(data, list)
