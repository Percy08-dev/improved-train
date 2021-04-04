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