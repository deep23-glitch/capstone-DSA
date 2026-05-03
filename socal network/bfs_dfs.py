"""
bfs_dfs.py - Graph Traversal Algorithms
BFS  : Shortest path (degrees of separation) between two users
DFS  : Friends-of-friends exploration up to depth d
"""

from collections import deque


# ═══════════════════════════════════════════════════════════════════════════════
#  BFS — Shortest Path (Degrees of Separation)
# ═══════════════════════════════════════════════════════════════════════════════

def bfs_shortest_path(graph, start, end):
    """
    Find shortest path from start to end using BFS on the friendship graph.

    Algorithm:
      1. Enqueue start node with path=[start]
      2. For each node dequeued, explore unvisited neighbours
      3. Return path when end is found; None if unreachable

    Time Complexity : O(V + E)
    Space Complexity: O(V) for visited set + queue

    Returns: list of user_ids representing path, or None if no path exists.
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque()
    queue.append((start, [start]))   # (current_node, path_so_far)

    while queue:
        current, path = queue.popleft()

        for neighbour in graph.get_friends(current):
            if neighbour == end:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None   # No path found


def print_bfs_result(graph, start, end):
    """Pretty-print BFS shortest path result."""
    print(f"\n  BFS Shortest Path: '{start}' → '{end}'")
    path = bfs_shortest_path(graph, start, end)
    if path is None:
        print(f"  [!] No connection found between '{start}' and '{end}'.")
    else:
        degrees = len(path) - 1
        print(f"  Path  : {' → '.join(path)}")
        print(f"  Degree of Separation: {degrees}")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
#  DFS — Friends-of-Friends Exploration up to Depth d
# ═══════════════════════════════════════════════════════════════════════════════

def dfs_explore(graph, start, max_depth):
    """
    Explore all users reachable from start within max_depth hops using DFS.

    Algorithm (iterative DFS with depth tracking):
      1. Push (start, 0) onto stack
      2. For each popped node at depth d < max_depth, push unvisited neighbours at d+1
      3. Collect all visited nodes except the start node itself

    Time Complexity : O(V + E) in worst case (bounded by depth in practice)
    Space Complexity: O(V) for visited set + stack

    Returns: dict mapping user_id -> depth_at_which_discovered
    """
    visited = {}          # user_id -> depth discovered
    stack = [(start, 0)]  # (node, current_depth)
    visited[start] = 0

    while stack:
        current, depth = stack.pop()

        if depth < max_depth:
            for neighbour in graph.get_friends(current):
                if neighbour not in visited:
                    visited[neighbour] = depth + 1
                    stack.append((neighbour, depth + 1))

    # Remove the start node from results
    discovered = {uid: d for uid, d in visited.items() if uid != start}
    return discovered


def print_dfs_result(graph, start, max_depth, profile_manager=None):
    """Pretty-print DFS exploration result grouped by depth."""
    print(f"\n  DFS Exploration from '{start}' (max depth={max_depth})")
    discovered = dfs_explore(graph, start, max_depth)

    if not discovered:
        print("  No users discovered within depth limit.")
        return discovered

    # Group by depth
    by_depth = {}
    for uid, d in discovered.items():
        by_depth.setdefault(d, []).append(uid)

    for depth in sorted(by_depth.keys()):
        label = "Friend" if depth == 1 else f"Depth-{depth} connection"
        users = by_depth[depth]
        names = []
        for uid in users:
            if profile_manager:
                p = profile_manager.get_profile(uid)
                names.append(p.name if p else uid)
            else:
                names.append(uid)
        print(f"    Depth {depth} ({label}s): {', '.join(names)}")

    print(f"  Total discovered: {len(discovered)} user(s)")
    return discovered
