#!/usr/bin/env python3
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Create and return a function that multiplies a float by
    the given multiplier.

    Parameters:
    - multiplier (float): The multiplier to be used in the returned function.

    Returns:
    - Callable[[float], float]: A function that takes a float as input and
      returns the product of the input and multiplier.
    """
    def multiplier_function(x: float) -> float:
        """
        Multiply a float by the given multiplier.

        Parameters:
        - x (float): The input float.

        Returns:
        - float: The product of the input float and multiplier.
        """
        return x * multiplier

    return multiplier_function
