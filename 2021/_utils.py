import os

def read_input(filepath: str):
    """
    Open and read file at filepath, return list of integers.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_path, filepath)

    with open(filepath) as _input:
        return _input.read().splitlines()