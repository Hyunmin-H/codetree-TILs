import sys
from collections import deque
import copy

def bfs(r, c, v):
    q = deque([(r, c)])
    q_ij = deque([(r, c)])
    q_status = deque([board[r][c]])
    v[r][c] = True
    q.popleft()
    for d in range(4):
        ii = r + dy[d]
        jj = c + dx[d]

        if ii < 0 or jj < 0 or ii >= N or jj >= N or v[ii][jj]:
            continue
        if board[ii][jj] == 2:
            q.append((ii, jj))
            v[ii][jj] = True
            q_ij.append((ii, jj))
            q_status.append(board[ii][jj])


    while q :
        i, j = q.popleft()

        for d in range(4):
            ii = i+dy[d]
            jj = j+dx[d]

            if ii< 0 or jj < 0 or ii >=N or jj >= N or v[ii][jj]:
                continue
            if board[ii][jj] > 0 :
                q.append((ii, jj))
                v[ii][jj] = True
                q_ij.append((ii, jj))
                q_status.append(board[ii][jj])
    return q_ij, q_status, v


def make_queues():
    q_ij_list = []
    q_status_list = []

    v = [[False for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not v[i][j] and board[i][j] == 1  :
                q_ij, q_status, v = bfs(i, j, v)
                q_ij_list.append(q_ij)
                q_status_list.append(q_status)
    return q_ij_list, q_status_list

def move(q_status_list, dirs):

    for i, q_status in enumerate(q_status_list):
        if dirs[i] == 0 :
            status = q_status.popleft()
            q_status.append(status)
        else :
            status = q_status.pop()
            q_status.appendleft(status)
    return q_status_list, dirs

def q_to_mat(q_ij_list, q_status_list):

    new_board = [[0 for _ in range(N)] for _ in range(N)]
    for m in range(M):
        for n, (i, j) in enumerate(q_ij_list[m]):
            new_board[i][j] = q_status_list[m][n]
    return new_board

def get_order_person(i, j, dirs):
    for m in range(M):
        if (i, j) in q_ij_list[m]:
            index = q_ij_list[m].index((i, j))
            break
    if dirs[m] == 0 :
        order = 0
        while True :
            order += 1
            if q_status_list[m][index] == 1 :
                break
            index = index-1
    else :
        order = 0
        while True :
            order += 1
            if q_status_list[m][index] == 1 :
                break
            index = (index+1) % N

    return order, m

def change_order(m, dirs):

    for i in range(len(q_status_list[m])):
        if q_status_list[m][i] == 1 :
            q_status_list[m][i] = 3
        elif q_status_list[m][i] == 3 :
            q_status_list[m][i] = 1

    dirs[m] = (dirs[m]+1) % 2
    return dirs

def throw_ball(board, k, dirs):
    global answer
    order = 0
    d = (k // N) % 4
    n = k % N


    if d == 2 or d == 3 :
        n = N - n -1

    if d == 0 :
        ## 가로
        for j in range(N):
            if 0< board[n][j] < 4:
                order, m = get_order_person(n, j, dirs)
                dirs = change_order(m, dirs)
                break


    elif d ==1 :
        for i in range(N-1, -1, -1):
            if 0 < board[i][n] <4 :
                order,m =get_order_person(i, n, dirs)
                dirs = change_order(m, dirs)
                break
    elif d == 2 :
        ## 가로
        for j in range(N-1, -1, -1):
            if 0 < board[n][j] <4 :
                order, m =get_order_person(n, j, dirs)
                dirs = change_order(m, dirs)
                break
    elif d == 3 :
        for i in range(N):
            if 0 < board[i][n] <4 :
                order,m  =get_order_person(i, n, dirs)
                dirs = change_order(m, dirs)
                break

    answer += order * order
    return dirs

def print_2d(a):
    for i in a :
        for j in i:
            print(j, end=' ')
        print()
    print('===')



dy = [0, 1, 0, -1]
dx = [-1, 0, 1, 0]

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
answer = 0
q_ij_list, q_status_list = make_queues()
dirs = [0 for _ in range(M)]

for k in range(K):
    move(q_status_list, dirs)
    board = q_to_mat(q_ij_list, q_status_list)
    dirs = throw_ball(board, k, dirs)
print(answer)