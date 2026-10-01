import sys
import pygame
from custom_io import read_board_from_file
from functions import play_game_of_life
from drawing import draw_game_board, draw_game_boards
from animate import animate_surfaces


def main():
    print("Coding the Game of Life!")

    # CLAS go into an array (list) of strings called sys
    #length of sys.argv is 1 more than the number of parameters given 
    #sys.argv[0] is the name of the program (main.py here)
    # the remaning elements of the list are strings 
    # corresponding to what i passed into the command line

    if len(sys.argv) != 5:
        raise ValueError("Error")
    
    input_csv = sys.argv[1]
    output_prefix = sys.argv[2]
    cell_wdith = int(sys.argv[3])
    num_gens = int(sys.argv[4])

    #first, read the board from file
    inital_board = read_board_from_file(input_csv)
    # next simulate 
    all_boards = play_game_of_life(initial_board, num_gens)
    # next, animate and write to file 
    print("Animating board")
    # to fill in
    print("Animation drawn ")



if __name__ == "__main__":
    main()
