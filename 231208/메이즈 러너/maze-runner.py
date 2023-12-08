import sys
from collections import deque

def print_2d(a):
    for i in a:
        for j in i:
            print(j, end=' ')
        print()
    print('=====')

def print_2d2(a, b):
    for i, j in zip(a, b):
        for ii, jj in zip(i, j):
            print(ii+ 10*jj, end=' ')
        print()
    print('=====')
def find_people_and_exit():
    exit = ()
    people = []
    for i in range(N):
        for j in range(N):
            if area_p[i][j] > 0 :
                people.append([i, j, area_p[i][j]])
            if area[i][j] == -1 :
                exit = (i, j)
    return people, exit

def move_people(people, exit):
    global final_move_length
    ei, ej = exit
    p_after = people[:]

    for n, p in enumerate(people) :
        is_move = False
        is_skip = False
        pi, pj, n_p = p
        pii, pjj, _ = p
        if pi > ei :
            pii = pi -1
        elif pi < ei :
            pii = pi +1
        else :
            is_skip = True

        if not is_skip :
            # if not (pii < 0 or pjj < 0 or pii >=N or pjj >=N or 0 < area[pii][pjj] < 10) :
            if  pii >= 0 and pjj >= 0 and pii < N and pjj < N:

                if area[pii][pjj] == -1 : ## 출구일 때
                    p_after[n][0] = -1
                    p_after[n][1] = -1
                    final_move_length += n_p
                    continue
                elif area_p[pii][pjj] > 0: ## 사람이 있을 때
                    p_after[n][0] = pii
                    p_after[n][1] = pjj
                    # area[pii][pjj] += n_p
                    # area[pi][pj] = 0
                    final_move_length += n_p
                    continue
                elif area[pii][pjj] == 0 and area_p[pii][pjj] == 0: ## 아무도 없을 때
                    p_after[n][0] = pii
                    p_after[n][1] = pjj
                    # area[pii][pjj] = 10+n_p
                    # area[pi][pj] = 0
                    final_move_length += n_p

                    continue

        pii, pjj, _ = p

        if pj > ej :
            pjj = pj -1
        elif pj < ej :
            pjj = pj + 1
        else :
            continue

        if pii < 0 or pjj < 0 or pii >=N or pjj >=N or 0 < area[pii][pjj] < 10 :
            continue
        final_move_length += n_p
        if area[pii][pjj] == -1 : ## 출구일 때
            p_after[n][0] = -1
            p_after[n][1] = -1
            # area[pi][pj] = 0
        elif area_p[pii][pjj] > 0: ## 사람이 있을 때
            p_after[n][0] = pii
            p_after[n][1] = pjj
            # area[pii][pjj] += n_p
            # area[pi][pj] = 0
        elif area[pii][pjj] == 0 and area_p[pii][pjj] == 0: ## 아무도 없을 때
            p_after[n][0] = pii
            p_after[n][1] = pjj
            # area[pii][pjj] = 10+n_p
            # area[pi][pj] = 0
    area_p_after = [[0 for _ in range(N)] for _ in range(N)]
    for p in p_after:
        i, j, np = p
        if i == -1 and j == -1 :
            continue
        area_p_after[i][j] += np



    return area_p_after

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

def set_square2(exit):
    is_exit = False
    is_person = False
    for n in range(2,N+1):
        for i in range(N-n+1):
            for j in range(N-n+1):
                is_exit = False
                is_person = False
                for ii in range(n):
                    for jj in range(n):
                        if area_p[i+ii][j+jj] > 0:
                            is_person = True
                        elif area[i+ii][j+jj] == -1 :
                            is_exit = True

                if is_exit and is_person :
                    break
            if is_exit and is_person:
                break
        if is_exit and is_person:
            break
    return (i, j), (i+n-1, j+n-1)

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
    temp_area_p = [a[luj:rbj+1] for a in area_p[lui:rbi+1]]

    # length = len(temp_area)
    # for i in range(length):
    #     for j in range(length):
    #         temp_area[j][length-1-i] = area[lui+i][luj+j]

    temp_area = rotate_matrix(temp_area)
    temp_area_p = rotate_matrix(temp_area_p)

    for i in range(len(temp_area)) :
        for j in range(len(temp_area)) :
            if 0 < temp_area[i][j] < 10 :
                area[i+lui][j+luj] = temp_area[i][j] -1
            else :
                area[i+lui][j+luj] = temp_area[i][j]
            area_p[i + lui][j + luj] = temp_area_p[i][j]
    del temp_area

def rotate_miro(exit) :

    lu, rb = set_square2(exit)
    rotate_square(lu, rb)



dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]
N, M , K = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(N)]
area_p = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(M) :
    i, j = map(int, input().split())
    area_p[i-1][j-1] += 1
exit = list(map(int, input().split()))


final_move_length = 0
area[exit[0]-1][exit[1]-1] = -1

for k in range(K):
    people, exit = find_people_and_exit()
    if len(people) == 0:
        break
    area_p = move_people(people, exit)
    people, exit = find_people_and_exit()
    if len(people) == 0:
        break

    rotate_miro(exit)

print(final_move_length)
_, exit = find_people_and_exit()
print(exit[0]+1, exit[1]+1)