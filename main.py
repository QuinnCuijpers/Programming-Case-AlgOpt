from typing import List, Deque, Optional, Set, Tuple
from collections import deque
from dataclasses import dataclass
from time import perf_counter


# O(1) should be as none of this depends on the input size
@dataclass
class State:
    pos_a: int
    pos_b: int
    t: int
    prev: Optional["State"]

    def __hash__(self) -> int:
        return hash(tuple({self.pos_a, self.pos_b}))

    def __eq__(self, other) -> bool:
        return self.pos_a == other.pos_a and self.pos_b == other.pos_b

    def __repr__(self) -> str:
        return f"({self.pos_a}, {self.pos_b}) at time {self.t}"


# O(n(n+m)) as it does a bfs (through adjacancy list) for all nodes
def bfs_dist(adj_matrix) -> List[List[int]]:
    n: int = len(adj_matrix)
    dist_matrix: List[List[int]] = [[-1] * n for _ in range(n)]

    for start in range(n):
        # BFS from node 'start'
        queue = deque([(start, 0)])  # (current_node, distance)
        visited: List[bool] = [False] * n
        visited[start] = True

        while queue:
            current, distance = queue.popleft()
            dist_matrix[start][current] = distance

            for neighbor in adj_matrix[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, distance + 1))

    return dist_matrix


# slow as it generates all pairs for both and uses deepcopy which is linear, total order O(m^2 + n)
def generate_neighbours(
    a: int, b: int, adj: List[List[int]], D: int
) -> List[tuple[int, int]]:

    neighbours_a: List[int] = adj[a] + [a]
    neighbours_b: List[int] = adj[b] + [b]

    # Generate pairs directly with filtering list comprehension
    results: List[Tuple[int, int]] = [
        (neighbour_a, neighbour_b)
        for neighbour_a in neighbours_a
        for neighbour_b in neighbours_b
        if dist[neighbour_a][neighbour_b] > D
    ]

    return results


# O(T) as there are at most T steps in the path
def backtrack(s: State) -> List[tuple[int, int]]:
    # indexing by plus 1 to go back to 1 based output
    path: List[tuple[int, int]] = [(s.pos_a + 1, s.pos_b + 1)]
    curr: State = s
    while curr.prev:
        prev: State = curr.prev
        path.append((prev.pos_a + 1, prev.pos_b + 1))
        curr = prev

    return path[::-1]  # O(n) for reversal of list


# O(n+O(GN))
def bfs(adj: List[List[int]], dist: List[List[int]], state: State, t_a: int, t_b: int):
    queue: Deque[State] = deque()
    visited: Set[State] = set()

    queue.append(state)
    visited.add(state)

    found = False
    best_t: int = T + 1
    while queue:
        s: State = queue.popleft()
        if s.pos_a == t_a and s.pos_b == t_b:
            found = True
            best_t = min(s.t, best_t)
            end_state: State = s
            break
        if s.t >= T:
            break
        a, b = s.pos_a, s.pos_b
        for a_n, b_n in generate_neighbours(a, b, adj, D):
            if State(a_n, b_n, s.t + 1, s) not in visited:
                new_state: State = State(a_n, b_n, s.t + 1, s)
                queue.append(new_state)
                visited.add(new_state)

    if found:
        path: List[tuple[int, int]] = backtrack(end_state)
        return True, best_t, path
    else:
        return False, T + 1, []


if __name__ == "__main__":
    path = "testcases/grid10-0-randomized.in"

    with open(path, "r") as file:
        line1 = file.readline().split(" ")
        n, m, T, D = tuple(map(int, line1))

        adj: List[List[int]] = [[] for _ in range(n)]
        line2 = file.readline().split(" ")
        s_a, t_a, s_b, t_b = tuple(map(int, line2))
        s_a -= 1
        t_a -= 1
        s_b -= 1
        t_b -= 1
        for _ in range(m):
            a, b = tuple(map(int, file.readline().split(" ")))
            # to go from 1 based indexing to 0 based
            a -= 1
            b -= 1

            adj[a].append(b)
            adj[b].append(a)

    time_begin: float = perf_counter()
    dist: List[List[int]] = bfs_dist(adj)

    found, steps, path = bfs(adj, dist, State(s_a, s_b, 0, None), t_a, t_b)

    time_end: float = perf_counter()
    time: float = time_end - time_begin

    if found:
        print(steps)
        print(" ".join(str(t[0]) for t in path))
        print(" ".join(str(t[1]) for t in path))
        print(f"{time:.2f} seconds")
    else:
        print(T + 1)
        print(f"{time:.2f} seconds")
