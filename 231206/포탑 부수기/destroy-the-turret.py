import sys
from collections import deque

def print_2d(a):
    for i in a :
        for j in i:
            print(j, end=' ')
        print()
    print('=====')

def is_end(area):
    count = 0
    for i in area :
        for j in i :
            if j > 0 :
                count += 1
    if count <= 1 :
        return True
    else :
        return False

def get_strongest(area):
    s = 0
    for i in area :
        for j in i :
            s = max(s, j)
    return s

def select_attacker(area):
    min_value = 1e+9
    min_ijs = []
    for i in range(N):
        for j in range(M):
            if area[i][j] ==0 :
                continue
            if area[i][j] < min_value  :
                min_value = area[i][j]
                min_ijs = [(i, j)]
            elif area[i][j] == min_value :
                min_ijs.append((i, j))
    if len(min_ijs) == 1 :
        return min_ijs[0]

    recent = 0
    recent_ij = []

    for i, j in min_ijs :
        if attack_history[i][j] > 0 and recent < attack_history[i][j] :
            recent = attack_history[i][j]
            recent_ij = [(i, j)]
    if len(recent_ij) > 0 :
        return recent_ij[0]
    # for i in range(len(attacker_list)-1, -1, -1):
    #     if attacker_list[i] in min_ijs :
    #         return attacker_list[i]

    max_sum = 0
    max_sum_ijs = []
    for i, j in min_ijs :
        if max_sum < i+j :
            max_sum = i+j
            max_sum_ijs = [(i, j)]
        elif max_sum == i+j :
            max_sum_ijs.append((i, j))
    if len(max_sum_ijs) == 1 :
        return max_sum_ijs[0]


    max_j = 0
    max_j_ij = []
    for i, j in max_sum_ijs :
        if max_j < j :
            max_j = j
            max_j_ij = [(i, j)]
    return max_j_ij[0]

def select_defenser(area, a_i, a_j):
    attacker = (a_i, a_j)
    max_value = 0
    max_ijs = []
    for i in range(N):
        for j in range(M):
            if area[i][j] ==0 :
                continue
            if i == a_i and j == a_j :
                continue
            if area[i][j] > max_value  :
                max_value = area[i][j]
                max_ijs = [(i, j)]
            elif area[i][j] == max_value :
                max_ijs.append((i, j))
    if len(max_ijs) == 1 :
        if max_ijs[0] != attacker  :
            return max_ijs[0]


    old = 1e+9
    old_ij = []

    for i, j in max_ijs :
        if old > attack_history[i][j] :
            old = attack_history[i][j]
            old_ij = [(i, j)]
        elif old == attack_history[i][j] :
            old_ij.append((i, j))
    if len(old_ij) ==1 :
        return old_ij[0]

    #
    # in_attacker= []
    # in_attacker_set=set([])
    #
    # print('attacker_list', attacker_list)
    # for i in range(len(attacker_list)):
    #     if attacker_list[i] in max_ijs :
    #         in_attacker.append(attacker_list[i])
    #         in_attacker_set.add(attacker_list[i])
    # print('in_attacker', in_attacker)
    # print('max_ijs', max_ijs)
    # if len(in_attacker_set) == len(max_ijs):
    #     return in_attacker[0]
    # else :
    #     for in_attack in in_attacker:
    #         if in_attack in max_ijs:
    #             max_ijs.remove(in_attack)

    min_sum = 1e+9
    min_sum_ijs = []
    for i, j in max_ijs :
        if min_sum > i+j :
            min_sum = i+j
            min_sum_ijs = [(i, j)]
        elif min_sum == i+j :
            min_sum_ijs.append((i, j))
    if len(min_sum_ijs) == 1 :
        if min_sum_ijs[0] != attacker  :
            return min_sum_ijs[0]

    min_j = 1e+9
    min_j_ij = []
    for i, j in min_sum_ijs :
        if min_j > j :
            min_j = j
            min_j_ij = [(i, j)]
    print('min_j_ij', min_j_ij)
    return min_j_ij[0]

def attack_laser(i, j, d_i, d_j, route, v):

    if i == d_i and j == d_j :
        routes_final.append(route)
        return
    route.append((i, j))
    v[i][j] = True

    for n in range(4):
        ii = (i + dy[n]) % N
        jj = (j + dx[n]) % M
        if area[ii][jj] == 0 :
            continue
        if not v[ii][jj] :
            v_ = [vv[:] for vv in v]
            route_ = [r[:] for r in route]
            attack_laser(ii, jj, d_i, d_j, route_, v_)

def attack_laser2(i, j, d_i, d_j):
    q = deque([(i, j, [(i, j)])])

    while q:
        ii, jj, route = q.pop()

        for n in range(4):
            iii = (ii + dy[n]) % N
            jjj = (jj + dx[n]) % M

            if area[iii][jjj] == 0 :
                continue
            if (iii, jjj) == (d_i, d_j):
                return route
                break

            if not (iii, jjj) in route:

                route_ = [r[:] for r in route]
                route_.append((iii, jjj))
                q.append((iii, jjj, route_))

    # print(routes_final)


def choose_min_route(routes):
    min_value = 1e+9
    min_routes = []
    for route in routes:
        if len(route) < min_value :
            min_value = len(route)
            min_routes = [route]
        elif len(route) == min_value :
            min_routes.append(route)
    return min_routes[0][1:]

def damage_route(route, damage):
    for r in route :
        i, j = r
        area[i][j] = max(0, area[i][j] - damage//2)

def attack_poktan(a_i, a_j, d_i, d_j, damage):
    dyy = [-1, -1, 0, 1, 1, 1, 0, -1]
    dxx = [0, 1, 1, 1, 0, -1, -1, -1]
    damage_area = []
    for n in range(8):
        ii = (d_i + dyy[n]) % N
        jj = (d_j + dxx[n]) % M

        if area[ii][jj] == 0 or (ii == a_i and jj == a_j):
            continue
        area[ii][jj] = max(0, area[ii][jj]  - damage//2)
        damage_area.append((ii, jj))
    return damage_area

def append_attacker(a_i, a_j):
    if (a_i, a_j) in attacker_list:
        attacker_list.remove((a_i, a_j))
    attacker_list.append((a_i, a_j))

def get_energy(a_i, a_j, d_i, d_j, route):

    for i in range(N):
        for j in range(M):
            if area[i][j] == 0 :
                continue
            if (i == a_i and j == a_j) or (i == d_i and j == d_j):
                continue
            if (i, j) in route :
                continue
            area[i][j] += 1


# dy = [0, 1, 0, -1]
# dx = [1, 0, -1, 0]
dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]

N, M, K = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(N)]
attacker_list = []
attack_history = [[0 for _ in range(M)] for _ in range(N)]
for k in range(K):
    if is_end(area) :
        break
    a_i, a_j = select_attacker(area)
    area[a_i][a_j] += N+M

    d_i, d_j = select_defenser(area, a_i, a_j)
    v = [[False for _ in range(M)] for _ in range(N)]
    v[a_i][a_j] = True
    routes_final = []
    # attack_laser(a_i, a_j, d_i, d_j, [], v)
    routes_final.append(attack_laser2(a_i, a_j, d_i, d_j))

    if len(routes_final) == 0 :
        route_final = attack_poktan(a_i, a_j, d_i, d_j, area[a_i][a_j])
    else :
        route_final = choose_min_route(routes_final)
        damage_route(route_final, area[a_i][a_j])
    area[d_i][d_j] = max(0, area[d_i][d_j] - area[a_i][a_j])
    get_energy(a_i, a_j, d_i, d_j,route_final)

    append_attacker(a_i, a_j)
    attack_history[a_i][a_j] = k+1
print(get_strongest(area))