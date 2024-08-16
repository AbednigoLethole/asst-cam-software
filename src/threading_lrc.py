"""Script to run the background thread."""

import threading


def background(f):
    """
    a threading decorator
    use @background above the function
    you want to run in the background
    """

    # TODO:Introduce Dramatiq to control and monitor background threads. # pylint: disable=W0511
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return backgrnd_func
