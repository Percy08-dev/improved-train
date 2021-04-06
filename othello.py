import sys
import random
import time

# 初期化
def set_game():
    board = [[-1 for i in range(8)] for j in range(8)]
    for i in range(3, 5):
        for j in range(3, 5):
            if (i+j)%2 == 0:
                board[i][j] = 0
            else:
                board[i][j] = 1
    
    return board

# 表示部
def visualise_player(num):
    if num == 1:
        return "◇"
    else:
        return "◆"

def visualise(line):
    v_line = ["" for i in range(8)]
    for i in range(8):
        if line[i] == 1:
            v_line[i] = "◇"
        elif line[i] == 0:
            v_line[i] = "◆"
        else:
            v_line[i] = " "
    
    return v_line

def print_board(board):
    # 最上段ルーラー出力
    print("   ", end =" ")
    for i in range(97, 97 + 8):
        print(chr(i), end = " ")
    print()
    
    for i in range(8):
        print(f"{i}", "[", end = " ")
        for j in visualise(board[i]):
            print(j, end = " ")
        print("]")


# 既存のマスに隣接しているかを確認 -> 不正な値の場合はFalse(0)を返す
# 判定 -> (縦, 横, 斜め)それぞれ、挟むことができる場合に終点までの座標を返す, 挟めない場合-1を返す.
# point -> (x, y)
def adjacent(board, point, player):
    # 隣接確認 -> 不正な値ならばFalseを返す
    # boardを10x10にして枠を例外にしたほうがスマート、でもリファクタリングしたくない...

    for i in range(point[0] - 1, point[0] + 2):
        # 無理やり回避部分
        if i < 0 or i > 7:
            continue

        for j in range(point[1] - 1, point[1] + 2):
            # 同様に無理やり部分
            if j < 0 or j > 7:
                continue

            if [i, j] == point:
                continue
            
            if board[j][i] != -1:
                break
        else:
            continue
        break
    else:
        return False
    
    return True

# 既存のマスのチェック
def existing_point(board, point):
    x, y = point
    if board[y][x] != -1:
        return False
    else:
        return True

# 横の確認
def horizon_check(board, point, player):
    x, y = point
    mem = [x, x]
    #left
    for i in reversed(range(x)):
        if board[y][i] == -1:
            mem[0] = x
            break
        elif board[y][i] == player:
            mem[0] = i
            break
    
    #right
    for i in range(x+1, 8):
        if board[y][i] == -1:
            mem[1] = x
            break
        elif board[y][i] == player:
            mem[1] = i
            break

    # 連続していないかの確認
    if mem[1] - mem[0] == 1:
        mem = [x, x]

    return mem

# 縦の確認
def vertical_check(board, point, player):
    x, y = point
    mem = [y, y]

    # upper
    for i in reversed(range(y)):
        if board[i][x] == -1:
            mem[0] = y
            break
        elif board[i][x] == player:
            mem[0] = i
            break

    # lower
    for i in range(y+1, 8):
        if board[i][x] == -1:
            mem[1] = y
            break
        elif board[i][x] == player:
            mem[1] = i
            break

    # 連続していないかの確認
    if mem[1] - mem[0] == 1:
        mem = [y, y]

    return mem

# 斜めの判定はy = x + res, y = -x + resで行う
# 右斜めの確認
def diagonal_right_check(board, point, player):
    x, y = point
    mem = [[x, y], [x, y]]
    res = y - x
    # upper left
    for i in reversed(range(x)):
        if i + res < 0:
            continue

        if board[i + res][i] == -1:
            mem[0] = [x, y]
            break

        elif board[i + res][i] == player:
            mem[0] = [i, i + res]
            break
        

    
    # lower right
    for i in range(x + 1, 8):
        #print("::::::::", i + res, chr(i + 97))
        if i + res >= 8:
            break

        if board[i + res][i] == -1:
            mem[1] = [x, y]
            break
        elif board[i + res][i] == player:
            mem[1] = [i, i + res]
            break
    
    # 連続してないか確認
    if mem[1][0] - mem[0][0] == 1 and mem[1][1] - mem[0][1] == 1:
        mem = [[x, y], [x, y]]
    
    return mem

# 左斜めの確認
def diagonal_left_check(board, point, player):
    x, y = point
    mem = [[x, y], [x, y]]
    res = x + y

    # lower left
    for i in reversed(range(x)):
        #print(i, res-i)
        if res - i >= 8:
            continue

        if board[res - i][i] == -1:
            mem[0] = [x, y]
            break
        elif board[res - i][i] == player:
            mem[0] = [i, res - i]
            break

    # upper right
    for i in range(x+1, 8):
        if res - i < 0:
            break

        if board[res - i][i] == -1:
            mem[1] = [x, y]
            break
        elif board[res - i][i] == player:
            mem[1] = [i, res - i]
            break
    
    # 連続してないか確認
    #print(mem)
    if mem[1][0] - mem[0][0] == 1 and mem[0][1] - mem[1][1] == 1:
        mem = [[x, y], [x, y]]
    
    return mem




# 縦横斜めのチェッカーのまとめ
# 縦横斜めの判定と, boardの更新をどうにか同時にしたい, global変数をのぞく方法でどうにかしたい
def checker(board, point, player):
    x, y = point

    h = horizon_check(board, point, player)
    v = vertical_check(board, point, player)
    r_d = diagonal_right_check(board, point, player)
    l_d = diagonal_left_check(board, point, player)

    #print(h, v, r_d, l_d)
    if h == [x, x] and v == [y, y] and r_d == [[x, y], [x, y]] and l_d == [[x, y], [x, y]]:
        return False
    else:
        return True

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

# 終了判定
def fill_check(board):
    mem = 0
    for i in board:
        mem += i.count(-1)
    return mem

# 置ける場所のリストを返す
def can_place_stone(board, player):
    mem = []
    for i in range(8):
        for j in range(8):
            point = [i, j]
            if adjacent(board, point, player) and existing_point(board, point) and checker(board, point, player):
                mem.append(point)

    return mem

# 全滅判定
def no_stone(board, player):
    j = False
    for i in board:
        j = j or player in i
    
    return j

# 勝利判定
def stone_count(board):
    p = [0, 0]
    for i in board:
        p[0] += i.count(0)
        p[1] += i.count(1)

    return p

def judge(board):
    cnt = stone_count(board)
    print(f"{visualise_player(0)} : {cnt[0]}")
    print(f"{visualise_player(1)} : {cnt[1]}")
    if cnt[0] > cnt[1]:
        print("win:", visualise_player(0))
    elif cnt[0] < cnt[1]:
        print("win:", visualise_player(1))
    else:
        print("Draw!")

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
    
    board = reverser(board, point, player)
    
    return board

# 0手読み (test play)
def point_input_testplay(board, player, can_place_stone_list):
    while True:
        i = random.randint(0, len(can_place_stone_list) - 1)
        x, y = can_place_stone_list[i]
        #time.sleep(0.2)

        point = [x, y] 

        if point in can_place_stone_list:
            break
        else:
            print("置けないマスです.")
    
    return point

# 本体
def game():
    print("\n New Game! \n")

    player = 1
    board = set_game()
    print_board(board)

    skip_cnt = 0

    if len(sys.argv) == 1:
        mode = None
    else:
        mode = sys.argv[1]

    while True:
        if (fill_check(board) == False or no_stone(board, player) == False):
            print(fill_check(board), no_stone(board, player))
            judge(board)
            break

        if skip_cnt == 2:
            print("両者置けません.")
            judge(board)
            break
        
        can_place_stone_list = can_place_stone(board, player)
        if len(can_place_stone_list) == 0:
            print(visualise_player(player), "は置く場所がありません.")
            print("手番を変わります.")
            player = not player
            skip_cnt += 1
            continue
        
        if mode == "auto":
            point = point_input_testplay(board, player, can_place_stone_list)
            board = reverser(board, point, player)
        else:
            point = point_input(board, player, can_place_stone_list)
            board = reverser(board, point, player)
        
        print_board(board)
        skip_cnt = 0
        player = not player

game()