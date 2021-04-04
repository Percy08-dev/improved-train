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

# マスの反転
def reverser(board, point, player):
    x, y = point
    # 横
    h = horizon_check(board, point, player)
    for i in range(h[0], h[1] + 1):
        board[y][i] = player

    # 縦
    v = vertical_check(board, point, player)
    for i in range(v[0], v[1] + 1):
        board[i][x] = player

    # 右斜め
    r_d = diagonal_right_check(board, point, player)
    diff = r_d[1][0] - r_d[0][0]
    for i in range(diff):
        board[r_d[0][1] + i][r_d[0][0] + i] = player

    # 左斜め
    l_d = diagonal_left_check(board, point, player)
    diff = l_d[1][0] - l_d[0][0]
    for i in range(diff):
        board[l_d[0][1] - i][l_d[0][0] + i] = player

    return board
