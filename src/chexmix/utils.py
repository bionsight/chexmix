import gzip
import itertools
import logging
import os
import pickle
import re
from contextlib import contextmanager

import pandas as pd

import chexmix.env as env

log = logging.getLogger(__name__)


def basename(path):
    """get base name from path, i.e., filename without ext"""

    basename_, ext = os.path.splitext(os.path.basename(path))
    while ext != '':
        basename_, ext = os.path.splitext(os.path.basename(basename_))

    return basename_


def data_file(file_name):
    return os.path.join(env.data_path, file_name)


def save(o, filename):
    with open(filename, 'wb') as f:
        pickle.dump(o, f)


def load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


__disable_cache = False         # TODO: hide the global variable


@contextmanager
def disable_cache():
    global __disable_cache
    old_disable_cache = __disable_cache
    __disable_cache = True

    try:
        yield old_disable_cache

    finally:
        __disable_cache = old_disable_cache


def cached(pkl_filename):
    global __disable_cache

    def inner_decorator(f):
        def run_func(*args, reset=False, **kwargs):
            if (not __disable_cache) and (not reset) and os.path.isfile(pkl_filename):
                log.info(f'load {pkl_filename}')
                return load(pkl_filename)
            else:
                if __disable_cache or reset:
                    log.info('forced to run')
                ret = f(*args, **kwargs)
                log.info(f'save {pkl_filename}')
                save(ret, pkl_filename)
                return ret
        return run_func
    return inner_decorator


def first(iterable, condition=lambda x: True, default=None):
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
        else:
            raise


def flatten_list(lst):
    """concatenate a list of lists"""
    return list(itertools.chain.from_iterable(lst))


def iter_grouper(n, iterable):
    """returns iterator that chunks iterable"""
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


def open_mode(filename, mode):
    if mode == 'r':
        return 'rt' if filename.endswith('.gz') else 'r'
    return mode


def fopen(filename, mode='r'):
    """file open helper"""
    mode = open_mode(filename, mode)
    return gzip.open(filename, mode) if filename.endswith('.gz') \
        else open(filename, mode)


def strip(text):
    """strip str without Exception"""
    try:
        return text.strip()
    except AttributeError:
        return text


def remove_none_vals(dt):
    """remove None values in a dictionary"""
    return {k: v for k, v in dt.items() if not pd.isnull(v)}


def remove_symbols(s):
    """convert symbols to under bar"""
    return re.sub(r'[.,!?"\':;~() -]', '_', s)
