import sys
from collections import deque
import copy
def print_2d(a):
    for i in a:
        for j in i:
            print(j, end=' ')
        print()
    print('===')

def move_nutris(D, P, board_nutris):
    after_board = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if board_nutris[i][j] == 1:
                ii = (i + dy[D]*P) % N
                jj = (j + dx[D]*P) % N

                after_board[ii][jj] = 1
                board_trees[ii][jj] += 1

    board_trees_a = [a[:] for a in board_trees]
    for i in range(N):
        for j in range(N):
            if after_board[i][j] == 1:
                count = 0
                for d in range(4):
                    d = d*2 + 1

                    ii = i + dy[d]
                    jj = j + dx[d]
                    if ii < 0 or jj < 0 or ii >=N or jj >= N:
                        continue
                    if board_trees[ii][jj] >=1 :
                        count +=1

                board_trees_a[i][j] += count

    return after_board, board_trees_a

def cut_trees_and_put_nutris():
    board_nutris_a = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if board_nutris[i][j] != 1 :
                if board_trees[i][j] >=2 :
                    board_trees[i][j] -=2
                    board_nutris_a[i][j] = 1
    return board_nutris_a, board_trees

def calc_answer():
    count = 0
    for i in range(N):
        for j in range(N):
            count += board_trees[i][j]
    return count

dy = [0, -1, -1, -1, 0, 1, 1, 1]
dx = [1, 1, 0, -1, -1, -1, 0, 1]

N, M = map(int, input().split())
board_trees = [list(map(int, input().split())) for _ in range(N)]
board_nutris = [[0 for _ in range(N)] for _ in range(N)]
board_nutris[N-2][0] = 1
board_nutris[N-2][1] = 1
board_nutris[N-1][0] = 1
board_nutris[N-1][1] = 1

move_rules = []
for _ in range(M):
    d, s = map(int, input().split())
    move_rules.append((d-1, s))

for m in range(M):
    board_nutris, board_trees = move_nutris(move_rules[m][0], move_rules[m][1], board_nutris)
    board_nutris, board_trees = cut_trees_and_put_nutris()

answer = calc_answer()
print(answer)