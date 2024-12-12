from typing import List, Deque, Optional, Set, Tuple
from collections import deque
from dataclasses import dataclass
from time import perf_counter
from glob import glob


# O(1) should be as none of this depends on the input size
@dataclass
class State:
    pos_a: int
    pos_b: int
    t: int
    prev: Optional["State"]
    A_to_move: bool

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


# O(T) as there are at most T steps in the path
def backtrack(s: State) -> List[tuple[int, int]]:
    # indexing by plus 1 to go back to 1 based output
    path: List[tuple[int, int]] = [(s.pos_a + 1, s.pos_b + 1)]
    curr: State = s
    # need to reduce this by checking only every second move
    while curr.prev:
        prev: State = curr.prev
        path.append((prev.pos_a + 1, prev.pos_b + 1))
        curr = prev

    print((path))

    # all even pos in the path
    if len(path) % 2 == 1:
        path = [pos for i, pos in enumerate(path) if i % 2 == 0]
    else:
        path = [pos for i, pos in enumerate(path) if i % 2 == 1]

    return path[::-1]  # O(n) for reversal of list


def check(value, path) -> bool:

    if value != len(path) - 1:
        return False

    # decrementation happens to go back to 0 indexing
    for a, b in path:
        a -= 1
        b -= 1
        if dist[a][b] <= D:
            return False
    return True


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
            end_state: State

            if not s.A_to_move:
                print("hit")
                end_state = State(t_a, t_b, s.t + 1, s, True)
                best_t = s.t + 1
            else:
                end_state = s
                best_t = s.t
            break
        if s.t >= T:
            break
        a, b = s.pos_a, s.pos_b

        if s.A_to_move:
            for next_a in [a] + adj[a]:
                if State(next_a, b, s.t + 1, s, False) not in visited:
                    new_state_A: State = State(next_a, b, s.t, s, False)
                    visited.add(new_state_A)
                    queue.append(new_state_A)

        else:
            for next_b in [b] + adj[b]:
                if dist[a][next_b] > D:
                    if State(a, next_b, s.t + 1, s, True) not in visited:
                        new_state_B: State = State(a, next_b, s.t + 1, s, True)
                        queue.append(new_state_B)
                        visited.add(new_state_B)

    for state in visited:
        if state.pos_a == 17 and state.pos_b == 34:
            print(f" reached ({state.pos_a}, {state.pos_b}) at time {state.t}")
    if found:
        path: List[tuple[int, int]] = backtrack(end_state)
        return True, best_t, path
    else:
        return False, T + 1, []


if __name__ == "__main__":

    path = "testcases/grid25-4-randomized.in"

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

    found, steps, path = bfs(adj, dist, State(s_a, s_b, 0, None, True), t_a, t_b)

    time_end: float = perf_counter()
    time: float = time_end - time_begin

    if found:
        print()
        print(steps)
        print(" ".join(str(t[0]) for t in path))
        print(" ".join(str(t[1]) for t in path))
        print(f"{time:.2f} seconds")
    else:
        print()
        print(T + 1)
        print(f"{time:.2f} seconds")

    print(check(steps, path))
