from visual import visualise_player

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