from typing import List

import numpy as np


def read_environment() -> List[float]:
    """Mock sensor input: replace later with real sensor vectors."""
    return list(np.random.randn(1))
