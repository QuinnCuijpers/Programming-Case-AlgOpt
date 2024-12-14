from typing import List, Deque, Optional, Set, Tuple
from collections import deque
from dataclasses import dataclass
from time import perf_counter
from glob import glob

"""
File to check if all .in files that find a solution (yes-instance) has the correct amount of steps.
checks every file, so can take a while to run.
"""


@dataclass
class State:
    pos_a: int
    pos_b: int
    t: int
    prev: Optional["State"]
    A_to_move: bool

    def __hash__(self) -> int:
        return hash(tuple((self.pos_a, self.pos_b)))

    def __eq__(self, other) -> bool:
        return (
            self.pos_a == other.pos_a
            and self.pos_b == other.pos_b
            and self.A_to_move == other.A_to_move
        )

    def __repr__(self) -> str:
        return f"({self.pos_a}, {self.pos_b}) at time {self.t}"


def bfs_dist(adj_matrix) -> List[List[int]]:
    n: int = len(adj_matrix)
    dist_matrix: List[List[int]] = [[-1] * n for _ in range(n)]

    for start in range(n):
        queue = deque([(start, 0)])
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


def backtrack(s: State) -> List[tuple[int, int]]:
    path: List[tuple[int, int]] = [(s.pos_a + 1, s.pos_b + 1)]
    curr: State = s
    while curr.prev:
        prev: State = curr.prev
        path.append((prev.pos_a + 1, prev.pos_b + 1))
        curr = prev

    if len(path) % 2 == 1:
        path = [pos for i, pos in enumerate(path) if i % 2 == 0]
    else:
        path = [pos for i, pos in enumerate(path) if i % 2 == 1]

    return path[::-1]


def check(value, path, file) -> bool:

    file = file[0:-3] + ".out"

    with open(file, "r") as f:
        true_value = int(f.readline())

    if value != true_value:
        return False

    for a, b in path:
        a -= 1
        b -= 1
        if dist[a][b] <= D:
            return False
    return True


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

    if found:
        path: List[tuple[int, int]] = backtrack(end_state)
        return True, best_t, path
    else:
        return False, T + 1, []


if __name__ == "__main__":
    time_begin: float = perf_counter()
    paths: list[str] = glob("testcases/*.in")

    print(len(paths))

    for i, path in enumerate(paths):

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
                a -= 1
                b -= 1

                adj[a].append(b)
                adj[b].append(a)

        dist: List[List[int]] = bfs_dist(adj)

        found, steps, path = bfs(adj, dist, State(s_a, s_b, 0, None, True), t_a, t_b)

        time_end: float = perf_counter()
        time: float = time_end - time_begin

        if found:
            if not check(steps, path, file.name):
                print(file.name)
            else:
                print(f"{((i+1)/len(paths))*100:.2f}% there")
