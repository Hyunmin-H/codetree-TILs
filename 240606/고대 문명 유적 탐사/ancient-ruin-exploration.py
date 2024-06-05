import sys
from collections import deque
import copy

def print_2d(a):
    for i in a :
        for j in i:
            print(j,end=' ')
        print()
    print('===')
def rotate(board, d, i, j):
    new_board = copy.deepcopy(board)
    temp_board = [[0 for _ in range(3)] for _ in range(3)]
    temp_board2 = [[0 for _ in range(3)] for _ in range(3)]
    for y in range(3):
        for x in range(3):
            temp_board[y][x] = board[i+y][j+x]
    for dd in range(d):
        for y in range(3):
            for x in range(3):
                temp_board2[x][y] = temp_board[3-y-1][x]
        temp_board = [a[:] for a in temp_board2]
    for y in range(3):
        for x in range(3):
            new_board[i+y][j+x] = temp_board[y][x]
    return new_board


def bfs(y, x, board, v):

    q = deque([(y, x)])
    v[y][x] = True
    num = 0
    while q :
        i, j = q.popleft()
        num +=1

        for d in range(4):
            ii = i + dy[d]
            jj = j + dx[d]

            if ii < 0 or jj < 0 or ii >=5 or jj >=5 or v[ii][jj]:
                continue
            if board[y][x] == board[ii][jj] :
                q.append((ii, jj))
                v[ii][jj] = True
    return num, v
def obtain_remains(board):
    sum_value = 0
    v = [[False for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            if not v[i][j] :
                value, v = bfs(i, j, board, v)
                if value >=3 :
                    sum_value += value
    return sum_value


def find_optim_remains():
    global board
    max_value = 0
    max_queue = deque([])
    for d in range(1, 4):
        for i in range(3):
            for j in range(3):
                new_board = rotate(board, d, i, j)
                value = obtain_remains(new_board)
                if value == max_value :
                    max_queue.append((d, i, j))
                elif value > max_value :
                    max_value = value
                    max_queue = deque([(d, i, j)])
    d, i, j = max_queue.popleft()
    board = rotate(board, d, i, j)
    return board


def bfs2(y, x, v):
    ## 3 이상의 i, j return
    q = deque([(y, x)])
    ij_list = []
    v[y][x] = True
    num = 0
    while q :
        i, j = q.popleft()
        num +=1
        ij_list.append((i, j))
        for d in range(4):
            ii = i + dy[d]
            jj = j + dx[d]

            if ii < 0 or jj < 0 or ii >=5 or jj >=5 or v[ii][jj]:
                continue

            if board[y][x] == board[ii][jj] :
                q.append((ii, jj))
                v[ii][jj] = True
    if num >=3 :
        return ij_list, v
    else :
        return [], v
def obtain_remains_and_fill(remains_queue):
    values_obtained = 0
    while True :
        v = [[False for _ in range(5)] for _ in range(5)]
        remain_ij_list = []
        for i in range(5):
            for j in range(5):
                if not v[i][j] :
                    ij_list, v = bfs2(i, j, v)
                    remain_ij_list.extend(ij_list)
        if len(remain_ij_list) == 0 :
            break
        values_obtained += len(remain_ij_list)
        remain_ij_list = sorted(remain_ij_list, key = lambda x:x[0], reverse = True)
        remain_ij_list = sorted(remain_ij_list, key = lambda x:x[1])

        for i, j in remain_ij_list:
            index = remains_queue.popleft()
            board[i][j] = index

    return remains_queue, values_obtained

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]



K, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(5)]
remains_queue = deque(map(int, input().split()))
answer = ""
for k in range(K):
    board = find_optim_remains()
    remains_queue, value = obtain_remains_and_fill(remains_queue)
    if value == 0 :
        break

    answer += str(value) + " "
print(answer)