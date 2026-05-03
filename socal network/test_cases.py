"""
test_cases.py - Unit Tests for Social Network Explorer
Run with: python test_cases.py
"""

import sys
from profiles import ProfileManager
from graph import SocialGraph
from bfs_dfs import bfs_shortest_path, dfs_explore
from sorting import recommend_friends, _common_interests_count, _haversine_km


def run_test(name, passed, details=""):
    status = "PASS ✓" if passed else "FAIL ✗"
    print(f"  [{status}] {name}" + (f" — {details}" if details else ""))
    return passed


def setup():
    """Create a small test graph:
    alice - bob - carol
      |           |
    dave        frank
      |
    eve
    """
    pm = ProfileManager()
    sg = SocialGraph()

    pm.add_user("alice", "Alice", 22, ["music", "coding", "travel"], "Delhi")
    pm.add_user("bob",   "Bob",   25, ["travel", "hiking"],          "Mumbai")
    pm.add_user("carol", "Carol", 23, ["coding", "gaming", "music"], "Bangalore")
    pm.add_user("dave",  "Dave",  28, ["hiking", "cooking"],         "Delhi")
    pm.add_user("frank", "Frank", 30, ["coding", "AI"],              "Bangalore")
    pm.add_user("eve",   "Eve",   21, ["music", "art"],              "Chennai")

    for uid in ["alice","bob","carol","dave","frank","eve"]:
        sg._ensure_node(uid)

    sg.add_friendship("alice", "bob")
    sg.add_friendship("alice", "dave")
    sg.add_friendship("bob",   "carol")
    sg.add_friendship("carol", "frank")
    sg.add_friendship("dave",  "eve")

    return pm, sg


def test_profiles():
    print("\n── Profile Tests ──────────────────────────────")
    pm, _ = setup()
    results = []

    # Add duplicate
    r = pm.add_user("alice", "Alice2", 22, [], "")
    results.append(run_test("Reject duplicate user", r == False))

    # Get profile
    p = pm.get_profile("alice")
    results.append(run_test("Get existing profile", p is not None and p.name == "Alice"))

    # Get missing profile
    p2 = pm.get_profile("nobody")
    results.append(run_test("Get missing profile returns None", p2 is None))

    # Update profile
    pm.update_profile("alice", age=30, interests=["AI", "music"])
    p3 = pm.get_profile("alice")
    results.append(run_test("Update age", p3.age == 30))
    results.append(run_test("Update interests", "AI" in p3.interests))

    # Update missing profile
    r2 = pm.update_profile("ghost", name="Ghost")
    results.append(run_test("Update missing profile returns False", r2 == False))

    return all(results)


def test_graph():
    print("\n── Graph Tests ────────────────────────────────")
    _, sg = setup()
    results = []

    # Friends
    friends_alice = sg.get_friends("alice")
    results.append(run_test("Alice friends contain bob", "bob" in friends_alice))
    results.append(run_test("Alice friends contain dave", "dave" in friends_alice))

    # Bidirectional
    friends_bob = sg.get_friends("bob")
    results.append(run_test("Friendship is bidirectional (bob knows alice)", "alice" in friends_bob))

    # Remove friendship
    sg.add_friendship("alice", "carol")
    sg.remove_friendship("alice", "carol")
    results.append(run_test("Removed friendship gone from alice", "carol" not in sg.get_friends("alice")))
    results.append(run_test("Removed friendship gone from carol", "alice" not in sg.get_friends("carol")))

    # Duplicate removal
    r = sg.add_friendship("alice", "bob")
    results.append(run_test("Reject duplicate friendship", r == False))

    # Follow
    sg.add_follow("alice", "frank")
    results.append(run_test("Follow: alice follows frank", "frank" in sg.get_following("alice")))
    results.append(run_test("Follow: frank has alice as follower", "alice" in sg.get_followers("frank")))

    sg.remove_follow("alice", "frank")
    results.append(run_test("Unfollow removes from following", "frank" not in sg.get_following("alice")))

    return all(results)


def test_bfs():
    print("\n── BFS Tests ──────────────────────────────────")
    _, sg = setup()
    results = []

    # Direct connection
    path = bfs_shortest_path(sg, "alice", "bob")
    results.append(run_test("Direct path alice→bob", path == ["alice", "bob"],
                             f"got {path}"))

    # Two hops
    path2 = bfs_shortest_path(sg, "alice", "carol")
    results.append(run_test("Two-hop path alice→carol length=3", len(path2) == 3,
                             f"got {path2}"))
    results.append(run_test("Two-hop path passes through bob", "bob" in path2))

    # Three hops
    path3 = bfs_shortest_path(sg, "alice", "frank")
    results.append(run_test("Three-hop path alice→frank length=4", len(path3) == 4,
                             f"got {path3}"))

    # Same node
    path4 = bfs_shortest_path(sg, "alice", "alice")
    results.append(run_test("Same node path length=1", path4 == ["alice"]))

    # No path (isolated node scenario)
    sg._ensure_node("isolated")
    path5 = bfs_shortest_path(sg, "alice", "isolated")
    results.append(run_test("No path returns None", path5 is None))

    return all(results)


def test_dfs():
    print("\n── DFS Tests ──────────────────────────────────")
    _, sg = setup()
    results = []

    # Depth 1 = direct friends only
    d1 = dfs_explore(sg, "alice", 1)
    results.append(run_test("DFS depth=1 finds bob", "bob" in d1))
    results.append(run_test("DFS depth=1 finds dave", "dave" in d1))
    results.append(run_test("DFS depth=1 does NOT find carol (2 hops)", "carol" not in d1))

    # Depth 2 = friends of friends
    d2 = dfs_explore(sg, "alice", 2)
    results.append(run_test("DFS depth=2 finds carol", "carol" in d2))
    results.append(run_test("DFS depth=2 finds eve", "eve" in d2))
    results.append(run_test("DFS depth=2 depth of carol == 2", d2.get("carol") == 2))

    # Depth 3
    d3 = dfs_explore(sg, "alice", 3)
    results.append(run_test("DFS depth=3 finds frank", "frank" in d3))
    results.append(run_test("DFS depth=3 depth of frank == 3", d3.get("frank") == 3))

    # Start node not in result
    results.append(run_test("Start node not in DFS result", "alice" not in d3))

    return all(results)


def test_sorting():
    print("\n── Recommendation/Sorting Tests ───────────────")
    pm, sg = setup()
    results = []

    # Common interests
    pa = pm.get_profile("alice")   # music, coding, travel
    pc = pm.get_profile("carol")   # coding, gaming, music
    count, common = _common_interests_count(pa, pc)
    results.append(run_test("Alice & Carol have 2 common interests", count == 2,
                             f"got {count}: {common}"))

    # No interests in common
    pb = pm.get_profile("bob")     # travel, hiking
    pf = pm.get_profile("frank")   # coding, AI
    count2, _ = _common_interests_count(pb, pf)
    results.append(run_test("Bob & Frank have 0 common interests", count2 == 0))

    # Recommendations: carol should rank high for alice (2 common interests)
    recs = recommend_friends("alice", sg, pm, top_n=5)
    rec_ids = [r["user_id"] for r in recs]
    results.append(run_test("carol in alice's recommendations", "carol" in rec_ids))
    results.append(run_test("frank in alice's recommendations", "frank" in rec_ids))

    # Friends should NOT appear in recommendations
    results.append(run_test("bob NOT in alice's recs (already friend)", "bob" not in rec_ids))
    results.append(run_test("dave NOT in alice's recs (already friend)", "dave" not in rec_ids))

    # Top recommendation has most common interests
    if recs:
        results.append(run_test("Top rec has >= 1 common interest with alice",
                                 recs[0]["common_interests"] >= 1))

    # Haversine
    dist = _haversine_km("Delhi", "Mumbai")
    results.append(run_test("Delhi→Mumbai ~1150 km", 1100 < dist < 1200,
                             f"got {dist:.1f} km"))

    return all(results)


def main():
    print("\n╔══════════════════════════════════════════════╗")
    print("║   Social Network Explorer — Test Suite      ║")
    print("╚══════════════════════════════════════════════╝")

    suites = [
        ("Profiles",        test_profiles),
        ("Graph",           test_graph),
        ("BFS",             test_bfs),
        ("DFS",             test_dfs),
        ("Sorting/Recs",    test_sorting),
    ]

    overall = []
    for name, fn in suites:
        ok = fn()
        overall.append(ok)
        print(f"  Suite '{name}': {'ALL PASSED ✓' if ok else 'SOME FAILED ✗'}")

    print("\n" + "═" * 48)
    if all(overall):
        print("  ALL TESTS PASSED ✓")
    else:
        failed = [n for (n, _), ok in zip(suites, overall) if not ok]
        print(f"  FAILED SUITES: {', '.join(failed)}")
    print("═" * 48 + "\n")

    return 0 if all(overall) else 1


if __name__ == "__main__":
    sys.exit(main())
