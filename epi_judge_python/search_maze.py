import collections
import copy
import functools
from typing import List, Tuple, Union, Optional, Dict

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

WHITE, BLACK = range(2)

Coordinate = collections.namedtuple('Coordinate', ('x', 'y'))


def search_maze(maze: List[List[int]], s: Coordinate,
                e: Coordinate) -> List[Coordinate]:
    # BFS from each side
    s_node, e_node = buildGraph(maze, s, e)
    visited = dict({})
    queue = []
    if s_node == None or e_node == None:
        return []
    # shortest_path = BFS_shortest_path(s_node, e_node, memo=visited, queue=queue)
    # if shortest_path == -1:
    #     return []
    # return [node.coords for node in shortest_path]
    path = DFS(s_node, e_node, memo=visited)
    if path == -1:
        return []
    return [node.coords for node in path]

class Node:

    def __init__(self, coords: Coordinate) -> None:
        self.edges = dict({
            "N": None,
            "S": None,
            "W": None,
            "E": None,
        })
        self.coords = coords


def buildGraph(maze: List[List[int]], s: Coordinate, e: Coordinate) -> Tuple[Node, Node]:
    graph = [[None for x in range(len(maze[0]))] for y in range(len(maze))]
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 0:
                path_node = Node(Coordinate(row, col))
                graph[row][col] = path_node
                if col - 1 >= 0 and graph[row][col-1] != None:
                    path_node.edges['W'] = graph[row][col-1]
                    graph[row][col - 1].edges['E'] = path_node
                if col + 1 < len(maze[0]) and graph[row][col+1] != None:
                    path_node.edges['E'] = graph[row][col+1]
                    graph[row][col + 1].edges['W'] = path_node
                if row + 1 < len(maze) and graph[row+1][col] != None:
                    path_node.edges['S'] = graph[row+1][col]
                    graph[row + 1][col].edges['N'] = path_node
                if row - 1 >= 0 and graph[row-1][col] != None:
                    path_node.edges['N'] = graph[row-1][col]
                    graph[row - 1][col].edges['S'] = path_node

    return graph[s[0]][s[1]], graph[e[0]][e[1]]


def BFS_shortest_path(start_node: Node, end_node: Node, memo: Optional[Dict] = None,
    queue: Optional[List] = None) -> Union[List, int]:
    queue.append([start_node])

    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if memo.get(vertex, False) != True:
            for neighbor in vertex.edges.values():
                if neighbor == None:
                    continue
                if neighbor == end_node:
                    path.append(end_node)
                    return path
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
            memo[vertex] = True

    return -1

def DFS(start_node: Node, end_node: Node, memo: Optional[Dict]=None) -> Union[List[Node], int]:
    memo[start_node] = True
    result = -1
    for neighbor in start_node.edges.values():
        if neighbor != None:
            if neighbor == end_node:
                return [start_node, end_node]
            elif memo.get(neighbor, False) != True:
                result = DFS(neighbor, end_node, memo=memo)
                if result != -1:
                    result.insert(0, start_node)
                    break
    return result

def path_element_is_feasible(maze, prev, cur):
    if not ((0 <= cur.x < len(maze)) and
            (0 <= cur.y < len(maze[cur.x])) and maze[cur.x][cur.y] == WHITE):
        return False
    return cur == (prev.x + 1, prev.y) or \
           cur == (prev.x - 1, prev.y) or \
           cur == (prev.x, prev.y + 1) or \
           cur == (prev.x, prev.y - 1)


@enable_executor_hook
def search_maze_wrapper(executor, maze, s, e):
    s = Coordinate(*s)
    e = Coordinate(*e)
    cp = copy.deepcopy(maze)

    path = executor.run(functools.partial(search_maze, cp, s, e))

    if not path:
        return s == e

    if path[0] != s or path[-1] != e:
        raise TestFailure('Path doesn\'t lay between start and end points')

    for i in range(1, len(path)):
        if not path_element_is_feasible(maze, path[i - 1], path[i]):
            raise TestFailure('Path contains invalid segments')

    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_maze.py', 'search_maze.tsv',
                                       search_maze_wrapper))
