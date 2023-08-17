"""
Helpers File

A collection of useful functions.
"""

import os
import json

from typing import Callable, cast

from flipflop.structure import Flip

import settings


'''API'''


def cache_json(module: settings.Modules):
    """
    A decorator to save to or fetch from a designated JSON data cache, if permitted by ``settings.CACHE``.

    This will also save the data to a session cache, meaning it only reads from the local cache once.
    """

    def wrapper(fetcher: Callable):

        session_cache = None

        def _wrapper(*args, **kwargs):
            nonlocal session_cache

            # If session cache exists, just return that
            if session_cache is not None:
                return session_cache

            # Cache exists; use it
            cache_path = os.path.join(settings.CACHE_PATH, module.value)

            if settings.CACHE and module not in settings.REGENERATE_CACHE and os.path.exists(cache_path):
                with open(cache_path, 'r') as f:
                    session_cache = json.loads(f.read())
                    return session_cache

            # Cache does not exist, module is to be regenerated, or ``CACHE = False``; fetch data and create
            # (if applicable)

            data = fetcher(*args, **kwargs)
            session_cache = data

            if settings.CACHE:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)

                with open(cache_path, 'w') as f:
                    f.write(
                        json.dumps(data)
                    )

            return data

        return _wrapper

    return wrapper


'''Flips'''


def flip(flip_obj: type[Flip]):
    """A simple decorator to wrap flip function outputs with their corresponding ``Flip()`` objects."""

    def wrapper(flip_func: Callable):

        def _wrapper(*args, **kwargs):

            result = flip_func(*args, **kwargs)
            return flip_obj(*result)

        return _wrapper

    return wrapper


'''Internals'''


def to_tuple(o: dict):
    """Transform a ``dict()`` recipe object to a tuple form."""

    # Forgive me, programming gods! (╯˘ -˘ )╯
    return cast(
        tuple[tuple[str, int]],
        tuple(o.items())
    )


def multiply(o: dict, factor: int):
    """Multiplies the values of a ``dict()`` object by an integer factor."""

    for k in o.keys():
        o[k] = o[k] * factor

    return o
