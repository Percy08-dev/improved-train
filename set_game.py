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