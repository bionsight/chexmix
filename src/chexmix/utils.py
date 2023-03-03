import gzip
import itertools
import logging
import os
import pickle
import re
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterable, List

from chexmix import env
import pandas as pd

log = logging.getLogger(__name__)


def basename(path) -> str:
    """get base name from path, i.e., filename without ext"""

    basename_, ext = os.path.splitext(os.path.basename(path))
    while ext != '':
        basename_, ext = os.path.splitext(os.path.basename(basename_))

    return basename_


def data_file(file_name: str) -> str:
    return os.path.join(env.data_path, file_name)


def save(data: Any, filename: str) -> None:
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load(filename: str) -> Any:
    with open(filename, 'rb') as f:
        return pickle.load(f)


@contextmanager
def disable_cache():
    enable_cache = env.enable_cache

    try:
        if not enable_cache:
            yield True
        else:
            yield False

    finally:
        pass


def cached(pkl_filename: str) -> Callable:
    diable_cache = env.enable_cache

    def inner_decorator(f):
        def run_func(*args, reset=False, **kwargs):
            if (not diable_cache) and (not reset) and os.path.isfile(pkl_filename):
                log.info(f'load {pkl_filename}')
                return load(pkl_filename)
            if diable_cache or reset:
                log.info('forced to run')
            ret = f(*args, **kwargs)
            log.info(f'save {pkl_filename}')
            save(ret, pkl_filename)
            return ret

        return run_func

    return inner_decorator


def first(iterable: Iterable, condition=lambda x: True, default: Any = None) -> Any:
    """
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    If the `default` argument is given and the iterable is empty,
    or if it has no items matching the condition, the `default` argument
    is returned if it matches the condition.

    The `default` argument being None is the same as it not being given.

    Raises `StopIteration` if no item satisfying the condition is found
    and default is not given or doesn't satisfy the condition.

    >>> first( (1,2,3), condition=lambda x: (x % 2 == 0))
    2
    >>> first(range(3, 100))
    3
    >>> first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    >>> first([], default=1)
    1
    >>> first([], default=1, condition=lambda x: x % 2 == 0)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> first([1,3,5], default=1, condition=lambda x: x % 2 == 0)
    Traceback (most recent call last):
    ...
    StopIteration
    """

    try:
        return next(x for x in iterable if condition(x))
    except StopIteration:
        if default is not None and condition(default):
            return default
        raise


def flatten_list(lst: List[Any]) -> List[Any]:
    """concatenate a list of lists"""
    return list(itertools.chain.from_iterable(lst))


def iter_grouper(chunk_size: int, iterable: Iterable) -> itertools.chain:
    """returns iterator that chunks iterable"""
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, chunk_size)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


def open_mode(filename: str, mode: str) -> str:
    if mode == 'r':
        return 'rt' if filename.endswith('.gz') else 'r'
    return mode


def fopen(filename: str, mode='r') -> Any:
    """file open helper"""
    mode = open_mode(filename, mode)
    return (
        gzip.open(filename, mode, encoding='utf-8')
        if filename.endswith('.gz')
        else open(filename, mode, encoding='utf-8')
    )


def strip(text: str) -> str:
    """strip str without Exception"""
    try:
        return text.strip()
    except AttributeError:
        return text


def remove_none_vals(dt: Dict) -> Dict:
    """remove None values in a dictionary"""
    return {k: v for k, v in dt.items() if not pd.isnull(v)}


def remove_symbols(s: str) -> str:
    """convert symbols to under bar"""
    return re.sub(r'[.,!?"\':;~() -]', '_', s)
