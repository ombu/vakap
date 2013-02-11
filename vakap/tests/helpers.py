import sys
import cStringIO
from functools import wraps


def capture(returns_output=True):
    """
        http://stackoverflow.com/questions/2828953/silent-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-restor

        Decorate a function that prints to stdout, intercepting the output.
        If "returns_output" is True, the function will return a generator
        yielding the printed lines instead of the return values.

        The decorator litterally hijack sys.stdout during each function
        execution for ALL THE THREADS, so be careful with what you apply it to
        and in which context.

        >>> def numbers():
            print "42"
            print "1984"
        ...
        >>> numbers()
        42
        1984
        >>> capture(False)(numbers)()
        >>> list(capture()(numbers)())
        ['42', '1984']

    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            saved_stdout = sys.stdout
            sys.stdout = cStringIO.StringIO()

            try:
                out = func(*args, **kwargs)
                if returns_output:
                    out = sys.stdout.getvalue().strip().split()
            finally:
                sys.stdout = saved_stdout

            return out

        return wrapper

    return decorator
