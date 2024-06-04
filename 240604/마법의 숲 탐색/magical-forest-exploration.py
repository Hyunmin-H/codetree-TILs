import sys
from collections import deque

def print_2d(a):
    for i in a :
        for j in i :
            print(j, end=' ')
        print()
    print('===')
def check_and_move(r, c, exit):
    # 남쪽 한칸, 아니면 동쪽 아니면 서쪽

    if r == -2 and board[r+2][c] == 0 :
        r += 1
    elif r+2 < R and board[r+2][c]==0 and board[r+1][c-1]==0 and board[r+1][c+1]==0 :
        r +=1
    else :
        if 2 <= c < C  and board[r][c-2] == 0 and board[r-1][c-1] == 0 and board[r+1][c-1]==0 \
            and r + 2 < R and board[r + 2][c-1] == 0 and board[r + 1][c - 2] == 0 :
                c -= 1
                exit = (exit-1)%4
                r += 1
        else :
            if 0< c < C-2  and board[r][c + 2] == 0 and board[r - 1][c + 1] == 0 and board[r + 1][c + 1] == 0\
                and r + 2 < R and board[r + 2][c+1] == 0 and board[r + 1][c+2] == 0 :
                    r += 1
                    c += 1
                    exit = (exit+1)%4
            else :
                return False,r, c, exit
    return True, r, c, exit

def move_gorium(c, exit, k):
    global board
    r = -2
    while True :
        is_move, r, c, exit = check_and_move(r, c, exit)
        if not is_move :
            break
    if r < 0 :
        board = [[0 for _ in range(C)] for _ in range(R)]
    else :
        board[r][c] = k
        for d in range(4):
            if d == exit:
                board[r+dy[d]][c+dx[d]] = -k
            else :
                board[r+dy[d]][c+dx[d]] = k

    return r, c

def move_ferrary(r, c, k):

    max_r = 0
    q = deque([(r, c)])

    v = [[False for _ in range(C)] for _ in range(R)]
    v[r][c] = True

    while q :
        i, j = q.popleft()

        for d in range(4):
            ii = i + dy[d]
            jj = j + dx[d]

            if ii < 0 or jj < 0 or ii >=R or jj >= C or v[ii][jj]:
                continue
            if board[i][j] < 0  and board[ii][jj] != 0:
                max_r = max(max_r, ii+1)
                q.append((ii, jj))
                v[ii][jj] = True
            elif board[i][j] > 0  and (board[ii][jj] == -board[i][j] or board[ii][jj] == board[i][j]) :
                max_r = max(max_r, ii+1)
                q.append((ii, jj))
                v[ii][jj] = True


    global answer
    answer += max_r







dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

R, C, K = map(int, input().split())
ferrarys = [list(map(int, input().split())) for _ in range(K)]
board = [[0 for _ in range(C)] for _ in range(R)]
answer = 0
## board - n : 페라리 번호, -n : 페라리 n 의 출구
for k in range(K):
    k +=1
    r, c = move_gorium(ferrarys[k-1][0]-1, ferrarys[k-1][1], k)
    move_ferrary(r, c, k)

print(answer)