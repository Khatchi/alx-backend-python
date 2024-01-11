#!/usr/bin/ python3
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Calculate the sum of a list of integers and floats.

    Parameters:
    - mxd_lst (List[Union[int, float]]): A list containing integers and floats.

    Returns:
    - float: The sum of the elements in the mxd_lst.
    """
    return sum(mxd_lst)
