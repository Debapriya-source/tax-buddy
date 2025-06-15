from langchain.agents import tool


@tool
def add(a: float, b: float) -> float:
    """
    add two numbers and return the result
    Args:
        a (float): first number
        b (float): second number
    Returns:
        float: sum of a and b
    """
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """
    subtract two numbers and return the result
    Args:
        a (float): first number
        b (float): second number
    Returns:
        float: difference of a and b
    """
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """
    multiply two numbers and return the result
    Args:
        a (float): first number
        b (float): second number
    Returns:
        float: product of a and b
    """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """
    divide two numbers and return the result
    Args:
        a (float): first number
        b (float): second number
    Returns:
        float: quotient of a and b
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@tool
def power(base: float, exponent: float) -> float:
    """
    raise base to the power of exponent and return the result
    Args:
        base (float): base number
        exponent (float): exponent number
    Returns:
        float: base raised to the power of exponent
    """
    return base**exponent


@tool
def square_root(number: float) -> float:
    """
    calculate the square root of a number and return the result
    Args:
        number (float): number to calculate square root of
    Returns:
        float: square root of the number
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number**0.5


@tool
def percentage(part: float, whole: float) -> float:
    """
    calculate the percentage of part in whole and return the result
    Args:
        part (float): part of the whole
        whole (float): whole number
    Returns:
        float: percentage of part in whole
    """
    if whole == 0:
        raise ValueError("Cannot calculate percentage of zero")
    return (part / whole) * 100
