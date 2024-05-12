import modelbit, sys
from typing import *

# main function
def double_number(num: float) -> float:
    """
    Example model that doubles numbers
    >>> double_number(21)
    42
    """
    return 2 * num

# to run locally via git & terminal, uncomment the following lines
# if __name__ == "__main__":
#   result = double_number(...)
#   print(result)