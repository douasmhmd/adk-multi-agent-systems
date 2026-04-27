# file: agent_math/tools.py


def add(numbers: list[int]) -> int:
    """Calculates the sum of a list of integers.

    Args:
        numbers: A list of integers to be added.

    Returns:
        The sum of the integers in the input list.
    """
    return sum(numbers)


def subtract(a: int, b: int) -> int:
    """Subtracts b from a.

    Args:
        a: The number to subtract from.
        b: The number to subtract.

    Returns:
        The result of a - b.
    """
    return a - b


def multiply(numbers: list[int]) -> int:
    """Calculates the product of a list of integers.

    Args:
        numbers: A list of integers to multiply.

    Returns:
        The product of all integers in the list.
    """
    result = 1
    for n in numbers:
        result *= n
    return result


def divide(a: float, b: float) -> float:
    """Divides a by b.

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        The result of a / b.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b