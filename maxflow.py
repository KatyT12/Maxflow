import csv
from collections import deque



# Convert a list of edges to an adjacency list for convenience
def get_graph(edges):
    g = {}
    for (u,v) in edges:
        if not(u in g.keys()):
            g[u] = [v]
        else:
            g[u].append(v)
        if not (v in g.keys()):
            g[v] = []
    return g

# Find a shortest path from source (s) to sink (t)
def shortest_path(h,s,t):
    s = str(s)
    # Preprocessing
    visited = {}
    come_from = {}
    for u in h.keys():
        visited[u] = False
        come_from[u] = None
    visited[s] = True # Shouldn't be necessary
    q = deque([s])

    # Search
    while q:
        v = q.popleft()
        if v == t:
            break
        for u in h[v]:
            if not visited[u]:
                q.append(u)
                visited[u] = True
                come_from[u] = v

    if visited[t] == False:
        return None
    else:
        # Backtracking
        last = t
        path = [t]
        while last != s:
            v = come_from[last]
            path = [v] + path
            last = v
        return path



def find_augmenting_path(c,f,g,s,t):
    augmented_graph = {}
    augmented_graph[str(s)] =[]
    augmented_graph[str(t)] = []
    edges = {}
    for u,v in c.keys():
        if u not in augmented_graph.keys():
            augmented_graph[u] = []
        if v not in augmented_graph.keys():
            augmented_graph[v] = []
            
        if f[(u,v)] < c[(u,v)]:
            edges[(u,v)] = "Inc"
            augmented_graph[u].append(v)
        if f[(u,v)] > 0:
            augmented_graph[v].append(u)
            edges[(v,u)] = "Dec"
    path = shortest_path(augmented_graph,s,t)
    return path, augmented_graph, edges

# Find a minimum cut
def find_cut(g,s):
    visited = {}
    for v in g.keys():
        visited[v] = False
    visited[s] = True
    cut = set(s)
    stack = deque([s])

    while stack:
        u = stack.pop()
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                cut.add(v)
                stack.append(v)
    return cut


def compute_max_flow(capacity, s, t):
    print(capacity)
    # Preprocessing
    flow = {(u,v) : 0 for u,v in capacity}
    flow_value = 0
    g = get_graph(capacity)

    while True:
        path,augmented, h = find_augmenting_path(capacity,flow,g,s,t)
        if path == None:
            cut = find_cut(augmented,s)
            # Assert cut capacity equal to flow value
            return(flow_value,flow,cut)
        else:
            delta = float('Inf')
            # Find max possible delta
            for i in range(len(path) - 1):
                prev = path[i]
                next = path[i+1]
                if h[(prev,next)] == "Inc":
                    delta = min(delta, capacity[(prev,next)]- flow[(prev,next)])
                else:
                    delta = min(delta,flow[(next,prev)])

            # Now apply delta
            flow_value += delta
            for i in range(len(path)-1):
                prev = path[i]
                next = path[i+1]
                if h[(prev,next)] == "Inc":
                    flow[(prev,next)] += delta
                else:
                    flow[(next,prev)] -= delta
                # Assert: still a valid flow

"""
with open('flownetwork_02.csv') as f:
    rows = [row for row in csv.reader(f)][1:]
capacity = {(u, v): int(c) for u,v,c in rows}
f, fv, set = compute_max_flow(capacity,'0','5')
print(f,fv,set)
"""

capacity = {('0', '2'): 5, ('0', '5'): 5, ('1', '4'): 4, ('2', '4'): 5, ('4', '1'): 3, ('4', '3'): 1, ('5', '2'): 2, ('5', '3'): 3,
            ('5', '4'): 2, ('6', '8'): 3, ('8', '4'): 1, ('8', '7'): 3, ('9', '1'): 2, ('9', '10'): 5, ('7', '10'): 4, ('10', '0'): 3}
# 0 -> 10
# edge 0 -> 2
f, fv, cut = compute_max_flow(capacity,'0','10')
print(f,fv,cut)