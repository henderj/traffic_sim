import vector
import numpy as np


def normalize(v: vector.VectorObject) -> vector.VectorObject:
    normalized_v = v / np.sqrt(np.sum(v ** 2))
    return normalized_v
