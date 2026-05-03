# Social Network Explorer — Design Report

## 1. Module Overview

| Module | Responsibility | Key DS Used |
|---|---|---|
| `profiles.py` | User CRUD | Hash Map (`dict`) + Lists |
| `graph.py` | Network edges | Adjacency List (`dict` of `set`) |
| `bfs_dfs.py` | Traversal | Queue (BFS), Stack (DFS) |
| `sorting.py` | Recommendations | Set intersection + Sorting |
| `main.py` | CLI + Demo | Orchestration |
| `test_cases.py` | Validation | Unit tests |

---

## 2. Data Structure Decisions

### 2.1 Profile Manager — Hash Map
- **Choice**: Python `dict` (hash table), user_id → UserProfile object
- **Why**: O(1) average-case for `add`, `get`, `update`
- **Trade-off**: O(n) memory; hash collisions degrade to O(n) worst case (rare with good hash)
- Interests stored as Python `list` (array); converted to `set` for O(1) intersection during recommendations

### 2.2 Social Graph — Adjacency List (`dict` of `set`)
- **Choice**: `dict[str, set[str]]` rather than adjacency matrix
- **Why**: Sparse graph (real social networks: avg degree << n). Matrix = O(V²) space; list = O(V + E)
- Edge insertion/deletion: O(1) average (set operations)
- Neighbour enumeration: O(degree(v))
- **Friendship** = undirected (maintained in both directions)
- **Follow** = directed (separate `_followers` / `_following` dicts)

### 2.3 BFS Queue — `collections.deque`
- **Choice**: `deque` over `list` for the BFS frontier
- **Why**: `list.pop(0)` is O(n); `deque.popleft()` is O(1)
- Path tracked as list appended at each step; overall BFS: O(V + E)

### 2.4 DFS Stack — Python `list`
- **Choice**: Iterative DFS with explicit stack avoids Python recursion limit
- Stack `append`/`pop` are both O(1)
- Visited dict stores depth at discovery for depth-level grouping
- Time: O(V + E), bounded by depth in practice

### 2.5 Recommendation Sorting — Set Intersection + `sorted()`
- Common interests: `set(a.interests) & set(b.interests)` → O(min(|A|,|B|))
- Candidates scored then sorted with Python Timsort: O(n log n)
- Multi-key sort: (-common_interests, -mutual_friends, name) for stable, deterministic ranking

### 2.6 Geo-Proximity — K-D Tree (conceptual) / Linear Scan (demo)
- **Conceptual choice**: K-D Tree partitions 2D lat/lon space
  - Nearest neighbour: O(log n) average vs O(n) linear scan
  - Range query: O(√n + k) where k = results returned
- **Demo implementation**: Linear scan with Haversine distance formula (O(n))
- **Production recommendation**: `scipy.spatial.KDTree` for large user bases

---

## 3. Complexity Summary

| Operation | Time | Space |
|---|---|---|
| add_user | O(1) avg | O(1) |
| get_profile | O(1) avg | O(1) |
| update_profile | O(1) avg | O(1) |
| add_friendship | O(1) avg | O(1) |
| remove_friendship | O(1) avg | O(1) |
| get_friends | O(1) | O(degree) |
| BFS shortest path | O(V + E) | O(V) |
| DFS explore (depth d) | O(V + E) bounded | O(V) |
| Friend recommendations | O(n · k) | O(n) |
| Geo nearby (linear) | O(n) | O(n) |
| Geo nearby (K-D Tree) | O(log n) | O(n) |

*V = vertices (users), E = edges (connections), n = user count, k = avg interests*

---

## 4. Design Decisions

### Undirected vs Directed Edges
Implemented both: `add_friendship` (undirected, mutual) and `add_follow` (directed). This mirrors real platforms (Facebook friends vs Instagram follows).

### DFS Iterative vs Recursive
Chose iterative to avoid Python's default recursion limit (1000). With depth=3 and a dense graph, recursive DFS could hit this limit.

### Separation of Path Storage in BFS
Each queue entry carries its full path as a list. Memory cost: O(V · avg_path_length). Alternative is parent-pointer backtracking (O(V) space), chosen simplicity over micro-optimization given small n.

### Recommendation Multi-Key Sort
Sorting by (-common_interests, -mutual_friends, name) uses Python's stable Timsort and produces deterministic, reproducible rankings with no secondary-sort ambiguity.

### Module Isolation
Each file has a single responsibility and can be imported independently. `main.py` is the only file with cross-module imports, making unit testing clean and side-effect-free.

---

## 5. Checklist Verification

| Item | Status |
|---|---|
| 8 users added | ✓ (alice, bob, carol, dave, eve, frank, grace, heidi) |
| 2 profiles updated | ✓ (alice age+interests, frank location+interests) |
| 3+ profiles displayed | ✓ (alice, carol, dave, frank shown) |
| 8–12 connections | ✓ (10 friendships created) |
| 1 connection removed | ✓ (bob ↔ dave removed) |
| BFS query 1 | ✓ alice → frank |
| BFS query 2 | ✓ heidi → grace |
| DFS depth=2 | ✓ from alice |
| DFS depth=3 | ✓ from alice |
| Sorted recommendation list | ✓ by common interests + mutual friends |
| Bonus geo DS | ✓ K-D Tree concept + Haversine demo |
