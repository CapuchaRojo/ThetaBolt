import time

from src.kernel.qatp_kernel import QATPKernel


class DummySignal:
    @staticmethod
    def read_environment():
        return {"emf": 0.5, "signal_strength": 50, "noise": 0.1}


def test_kernel_dispatch(monkeypatch):
    monkeypatch.setattr("src.kernel.qatp_kernel.signal_driver", DummySignal)
    kernel = QATPKernel(config={"loop_interval": 0.1})
    kernel.startup()
    time.sleep(0.3)
    kernel.shutdown()
    assert not kernel.running
