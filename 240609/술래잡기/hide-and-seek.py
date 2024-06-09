import sys
from collections import deque
import copy

def print_2d(a):
    for i in a :
        for j in i :
            print(j, end=' ')
        print()
    print('===')
def have_to_escape(i, j, r, c):
    if abs(i-r) + abs(j-c)  <= 3 :
        return True
    else :
        return False
def move_escapers(escapers):
    new_escapers = [[deque() for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if have_to_escape(i, j, follower[0], follower[1]):
                while escapers[i][j] :
                    d = escapers[i][j].popleft()
                    ii = i + dy[d]
                    jj = j + dx[d]

                    if ii < 0 or jj < 0 or ii >=N or jj >=N :
                        d = (d+2) % 4
                        ii = i + dy[d]
                        jj = j + dx[d]
                        if not (follower[0] == ii and follower[1] == jj) :
                            new_escapers[ii][jj].append(d)
                        else :
                            new_escapers[i][j].append(d)

                    else :
                        if not (follower[0] == ii and follower[1] == jj) :
                            new_escapers[ii][jj].append(d)
                        else :
                            new_escapers[i][j].append(d)
            else :
                new_escapers[i][j].extend(escapers[i][j])
    return new_escapers

def move_follower(dists, dirs, remain_dist):
    i, j, d = follower

    ii = i + dy[d]
    jj = j + dx[d]

    follower[0], follower[1] = ii, jj

    remain_dist -= 1

    if remain_dist == 0 :
        if len(dists) != 0 :
            remain_dist = dists.popleft()
            follower[2] = dirs.popleft()
        else :
            if ii == 0 and jj == 0 :
                dists = copy.deepcopy(standard_dists_reverse)
                dirs = copy.deepcopy(standard_dirs_reverse)

                remain_dist = dists.popleft()
                follower[2] = dirs.popleft()
            elif ii == N//2 and jj == N//2 :
                dists = copy.deepcopy(standard_dists)
                dirs = copy.deepcopy(standard_dirs)

                remain_dist = dists.popleft()
                follower[2] = dirs.popleft()

    return follower, remain_dist, dists, dirs


def catch_escapers(k, escapers):
    global answer
    i, j, d = follower
    for dist in range(3):
        ii = i + dy[d] * dist
        jj = j + dx[d] * dist

        if ii < 0 or jj < 0 or ii >=N or jj >=N :
            continue
        if trees[ii][jj] :
            continue

        answer += k * len(escapers[ii][jj])
        escapers[ii][jj] = deque()

    return escapers


dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]


N, M, H, K = map(int, input().split())
escapers = [[deque() for _ in range(N)]for _ in range(N)]
trees = [[0 for _ in range(N)]for _ in range(N)]
follower = [N//2, N//2, 0]
answer = 0
for _ in range(M):
    x, y, d = map(int, input().split())
    escapers[x-1][y-1].append(d)

for _ in range(H):
    x, y = map(int, input().split())
    trees[x-1][y-1] = 1

dists = deque()
dirs = deque()

for i in range(1, N):
    dists.append(i)
    dists.append(i)
dists.append(i)

for i in range(2*N-1):
    dirs.append(i % 4)

standard_dists = copy.deepcopy(dists)
standard_dirs = copy.deepcopy(dirs)
standard_dists_reverse = deque(reversed(standard_dists))
standard_dirs_reverse = deque((d+2) % 4 for d in list(reversed(standard_dirs)))
remain_dist = dists.popleft()
dirs.popleft()

for k in range(1,K+1):
    escapers = move_escapers(escapers)
    follower, remain_dist, dists, dirs = move_follower(dists, dirs, remain_dist)
    escapers = catch_escapers(k,escapers)

print(answer)