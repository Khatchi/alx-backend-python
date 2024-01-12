#!/usr/bin/env python3
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Create a tuple with the string k and the square of the int or float v.

    Parameters:
    - k (str): A string.
    - v (Union[int, float]): An int or float.

    Returns:
    - Tuple[str, float]: A tuple containing the string k and the square of v.
    """
    result = (k, v ** 2.0)
    return result
