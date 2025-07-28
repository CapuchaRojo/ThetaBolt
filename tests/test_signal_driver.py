from src.agents.signal_driver import read_environment


def test_env_signal():
    data = read_environment()
    assert isinstance(data, dict)
    assert "emf" in data
    assert "signal_strength" in data
    assert "noise" in data
