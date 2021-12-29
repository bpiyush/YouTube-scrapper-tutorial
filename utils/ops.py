"""
Utilities for simple pythonic operations.
"""
from typing import List, Any
from functools import reduce
import operator
import numpy as np
import torch


def get_from_dict(dataDict: dict, mapList: List):
    """
    Returns value from a dict based on list of keys.
    E.g., for dict D, keys=[a, b, c], it will return D[a][b][c]
    Credits: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys

    Args:
        dataDict (dict): input dictionary
        mapList (List): list of keys to be accessed

    Returns:
        Any: value from the dict based on given keys
    """
    return reduce(operator.getitem, mapList, dataDict)


def set_in_dict(dataDict: dict, mapList: List, value: Any):
    """
    Replaces given value in a dict based on list of keys.
    E.g., for dict D, keys=[a, b, c], it will set D[a][b][c] = value
    Note that this is in-place replacement

    Credits: https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys

    Args:
        dataDict (dict): input dictionary
        mapList (List): list of keys to be accessed
        value (Any): value to be replaced
    """
    get_from_dict(dataDict, mapList[:-1])[mapList[-1]] = value


def tensorize(x: np.ndarray) -> torch.Tensor:
    """Converts numpy ndarray object to torch tensor

    Args:
        x (np.ndarray): input

    Returns:
        torch.tensor: tensorized input
    """
    if not isinstance(x, torch.Tensor):
        assert isinstance(x, np.ndarray)
        x = torch.from_numpy(x)
    return x


def numpify(x: torch.Tensor) -> np.ndarray:
    """Converts torch tensor to numpy ndarray

    Args:
        x (torch.Tensor): input

    Returns:
        np.ndarray: numpy ndarray conversion of input
    """
    if not isinstance(x, np.ndarray):
        assert isinstance(x, torch.Tensor)

        if x.requires_grad:
            x = x.detach()
        
        if x.is_cuda:
            x = x.cpu()
        
        x = x.numpy()
    
    return x


class DotDict(dict):
    """Allows dot.notation access to dictionary attributes

    Args:
        dict (dict): input dictionary
    """
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val
