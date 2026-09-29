def main():
    print("Two-dimensional arrays (tuples and lists).")
    
    kernel = (
    (0.05,0.20,0.05),
    (0.20,0.00,0.20),
    (0.05,0.20,0.05)
)
    print(kernel)
    # we can acess indviual elements (everything is 0-indexed)
    #we cant cahnge indiviual elements
    print(kernel[0][2])
    print(kernel[1][1])
    print(kernel[2][1])

    #Creating a 7X4 by 0 values default
    #a = [[0]*4]*7

    a = []
    # create a matrix
    for i in range(7):
        new_row = [0]*4
        a.append(new_row)

    #we can also add declare using a comphresion
    a = [[0]*4 for i in range(7)]  

    a[1][2] = 19
    a[0][0] = 42
    a[6][3] = 100

    #we can get number of rows and colmuns
    print("Number of row is ", len(a))
    print("Number of col is",len(a[0]))
    print(a)

    # We can have non-rectangular lists too
    num_row = 4
    board = []
    for i in range(num_row):
        board.append([False]*i)
    
    #lets add a False to every row
    for row in range(len(board)):
        board[row].append(False)

    set_first_elements(board)
    print_board(board)
    print(board)

    print("Now its the game of life function")
    num_rows = 5
    num_cols = 5
    #Declare R- potemeno with everyting starting as False
    r_pen = [[False]* num_cols for i in range(num_rows)]

    #Now set the values
    r_pen[1][2] = True
    r_pen[1][3] = True
    r_pen[2][1] = True
    r_pen[2][2] = True
    r_pen[3][2] = True

    print_board(r_pen)


    
def set_first_elements(a: list(list[bool])) -> True: # type: ignore
    """
    Sets a element in the top left to be true
    """
    if len(a) == 0 or len(a[0]) == 0:
        raise ValueError("Invaild dimesion")
    a[0][0] = True


def print_board(board: list[list[bool]]):
    """
    Prints a 2d list of booleans in fasionable way
    """
    for row in board:
        print_row(row)

def print_row(row):
    for val in row:
        print_cell(val)
    print() # new line after a new row

def print_cell(a):
    if a:
        print("🥰", end = " ")
    else:
        print("☠️", end = " ")


if __name__ == "__main__":
    main()

