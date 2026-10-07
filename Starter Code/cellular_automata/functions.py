from datatypes import GameBoard


def play_automaton(
    initial_board: GameBoard,
    num_gens: int,
    neighborhood_type: str,
    rules: dict[str, str]
) -> list[GameBoard]:
    """
    Simulate a cellular automaton for a given number of generations.

    Args:
        initial_board (GameBoard): The starting configuration of the automaton.
        num_gens (int): The number of generations to simulate.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state.

    Returns:
        list[GameBoard]: A list of GameBoard objects of length num_gens + 1,
        representing the automaton's progression from the initial board
        through each generation.
    """
    if not isinstance(initial_board, list) or len(initial_board) == 0:
        raise ValueError("initial_board must be a non-empty GameBoard.")
    assert_rectangular(initial_board)
    if type(num_gens) is not int or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dict[str, str].")

    boards = []
    boards.append([row[:] for row in initial_board])

    for i in range(num_gens):
        curr_board = boards[i]
        new_board = update_board(curr_board, neighborhood_type, rules)
        boards.append(new_board)

    return boards


def update_board(
    current_board: GameBoard,
    neighborhood_type: str,
    rules: dict[str, str]
) -> GameBoard:
    """
    Update a GameBoard for one generation according to the given rules and neighborhood type.

    Args:
        current_board (GameBoard): The current state of the automaton.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state

    Returns:
        GameBoard: The new board after applying the automaton rules for one generation.
    """
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    assert_rectangular(current_board)
    if neighborhood_type not in ["Moore", "vonNeumann"]:
        raise ValueError("neighborhood_type must be 'Moore' or 'vonNeumann'.")
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dictionary.")

    num_rows = count_rows(current_board)
    num_cols = count_columns(current_board)

    newboard = initialize_board(num_rows, num_cols)

    #range over all the cells of the current board and
    #update each cell acoording to the rules of gol
    for i in range(num_rows):
        for j in range(num_cols):
            newboard[i][j] = update_cell(
                current_board, i, j, neighborhood_type, rules
            )

    return newboard


def update_cell(
    board: GameBoard,
    r: int,
    c: int,
    neighborhood_type: str,
    rules: dict[str, str]
) -> str:
    """
    update_cell takes a GameBoard along with row and column indices,
    a neighborhood type, and a rule map.
    It returns the state of the cell at this row and column
    in the next generation.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    assert_rectangular(board)
    if type(r) is not int or type(c) is not int:
        raise ValueError("r and c must be integers.")
    if not in_field(board, r, c):
        raise ValueError("(r, c) must be inside the board.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dict[str, str].")

    #convert cell and its neighborhood to a string
    nbrhood = neighborhood_to_string(board, r, c, neighborhood_type)

    return rules.get(nbrhood, "0")


def neighborhood_to_string(
    current_board: GameBoard,
    r: int,
    c: int,
    neighborhood_type: str
) -> str:
    """
    neighborhood_to_string takes as input a GameBoard, row and column indices,
    and a neighborhood type as a string.
    It returns a string formed of the central square followed by its neighbors
    according to the neighborhood type indicated.

    Args:
        current_board (GameBoard): The game board.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        neighborhood_type (str): Either "Moore" or "vonNeumann".

    Returns:
        str: A string encoding the central cell and its neighbors' states.
    """
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    assert_rectangular(current_board)
    if type(r) is not int or type(c) is not int:
        raise ValueError("r and c must be integers.")
    if not in_field(current_board, r, c):
        raise ValueError("(r, c) must be inside the board.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')

    #First element in the string is the current cell
    neghiorhood = str(current_board[r][c])

    #then based on off the other negihborood type,
    # we are going to add the other neighbors to this string

    if neighborhood_type == "Moore":
        neighborhood_cells = [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c + 1),
            (r + 1, c + 1),
            (r + 1, c),
            (r + 1, c - 1),
            (r, c - 1),
        ]
    elif neighborhood_type == "vonNeumann":
        neighborhood_cells = [
            (r - 1, c),
            (r, c + 1),
            (r + 1, c),
            (r, c - 1),
        ]
    else:
        raise ValueError("Error")

    for (x, y) in neighborhood_cells:
        # make sure x and y in board
        if in_field(current_board, x, y):
            neghiorhood += str(current_board[x][y])
        else:
            neghiorhood += str(0)

    return neghiorhood


def initialize_board(num_rows: int, num_cols: int) -> GameBoard:
    """
    Initialize a GameBoard with the given number of rows and columns.

    Args:
        num_rows (int): Number of rows.
        num_cols (int): Number of columns.

    Returns:
        GameBoard: A num_rows x num_cols board filled with "0" values.
    """
    if type(num_rows) is not int or num_rows <= 0:
        raise ValueError("num_rows must be a positive integer.")
    if type(num_cols) is not int or num_cols <= 0:
        raise ValueError("num_cols must be a positive integer.")

    board: GameBoard = [] # declaring board

    for _ in range(num_rows):
        row = ["0"] * num_cols
        board.append(row)

    return board


def count_rows(board: GameBoard) -> int:
    """
    Count the number of rows in a GameBoard.

    Args:
        board (GameBoard): A 2D list of strings representing the game state.

    Returns:
        int: Number of rows in the board.
    """
    if not isinstance(board, list):
        raise ValueError("board must be a list.")

    return len(board)


def count_columns(board: GameBoard) -> int:
    """
    Count the number of columns in a GameBoard.

    Args:
        board (GameBoard): A 2D list of strings representing the game state.

    Returns:
        int: Number of columns in the board.

    Raises:
        ValueError: If the board is not rectangular.
    """
    assert_rectangular(board)

    return len(board[0])


def assert_rectangular(board: GameBoard) -> None:
    """
    Check whether a GameBoard is rectangular.

    Args:
        board (GameBoard): The game board.

    Raises:
        ValueError: If the board has no rows or if its rows are not the same length.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")

    if not isinstance(board[0], list) or len(board[0]) == 0:
        raise ValueError("Board rows must be non-empty lists.")

    first_row_length = len(board[0])

    # range over rows and make sure that they have the same length as first row
    for row in board:
        if not isinstance(row, list):
            raise ValueError("Each board row must be a list.")
        if len(row) != first_row_length:
            raise ValueError("Error: GameBoard is not rectangular.")


def in_field(board: GameBoard, i: int, j: int) -> bool:
    """
    Check if the indices (i, j) are within the bounds of the board.

    Args:
        board (GameBoard): The game board (2D list of strings).
        i (int): Row index.
        j (int): Column index.

    Returns:
        bool: True if (i, j) is inside the board, False otherwise.
    """
    # parameter checks
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if type(i) is not int or type(j) is not int:
        raise ValueError("i and j must be integers.")

    if i < 0 or j < 0:
        return False
    if i >= len(board) or j >= len(board[i]):
        return False

    # if we survive to here, then we are on the board
    return True