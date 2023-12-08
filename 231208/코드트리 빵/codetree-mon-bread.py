import sys
from collections import deque

def print_2d(a):
    for i in a:
        for j in i:
            print(j, end=' ')
        print()
    print('---')
def search_nearest_basecamp(n):

    i, j, _ = store_list[n]
    q = deque([])
    v = [[False for _ in range(N)] for _ in range(N)]
    q.append((i, j))

    while q :
        ii, jj = q.popleft()

        for d in range(4):
            iii = ii + dy[d]
            jjj = jj + dx[d]

            if iii < 0 or jjj < 0 or iii >=N or jjj >=N or v[iii][jjj]:
                continue
            if area[iii][jjj] == -1 :
                continue

            if area[iii][jjj] == 1 :
                people_info[n] = [iii, jjj, iii, jjj]
                area[iii][jjj] = -1
                return (iii, jjj)
            v[iii][jjj] = True
            q.append([iii, jjj])

def move_people():

    store_arrived = []

    for n in range(M):
        if store_list[n][2] or len(people_info[n]) == 0: ## 편의점에 도착했을 경우
            continue
        i, j, _, _ = people_info[n]
        q = deque([])
        v = [[False for _ in range(N)] for _ in range(N)]
        q.append((i, j, []))

        final_route = []
        is_break = False
        while q :
            ii, jj, route = q.popleft()

            for d in range(4):
                iii = ii + dy[d]
                jjj = jj + dx[d]

                if iii < 0 or jjj < 0 or iii >= N or jjj >= N or v[iii][jjj]:
                    continue
                if area[iii][jjj] == -1:
                    continue
                if iii == store_list[n][0] and jjj == store_list[n][1] :
                    is_break = True
                    route.append((iii, jjj))
                    final_route = route
                    break

                route_ = route[:]
                route_.append((iii, jjj))
                q.append((iii, jjj, route_))
                v[iii][jjj] = True

            if is_break :
                break
        if final_route[0][0] == store_list[n][0] and final_route[0][1] == store_list[n][1]  :
            store_arrived.append(n)

        people_info[n][0] = final_route[0][0]
        people_info[n][1] = final_route[0][1]
    return store_arrived

def update_store_arrived(store_arrived):
    for n in store_arrived:
        store_list[n][2] = True
        i, j = store_list[n][0], store_list[n][1]
        area[i][j] = -1

def is_all_arrived():
    for s in store_list :
        _, _, is_arrived = s
        if not is_arrived :
            return False
    return True

dy = [-1, 0, 0, 1]
dx = [0, -1, 1, 0]

N, M = map(int, input().split())
area = [list(map(int, input().split())) for _ in range(N)]
store_list = [list(map(int, input().split())) for _ in range(M)]
for i in range(M):
    store_list[i][0] -=1
    store_list[i][1] -=1
    store_list[i].append(False)
people_info = [[] for _ in range(M)]
time = 0
while True :

    time +=1
    ## 사람 모두 이동
    store_arrived = move_people()
    ## 도착 편의점 정보 Update
    update_store_arrived(store_arrived)

    if time <= M :

        ## 베캠 서치 & 베캠으로 이동
        search_nearest_basecamp(time-1)

    ## 편의점 모두 도착인지 판별
    if is_all_arrived():
        break
print(time)