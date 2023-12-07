import sys
from collections import deque

def print_2d(a):
    for i in a:
        for j in i:
            print(j, end=' ')
        print()
    print('=====')

def find_people_and_exit():
    exit = ()
    people = []
    for i in range(N):
        for j in range(N):
            if area[i][j] >=11 :
                people.append((i, j))
            if area[i][j] == -1 :
                exit = (i, j)
    return people, exit

def move_people(people, exit):
    global final_move_length
    ei, ej = exit
    for p in people :
        pi, pj = p
        pii, pjj = p
        if pi > ei :
            pii = pi -1
        elif pi < ei :
            pii = pi +1
        elif pj > ej :
            pjj = pj -1
        elif pj < ej :
            pjj = pj + 1

        if pii < 0 or pjj < 0 or pii >=N or pjj >=N or 0 < area[pii][pjj] < 10 :
            continue
        final_move_length += area[pi][pj] - 10
        if area[pii][pjj] == -1 :
            area[pi][pj] = 0
        else :
            area[pii][pjj] = area[pi][pj]
            area[pi][pj] = 0

def set_square(exit):
    ei, ej = exit
    q = deque([])
    q.append((ei, ej))
    v = [[False for _ in range(N)] for _ in range(N)]
    v[ei][ej] = True
    target_p = ()
    is_break = False
    while q :
        i, j = q.popleft()

        for n in range(4):
            ii = i + dy[n]
            jj = j + dx[n]

            if ii < 0 or jj < 0 or ii >=N or jj >=N or v[ii][jj] :
                continue
            if area[ii][jj] >= 11 :
                target_p = (ii, jj)
                is_break = True
                break
            v[ii][jj] = True
            q.append((ii, jj))
        if is_break :
            break

    ti, tj = target_p
    height = abs(ti - ei)
    width = abs(tj - ej)
    max_length = max(height, width)
    if height > width :
        max_x = max(tj, ej)
        lx = max_x - height-1
        while True :
            lx +=1
            if 0<= lx < N :
                break
        lu = (min(ti, ei), lx)
        rb = (max(ti, ei), lx + height)

    elif height < width :
        max_y = max(ti, ei)
        ly = max_y - width-1
        while True :
            ly +=1
            if 0<= ly < N :
                break
        lu = (ly, min(tj, ej))
        rb = (ly+width, max(tj, ej))
    else :
        lu = (min(ti, ei), min(tj, ej))
        rb = (max(ti, ei), max(tj, ej))
    return lu, rb

def rotate_matrix(a):

    a_ = [[0 for _ in range(len(a))] for _ in range(len(a))]
    length = len(a)
    for i in range(length):
        for j in range(length):
            a_[j][length-1-i] = a[i][j]
    return a_
def rotate_square(lu, rb):
    import copy
    lui, luj = lu
    rbi, rbj = rb
    temp_area = [a[luj:rbj+1] for a in area[lui:rbi+1]]

    length = len(temp_area)
    for i in range(length):
        for j in range(length):
            temp_area[j][length-1-i] = area[lui+i][luj+j]

    # rotated_area = rotate_matrix(temp_area)

    for i in range(len(temp_area)) :
        for j in range(len(temp_area)) :
            if 0 < temp_area[i][j] < 10 :
                area[i+lui][j+luj] = temp_area[i][j] -1
            else :
                area[i + lui][j + luj] = temp_area[i][j]
    del temp_area

def rotate_miro(exit) :

    lu, rb = set_square(exit)
    rotate_square(lu, rb)



dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]
N, M , K = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(N)]
for _ in range(M) :
    i, j = map(int, input().split())
    area[i-1][j-1] = 11
exit = list(map(int, input().split()))
final_move_length = 0
area[exit[0]-1][exit[1]-1] = -1

for k in range(K):
    people, exit = find_people_and_exit()
    if len(people) == 0:
        break
    move_people(people, exit)
    people, exit = find_people_and_exit()
    if len(people) == 0:
        break

    rotate_miro(exit)

print(final_move_length)
_, exit = find_people_and_exit()
print(exit[0]+1, exit[1]+1)