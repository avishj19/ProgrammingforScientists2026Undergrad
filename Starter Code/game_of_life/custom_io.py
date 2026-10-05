from datatypes import GameBoard


def read_board_from_file(filename: str) -> GameBoard:
    """
    Reads a CSV file representing a Game of Life board.
    "1" = alive (True), "0" = dead (False).
    Args:
        filename (str): The name of the CSV file.
    Returns:
        GameBoard: Parsed board.
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")

    board = []

    with open(filename, "r") as file:
        for line in file:
            row = []

            values = line.strip().split(",")

            for value in values:
                if value == "1":
                    row.append(True)
                elif value == "0":
                    row.append(False)
                else:
                    raise ValueError("Board can only contain 0s and 1s.")

            board.append(row)

    return board

def set_row_values(line_elements: list[str]) -> list[bool]:
    """
    Convert a list of "0"/"1" strings into booleans.
    Args:
        line_elements (list[str]): Strings "0"/"1".
    Returns:
        list[bool]: Row with True/False.
    """
    if not isinstance(line_elements, list) or len(line_elements) == 0:
        raise ValueError("line_elements must be a non-empty list.")
    return []  # TODO: implement
