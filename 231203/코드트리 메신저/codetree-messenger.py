import sys

def make_tree_and_authorities(node_info):
    tree = {i:[None] for i in range(N+1)}
    for n in range(1, N+1):
        tree[n][0] = node_info[n]
        tree[node_info[n]].append(n)

    authorities=[None]
    for n in range(N+1, 2*N+1):
        authorities.append(node_info[n])
    return tree, authorities

def change_alarm(n):

    alarms[n] = not alarms[n]

    return alarms

def change_authority(n, power):
    authorities[n] = power

def change_nodes(a, b):

    tree[tree[a][0]].remove(a)
    tree[tree[a][0]].append(b)

    tree[tree[b][0]].remove(b)
    tree[tree[b][0]].append(a)
    #
    temp = tree[a][0]
    tree[a][0] = tree[b][0]
    tree[b][0] = temp


def calc_numChats(n, depth):
    global answer
    if not alarms[n] :
        return
    if authorities[n] >= depth :
        answer += 1

    for nn in tree[n][1:]:
        calc_numChats(nn, depth+1)
def print_numChats(n, depth):

    global answer
    for nn in tree[n][1:]:
        calc_numChats(nn, depth+1)
    print(answer)

def print_numChats2(n):
    from collections import deque
    global answer

    visited = [False for _ in range(N+1)]

    q = deque([])
    for i in range(len(tree[n])-1):
        q.append([tree[n][i+1], 1])
    while q :
        nn, depth = q.pop()
        if not alarms[nn]:
            continue
        if authorities[nn] >= depth :
            answer += 1
        for nnn in tree[nn][1:]:
            if not visited[nnn] :
                q.append([nnn, depth+1])
                visited[nnn] = True

    print(answer)




N, Q = map(int, input().split())
node_info = list(map(int, input().split()))
tree, authorities = make_tree_and_authorities(node_info)
alarms = [True for _ in range(N+1)]
answer = 0
for qs in range(Q-1) :
    q = list(map(int, input().split()))

    if q[0] == 200 :
        change_alarm(q[1])
    elif q[0] == 300 :
        change_authority(q[1], q[2])
    elif q[0] == 400 :
        change_nodes(q[1], q[2])
    elif q[0] == 500 :
        print_numChats2(q[1])
        answer = 0
    # if qs == 4 :
    #     break