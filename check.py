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

# 終了判定
def fill_check(board):
    mem = False
    for i in board:
        mem = (-1 in i) or mem
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