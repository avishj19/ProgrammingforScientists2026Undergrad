"""
Pseudocode

PlayGameOfLife(initialBoard, numGens)
    boards ← array of numGens + 1 game boards
    boards[0] ← initialBoard
    for every integer i from 1 to numGens
        boards[i] ← UpdateBoard(boards[i–1])
    return boards

UpdateBoard(currentBoard)
    numRows ← CountRows(currentBoard)
    numCols ← CountCols(currentBoard)
    newBoard ← InitializeBoard(numRows, numCols)
    for every integer r between 0 and numRows – 1
        for every integer c between 0 and numCols – 1
            newBoard[r][c] ← UpdateCell(currentBoard, r, c)
    return newBoard

UpdateCell(currentBoard, r, c)
    numNeighbors ← CountLiveNeighbors(currentBoard, r, c)
    if currentBoard[r][c] = true (current cell is alive)
        if numNeighbors = 2 or numNeighbors = 3 (propagation)
            return true
        else (no mates/overpopulation)
            return false
    else (current cell is dead)
        if numNeighbors = 3 (zombie!)
            return true
        else (rest in peace)
            return false

CountLiveNeighbors(currentBoard, r, c)
    count ← 0
    for every integer i between r – 1 and r + 1
        for every integer j between c – 1 and c + 1
            if (i≠r or j≠c) and InField(currentBoard, i, j) = true
                if currentBoard[i][j] = true
                    count ← count + 1
    return count

    
"""

from datatypes import GameBoard


def count_rows(board: GameBoard) -> int:
    """
    Count the number of rows in a GameBoard.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Returns:
        int: Number of rows in the board.
    """
    if not isinstance(board, list):
        raise ValueError("board must be a list.")
    return len(board) # TODO: implement


def count_cols(board: GameBoard) -> int:
    """
    Count the number of columns in a GameBoard.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Returns:
        int: Number of columns in the board.
    Raises:
        ValueError: If the board is not rectangular.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    
    #here is where we should make sure that board is rectangular
    assert_rectangular(board)

    return len(board[0])


def assert_rectangular(board: GameBoard) -> None:
    """
    Ensure that a GameBoard is rectangular.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Raises:
        ValueError: If the board has no rows or if its rows are not of equal length.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    # TODO: implement

    cols_0 = len(board[0])

    for i in range(count_rows(board)):
        if len(board[i]) != cols_0:
            raise ValueError("Eroor")
        
    #I survived and nothing is going to be retuned


def play_game_of_life(initial_board: GameBoard, num_gens: int) -> list[GameBoard]:
    """
    Simulate Game of Life for a given number of generations.
    Args:
        initial_board (GameBoard): The starting game board.
        num_gens (int): The number of generations to simulate.
    Returns:
        list[GameBoard]: Boards from initial through num_gens generations.
    """
    if not isinstance(initial_board, list) or len(initial_board) == 0:
        raise ValueError("initial_board must be a non-empty GameBoard.")
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer.")
    # TODO: implementboards = []
    boards = []

    #we know our first element of the list
    boards.append(initial_board)
    
    #we play the game num_gens times, updatingthe previous board each time
    for i in range(num_gens):
        prev_board = boards[i]
        new_board = update_board(prev_board)
        boards.append(new_board)
    



    return boards

def update_board(current_board: GameBoard) -> GameBoard:
    """
    Apply Game of Life rules for one generation.
    Args:
        current_board (GameBoard): The current game board.
    Returns:
        GameBoard: A new board representing the next generation.
    """
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    
    #make a new board of False
    num_rows = count_rows(current_board)
    num_cols = count_cols(current_board[0])

    newboard = initialize_board(num_rows, num_cols)


    
    #range over all the cells of the current board and
    #update each cell acoording to the rules of gol
    for i in range(num_rows):
        for j in range(num_cols):
            newboard[i][j] = update_cell(current_board,i,j)

    
    return newboard


def initialize_board(num_rows: int, num_cols: int) -> GameBoard:
    """
    Initialize a GameBoard with the given number of rows and columns.
    Args:
        num_rows (int): Number of rows.
        num_cols (int): Number of columns.
    Returns:
        GameBoard: A num_rows x num_cols board filled with False values.
    """
    if not isinstance(num_rows, int) or num_rows <= 0:
        raise ValueError("num_rows must be a positive integer.")
    if not isinstance(num_cols, int) or num_cols <= 0:
        raise ValueError("num_cols must be a positive integer.")
    
    board: GameBoard = []

    #create all rows
    for i in range(num_rows):
        current_row = [False] * num_cols
        board.append(current_row)
    
    return board


def update_cell(board: GameBoard, r: int, c: int) -> bool:
    """
    Determine the next state of the cell at (r, c).
    Args:
        board (GameBoard): The current game board.
        r (int): Row index.
        c (int): Column index.
    Returns:
        bool: True if alive next generation, False otherwise.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(r, int) or not isinstance(c, int):
        raise ValueError("r and c must be integers.")

    if board[r][c]: 
        if num_neigbhors == 2 or num_neighbhors ==3:
            return True

    
    else: # Dead
       if num_neighbors == 3:
           return True
       else:
           return False
    


def count_live_neighbors(board: GameBoard, r: int, c: int) -> int:
    """
    Count live neighbors of board[r][c].
    Args:
        board (GameBoard): The current game board.
        r (int): Row index.
        c (int): Column index.
    Returns:
        int: Number of live neighbors.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
   
    num_negigbhors = 0

    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            #board[i][j] is cuurent neighbhor
            if (((i !=r ) or (j !=c))) and in_field(board, i,j):
                if board[i][j]:
                    num_negigbhors+=1



    return num_negigbhors


def in_field(board: GameBoard, i: int, j: int) -> bool:
    """
    Check if the given (i, j) indices are within the board.
    Args:
        board (GameBoard): The current game board.
        i (int): Row index.
        j (int): Column index.
    Returns:
        bool: True if inside the board, False otherwise.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(i, int) or not isinstance(j, int):
        raise ValueError("i and j must be integers.")
    
    #lets check if it's not 
    if i < 0 or j < 0 or  i >= num_rows or j >= num_cols :
        return False
    
    return True
