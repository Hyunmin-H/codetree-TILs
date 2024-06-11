import sys
from collections import deque
import copy

def print_2d(a):
    for i in a :
        for j in i :
            print(j,end=" ")
        print()
    print('===')
def copy_monsters(board_monsters):
    # copied = [b[:] for b in b_row for b_row in board_monsters]
    copied = copy.deepcopy(board_monsters)

    return copied

def move_monsters(board_monsters):
    after_board = [[deque() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            while board_monsters[i][j] :
                mon_dir = board_monsters[i][j].popleft()

                is_move = False
                for _ in range(8):
                    ii = i + dy[mon_dir]
                    jj = j + dx[mon_dir]

                    if ii < 0 or jj < 0 or ii >= 4 or jj >= 4 or (ii == packman[0] and jj == packman[1]) or len(deads[ii][jj])>0 :
                        mon_dir = (mon_dir + 1) %8
                    else :
                        after_board[ii][jj].append(mon_dir)
                        is_move = True
                        break
                if not is_move :
                    after_board[i][j].append(mon_dir)
    return after_board

def move_packman(packman, board_monsters, deads):
    max_dirs = []
    max_eat = 0
    temp = copy.deepcopy(board_monsters)
    i, j = packman
    temp_mon = [[] for _ in range(3)]
    for d1 in range(4):
        ii1 = i + dy[d1*2]
        jj1 = j + dx[d1 * 2]

        if ii1 < 0 or jj1 < 0 or ii1 >= 4 or jj1 >= 4:
            continue
        count1 = len(temp[ii1][jj1])
        temp_mon[0] = temp[ii1][jj1]
        temp[ii1][jj1] = deque()
        for d2 in range(4):
            ii2 = ii1 + dy[d2*2]
            jj2 = jj1 + dx[d2 * 2]

            if ii2 < 0 or jj2 < 0 or ii2 >= 4 or jj2 >= 4:
                continue
            count2 = len(temp[ii2][jj2])
            temp_mon[1] = temp[ii2][jj2]
            temp[ii2][jj2] = deque()
            for d3 in range(4):
                ii3 = ii2 + dy[d3*2]
                jj3 = jj2 + dx[d3 * 2]

                if ii3 < 0 or jj3 < 0 or ii3 >= 4 or jj3 >= 4:
                    continue
                count3 = len(temp[ii3][jj3])
                temp_mon[2] = temp[ii3][jj3]
                temp[ii3][jj3] = deque()

                if count1+count2+count3 > max_eat :
                    max_dirs = [d1, d2, d3]
                    max_eat = count1+count2+count3
                temp[ii3][jj3] =  temp_mon[2]
            temp[ii2][jj2] = temp_mon[1]
        temp[ii1][jj1] = temp_mon[0]


    if max_eat == 0 : 
        max_dirs = [0, 0, 0]
    ii, jj = i, j
    for d in max_dirs :
        ii = ii + dy[d*2]
        jj = jj + dx[d*2]

        for _ in range(len(board_monsters[ii][jj])):
            deads[ii][jj].append(3)
        board_monsters[ii][jj] = deque()

    packman = [ii, jj]
    return board_monsters, deads, packman

def decrease_deadtime(deads):
    for i in range(4):
        for j in range(4):
            after_dead = []
            for k in range(len(deads[i][j])):
                deads[i][j][k] -= 1
                if deads[i][j][k] != 0 :
                    after_dead.append(deads[i][j][k])
            deads[i][j] = after_dead
    return deads
def add_copied_monsters(board_monsters, copied):
    for i in range(4):
        for j in range(4):
            for dir in copied[i][j] :
                board_monsters[i][j].append(dir)
    return board_monsters

def count_monsters(board_monsters):
    count = 0
    for i in range(4):
        for j in range(4):
            count += len(board_monsters[i][j])

    return count



dy = [-1, -1, 0, 1, 1, 1, 0, -1]
dx = [0, -1, -1, -1, 0, 1, 1, 1]


M, T = map(int, input().split())
r, c = map(int, input().split())
packman = [r-1, c-1]
board_monsters = [[deque() for _ in range(4)] for _ in range(4)]
deads = [[[] for _ in range(4)] for _ in range(4)]


for _ in range(M):
    r, c, d = map(int, input().split())
    board_monsters[r-1][c-1].append(d-1)

for t in range(T):
    copied = copy_monsters(board_monsters)
    board_monsters = move_monsters(board_monsters)
    board_monsters, deads, packman = move_packman(packman, board_monsters, deads)
    deads = decrease_deadtime(deads)

    board_monsters = add_copied_monsters(board_monsters, copied)
answer = count_monsters(board_monsters)
print(answer)