def sum(a, b):
    """
    >>> sum(5, 7)
    12

    >>> sum(4, -4)
    0
    """
    return a + b


def substract(a, b):
    """
    >>> substract(5, 7)
    -2
    """
    return a - b


def multiply(a, b):
    """
    >>> multiply(5, 7)
    35
    """
    return a * b


def divide(a, b):
    """
    >>> divide (10, 0)
    Traceback (most recent call last):
    ValueError: No está permitida la división entre 0
    """
    if b == 0:
        raise  ValueError("No está permitida la división entre 0")
    else:
        return a / b
