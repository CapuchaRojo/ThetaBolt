from src.agents.signal_driver import read_environment


def test_env_signal():
    data = read_environment()
    assert isinstance(data, list)
