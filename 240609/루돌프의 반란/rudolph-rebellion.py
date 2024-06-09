import sys
from collections import deque
import copy

def print_2d(a):
    for i in a:
        for j in i:
            print(j, end='\t')
        print()
    print('===')

def calc_dist(i, j, r, c):
    return (r-i)**2+(c-j)**2
def move_rudolf(rudolf):

    min_distance = 1e+9
    min_santa = -1
    for i in range(N):
        for j in range(N):
            ## 산타가 있을 경우
            if len(board_santas[i][j]) > 0 :
                dist = calc_dist(rudolf[0], rudolf[1], i, j)
                if dist <= min_distance:
                    min_distance = dist
                    min_santa = [board_santas[i][j][0], i, j]

    i, j = rudolf[0], rudolf[1]
    min_dist = 1e+9
    min_rudolf = []
    for d in range(8):
        ii = i + dy[d]
        jj = j + dx[d]

        if ii < 0 or jj < 0 or ii >= N or jj >= N :
            continue
        dist = calc_dist(ii, jj, min_santa[1], min_santa[2])
        if dist < min_dist:
            min_rudolf = [ii, jj, d]
            min_dist = dist

    rudolf = min_rudolf[:2]

    ## 산타와 충돌할 경우
    if len(board_santas[min_rudolf[0]][min_rudolf[1]]) > 0 :
        crash(min_rudolf[0], min_rudolf[1], min_rudolf[2], [min_rudolf[0], min_rudolf[1], board_santas[min_rudolf[0]][min_rudolf[1]]], C)

    return rudolf

def crash(i, j, d, santa, score):
    global scores
    scores[santa[2][0]] += score

    ii = i + dy[d] * score
    jj = j + dx[d] * score
    santa[2][1] = 2

    if ii < 0 or jj < 0 or ii >= N or jj >= N :
        board_santas[santa[0]][santa[1]] = []
    elif len(board_santas[ii][jj]) > 0 :
        ## 상호 작용
        temp = santa[2]
        board_santas[santa[0]][santa[1]] = []

        while True :
            temp2 = board_santas[ii][jj]
            board_santas[ii][jj] = temp
            temp = temp2

            ii = ii + dy[d]
            jj = jj + dx[d]

            if ii < 0 or jj < 0 or ii >= N or jj >= N :
                break
            if len(board_santas[ii][jj]) == 0 :
                board_santas[ii][jj] = temp
                break
    else :
        board_santas[ii][jj] = santa[2]
        board_santas[santa[0]][santa[1]] = []
    return board_santas

def find_santa(p):
    for i in range(N):
        for j in range(N):
            if len(board_santas[i][j]) > 0 :
                if board_santas[i][j][0] == p :
                    return i, j
    return None, None
def move_santas(board_santas):
    for p in range(1, P+1):
        i, j = find_santa(p)
        if i == None :
            continue

        ## 기절하지 않는 산타 중,
        if board_santas[i][j][1] == 0:
            min_dist = calc_dist(i, j, rudolf[0], rudolf[1])
            min_santa = []

            for d in range(4):
                ii = i + dy[d*2]
                jj = j + dx[d*2]

                if ii < 0 or jj < 0 or ii >= N or jj >= N or len(board_santas[ii][jj])>0:
                    continue
                dist = calc_dist(ii, jj, rudolf[0], rudolf[1])
                if min_dist > dist :
                    min_dist = dist
                    min_santa = [ii, jj, d*2]

            ## p 산타가 움직여야 할 때,
            if len(min_santa) > 0 :
                ## 충돌
                if min_santa[0] == rudolf[0] and min_santa[1] == rudolf[1] :
                    board_santas = crash(min_santa[0], min_santa[1], (min_santa[2]+4) % 8, [i, j, board_santas[i][j]], D)
                else :
                    board_santas[min_santa[0]][min_santa[1]] = board_santas[i][j]
                    board_santas[i][j] = []
    return board_santas


dy = [-1, -1, 0, 1, 1, 1, 0, -1]
dx = [0, 1, 1, 1, 0, -1, -1, -1]

N, M, P, C, D = map(int, input().split())
rudolf = list(map(int, input().split()))
rudolf = [rudolf[0]-1, rudolf[1]-1]
board_santas = [[[] for _ in range(N)] for _ in range(N)]
scores = [0 for _ in range(P+1)]

for _ in range(P):
    p, i, j = map(int, input().split())
    board_santas[i-1][j-1] = [p, 0]

for _ in range(M):
    rudolf = move_rudolf(rudolf)
    board_santas = move_santas(board_santas)

    num =0
    for i in range(N):
        for j in range(N):
            if len(board_santas[i][j]) > 0 :
                scores[board_santas[i][j][0]] += 1
                board_santas[i][j][1] = max(0, board_santas[i][j][1]-1)
                num+=1
    if num ==0 :
        break

answer = ""
for i in scores[1:]:
    answer += str(i) + " "
print(answer)