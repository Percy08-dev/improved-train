import sys
import random
import time
from visual import visualise_player

# 入力
def point_input(board, player, can_place_stone_list):
    while True:
        print(visualise_player(player), "(x, y)を入力してください :", end = " ")
        # print(can_place_stone_list)
        try:
            x, y = input().split()
        except:
            print("Error!")
            continue

        #強制終了
        if x == "-1" and y == "-1":
            sys.exit()

        if not(97 <= ord(x) <= 97 + 7):
            print("xには、a - hを入力してください")
            continue
        if not(48 <= ord(y) <= 48 + 7):
            print("yには0 - 7を入力してください")
            continue
        point = [ord(x) - 97, int(y)] 

        if point in can_place_stone_list:
            break
        else:
            print("置けないマスです.")
    
    return point

def point_input_testplay(board, player, can_place_stone_list):
    while True:
        i = random.randint(0, len(can_place_stone_list) - 1)
        x, y = can_place_stone_list[i]
        time.sleep(0.2)

        point = [x, y] 

        if point in can_place_stone_list:
            break
        else:
            print("置けないマスです.")
    
    return point