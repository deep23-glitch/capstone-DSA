"""
graph.py - Social Network Graph
Data Structure: Adjacency List (dict of sets) for efficient O(1) edge operations.
Supports both undirected (friendships) and directed (followers) edges.
"""

class SocialGraph:
    """
    Adjacency List representation of the social network.

    - add_friendship   : undirected edge (both directions)
    - add_follow       : directed edge (follower -> followee)
    - remove_friendship: removes both directions
    - remove_follow    : removes single direction

    Space Complexity : O(V + E) where V = users, E = connections
    Edge Add/Remove  : O(1) average (using sets)
    Get Friends      : O(degree(v))
    """

    def __init__(self):
        self._adj = {}       # user_id -> set of connected user_ids (undirected friends)
        self._followers = {} # user_id -> set of follower user_ids (directed)
        self._following = {} # user_id -> set of users this user follows (directed)

    # ─── Internal helpers ───────────────────────────────────────────────────────

    def _ensure_node(self, user_id):
        if user_id not in self._adj:
            self._adj[user_id] = set()
        if user_id not in self._followers:
            self._followers[user_id] = set()
        if user_id not in self._following:
            self._following[user_id] = set()

    # ─── Friendship (undirected) ─────────────────────────────────────────────

    def add_friendship(self, u, v):
        """Add bidirectional friendship edge. O(1) average."""
        self._ensure_node(u)
        self._ensure_node(v)
        if v in self._adj[u]:
            print(f"[!] '{u}' and '{v}' are already friends.")
            return False
        self._adj[u].add(v)
        self._adj[v].add(u)
        print(f"[+] Friendship: {u} ↔ {v}")
        return True

    def remove_friendship(self, u, v):
        """Remove bidirectional friendship. O(1) average."""
        self._ensure_node(u)
        self._ensure_node(v)
        if v not in self._adj[u]:
            print(f"[!] '{u}' and '{v}' are not friends.")
            return False
        self._adj[u].discard(v)
        self._adj[v].discard(u)
        print(f"[-] Friendship removed: {u} ✗ {v}")
        return True

    def get_friends(self, user_id):
        """Return set of friends. O(1)."""
        self._ensure_node(user_id)
        return set(self._adj[user_id])

    # ─── Follow (directed) ────────────────────────────────────────────────────

    def add_follow(self, follower, followee):
        """follower starts following followee. O(1) average."""
        self._ensure_node(follower)
        self._ensure_node(followee)
        self._following[follower].add(followee)
        self._followers[followee].add(follower)
        print(f"[+] Follow: {follower} → {followee}")
        return True

    def remove_follow(self, follower, followee):
        """follower unfollows followee. O(1) average."""
        self._ensure_node(follower)
        self._ensure_node(followee)
        self._following[follower].discard(followee)
        self._followers[followee].discard(follower)
        print(f"[-] Unfollow: {follower} ✗→ {followee}")
        return True

    def get_followers(self, user_id):
        self._ensure_node(user_id)
        return set(self._followers[user_id])

    def get_following(self, user_id):
        self._ensure_node(user_id)
        return set(self._following[user_id])

    # ─── Utilities ────────────────────────────────────────────────────────────

    def are_friends(self, u, v):
        self._ensure_node(u)
        return v in self._adj[u]

    def all_nodes(self):
        return list(self._adj.keys())

    def display_connections(self, user_id):
        friends = self.get_friends(user_id)
        following = self.get_following(user_id)
        followers = self.get_followers(user_id)
        print(f"\n  Connections for '{user_id}':")
        print(f"    Friends   : {', '.join(friends) if friends else 'None'}")
        print(f"    Following : {', '.join(following) if following else 'None'}")
        print(f"    Followers : {', '.join(followers) if followers else 'None'}")
