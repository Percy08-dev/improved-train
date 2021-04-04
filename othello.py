import sys

#from check import *
from check import adjacent
from check import existing_point
from check import horizon_check
from check import vertical_check
from check import diagonal_right_check
from check import diagonal_left_check
from check import checker
from check import fill_check
from check import can_place_stone

#from judge import *
from judge import no_stone
from judge import stone_count
from judge import judge

#from point_input import *
from point_input import point_input
from point_input import point_input_testplay

#from reverse import *
from reverse import reverser

#from set_game import *
from set_game import set_game

#from visual import *
from visual import visualise_player
from visual import visualise
from visual import print_board

# 本体
def game():
    print("\n New Game! \n")

    player = 1
    board = set_game()
    print_board(board)

    mode = sys.argv[1]

    while True:
        if fill_check(board) == False or no_stone(board, player) == False:
            judge(board)
            break
        
        can_place_stone_list = can_place_stone(board, player)
        if len(can_place_stone_list) == 0:
            print(visualise_player(player), "は置く場所がありません.")
            print("手番を変わります.")
            player = not player
            continue
        
        if mode == "auto":
            point = point_input_testplay(board, player, can_place_stone_list)
            board = reverser(board, point, player)
        else:
            point = point_input(board, player, can_place_stone_list)
            board = reverser(board, point, player)
        
        print_board(board)
        player = not player

game()