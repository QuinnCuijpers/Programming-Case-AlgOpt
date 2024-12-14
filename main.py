from typing import List, Deque, Optional, Set
from collections import deque
from dataclasses import dataclass
from time import perf_counter


# dataclass auto generates an initializer for the class
@dataclass
# a class that holds a possible state for the game.
# it contains a position for player a and player b, which is the vertex the player is at
# t denotes the time of the state, every time both players move the time increments by 1
# prev denotes the parent state
# A_to_move is a boolean that denotes whose turn it is to move
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


# bfs search to find the shortest distance from all nodes to all other nodes
def bfs_dist(adj_matrix) -> List[List[int]]:
    n: int = len(adj_matrix)
    dist_matrix: List[List[int]] = [[-1] * n for _ in range(n)]

    for start in range(n):
        # BFS from node 'start'
        queue = deque([(start, 0)])  # (current_node, distance to start)

        # list that keeps track of whether a node was already visited
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


# method that given an endstate recreates the path to that state
def backtrack(s: State) -> List[tuple[int, int]]:
    # indexing by plus 1 to go back to 1 based output
    path: List[tuple[int, int]] = [(s.pos_a + 1, s.pos_b + 1)]
    curr: State = s

    # going through the chain of prev states and adding the positions onto the path
    # such that it creates a path from end till start
    while curr.prev:
        prev: State = curr.prev
        path.append((prev.pos_a + 1, prev.pos_b + 1))
        curr = prev

    # as the states are for half moves the path is for every second move
    # so the below code selects every 2nd element
    if len(path) % 2 == 1:
        path = path[::2]
    else:
        path = path[1::2]

    # returns the reversed path such that is from start till end state
    return path[::-1]


def check(value, path) -> bool:

    # the value returned should be 1 less than the length of the path
    if value != len(path) - 1:
        return False

    # checks if all distances on the path are larger than D
    for a, b in path:
        # decrementation happens to go back to 0 indexing
        a -= 1
        b -= 1
        if dist[a][b] <= D:
            return False
    return True


# bfs search through possible states where players move one at a time
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
            end_state: State = s
            if not s.A_to_move:
                end_state = State(t_a, t_b, s.t + 1, s, True)
                best_t = s.t + 1
            else:
                end_state = s
                best_t = s.t
            break

        # if a state is already in time T than there will be a solution with less than T steps
        if s.t >= T:
            break
        a, b = s.pos_a, s.pos_b

        if s.A_to_move:
            for next_a in [a] + adj[a]:
                if State(next_a, b, s.t, s, False) not in visited:
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

    # logic for whether a solution was found or not
    if found:
        path: List[tuple[int, int]] = backtrack(end_state)
        return True, best_t, path
    else:
        return False, T + 1, []


if __name__ == "__main__":

    # change path for different input file
    path = "testcases/grid10-2.in"

    # data reading
    with open(path, "r") as file:
        line1 = file.readline().split(" ")
        n, m, T, D = tuple(map(int, line1))

        adj: List[List[int]] = [[] for _ in range(n)]  # adj list representation of G
        line2 = file.readline().split(" ")
        s_a, t_a, s_b, t_b = tuple(map(int, line2))
        # decrementing values such that they are 0 based
        s_a -= 1
        t_a -= 1
        s_b -= 1
        t_b -= 1

        # creates an adj list for the graph
        for _ in range(m):
            a, b = tuple(map(int, file.readline().split(" ")))
            # decremeting to go from 1 based indexing to 0 based
            a -= 1
            b -= 1

            adj[a].append(b)
            adj[b].append(a)

    time_begin: float = perf_counter()
    dist: List[List[int]] = bfs_dist(adj)

    found, steps, path = bfs(adj, dist, State(s_a, s_b, 0, None, True), t_a, t_b)

    time_end: float = perf_counter()
    time: float = time_end - time_begin

    # output logic
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
