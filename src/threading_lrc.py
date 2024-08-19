"""Decorator to run functions in the background using threads."""

import threading


def background(f):
    """
    A threading decorator.

    Use @background above the function
    you want to run in the background.
    """

    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return backgrnd_func
