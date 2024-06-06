import sys
from collections import deque
import copy

def find_player(m):
    for i, row in enumerate(players_board):
        for j, a in enumerate(row):
            if len(a) != 0 :
                n, d, s, g = a
                if n == m :
                    return i, j, d, s, g

def fight(m1_i, m1_j, M1, m2_i, m2_j, M2):
    m1, d1, s1, g1 = M1
    m2, d2, s2, g2 = M2
    if s1+g1 == s2+g2:
        if s1 > s2 :
            return m1_i, m1_j, M1, m2_i, m2_j, M2
        else :
            return
    elif s1+g1 > s2+g2:
        return m1_i, m1_j, M1, m2_i, m2_j, M2
    else :
        return m2_i, m2_j, M2, m1_i, m1_j, M1

def loser_action(i, j, info):
    guns_board[i][j].append(info[3])
    info[3] = 0
    d = info[1]
    ii = i + dy[d]
    jj = j+ dx[d]

    while True :
        if ii < 0 or jj < 0 or ii >=N or jj >=N or len(players_board[ii][jj])>0 :
            d = (d+1)%4
            ii = i + dy[d]
            jj = j + dx[d]
        else :
            info[1] = d
            players_board[ii][jj] = copy.deepcopy(info)

            if len(guns_board[ii][jj]) > 0:
                max_gun = max(guns_board[ii][jj])
                if players_board[ii][jj][3] < max_gun:
                    guns_board[ii][jj].append(players_board[ii][jj][3])
                    players_board[ii][jj][3] = max_gun
                    guns_board[ii][jj].remove(max_gun)
            break

def move(m):
    global answer, dy, dx
    i, j, d, s, g = find_player(m)
    ii = i + dy[d]
    jj = j + dx[d]

    if ii < 0 or jj < 0 or ii >=N or jj >=N:
        d = (d+2)%4
        ii = i + dy[d]
        jj = j + dx[d]
        players_board[i][j][1] = d

    temp_player = copy.deepcopy(players_board[i][j])
    players_board[i][j] = []
    if len(players_board[ii][jj]) == 0 :
        if len(guns_board[ii][jj]) > 0 :
            max_gun = max(guns_board[ii][jj])
            if temp_player[3] < max_gun :
                guns_board[ii][jj].append(temp_player[3])
                temp_player[3] = max_gun
                guns_board[ii][jj].remove(max_gun)
        players_board[ii][jj] = copy.deepcopy(temp_player)
    else :
        winner_i, winner_j, winner_info, loser_i, loser_j, loser_info = fight(i, j, temp_player, ii, jj, players_board[ii][jj])

        answer[winner_info[0]] += winner_info[2]+winner_info[3] - (loser_info[2] +loser_info[3])

        loser_action(ii, jj, loser_info)

        if len(guns_board[loser_i][loser_j]) > 0:
            max_gun = max(guns_board[loser_i][loser_j])
            if winner_info[3] < max_gun :
                guns_board[ii][jj].append(winner_info[3])
                winner_info[3] = max_gun
                guns_board[ii][jj].remove(max_gun)
        players_board[ii][jj] = copy.deepcopy(winner_info)





def print_2d(a):
    for i in a:
        for j in i:
            print(j, end='\t\t')
        print()
    print('===')

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

N, M, K = map(int, input().split())
guns_board = [list(map(int, input().split())) for _ in range(N)]
answer = [0 for _ in range(M)]
for i in range(N):
    for j in range(N):
        guns_board[i][j] = [guns_board[i][j]]
players_board = [[[] for _ in range(N)] for _ in range(N)]
for i in range(M):
    x, y, d, s = map(int, input().split())
    players_board[x-1][y-1].extend([i, d, s, 0])
for k in range(K):
    for m in range(M):
        move(m)
answer_str = ""
for a in answer : 
    answer_str += str(a) + " "

print(answer_str)