"""
main.py - Social Network Explorer CLI
Integrates: ProfileManager, SocialGraph, BFS, DFS, Recommendations
"""

import sys
from profiles import ProfileManager
from graph import SocialGraph
from bfs_dfs import print_bfs_result, print_dfs_result
from sorting import print_recommendations, print_nearby

DIVIDER = "\n" + "═" * 60


def demo_run():
    """
    Automated demo satisfying the Minimum Demo Checklist:
      ✓ 8 users added, 2 profiles updated, 3+ profiles displayed
      ✓ 10 connections created, 1 removed
      ✓ 2 BFS shortest path queries
      ✓ DFS at depth=2 and depth=3
      ✓ Sorted recommendation list by common interests
      ✓ Bonus: Geo-proximity nearby users
    """
    pm = ProfileManager()
    sg = SocialGraph()

    # ── STEP 1: Add 8 Users ───────────────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 1 — Adding Users")
    print(DIVIDER)

    users = [
        ("alice",   "Alice Sharma",   22, ["music", "travel", "coding"],       "Delhi"),
        ("bob",     "Bob Mehta",      25, ["travel", "photography", "hiking"],  "Mumbai"),
        ("carol",   "Carol Iyer",     23, ["coding", "gaming", "music"],        "Bangalore"),
        ("dave",    "Dave Kapoor",    28, ["hiking", "travel", "cooking"],      "Delhi"),
        ("eve",     "Eve Nair",       21, ["music", "art", "cooking"],          "Chennai"),
        ("frank",   "Frank Bose",     30, ["coding", "AI", "gaming"],           "Kolkata"),
        ("grace",   "Grace Pillai",   26, ["photography", "travel", "art"],     "Hyderabad"),
        ("heidi",   "Heidi Joshi",    24, ["cooking", "music", "yoga"],         "Pune"),
    ]

    for uid, name, age, interests, location in users:
        pm.add_user(uid, name, age, interests, location)
        sg._ensure_node(uid)  # Register all nodes in graph

    # ── STEP 2: Update 2 Profiles ─────────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 2 — Updating Profiles")
    print(DIVIDER)

    pm.update_profile("alice", age=23, interests=["music", "travel", "coding", "AI"])
    pm.update_profile("frank", location="Bangalore", interests=["coding", "AI", "gaming", "robotics"])

    # ── STEP 3: Display 3+ Profiles ───────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 3 — Displaying Profiles")
    print(DIVIDER)

    for uid in ["alice", "carol", "dave", "frank"]:
        pm.display_profile(uid)

    # ── STEP 4: Create 10 Connections ─────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 4 — Creating Connections (Friendships)")
    print(DIVIDER)

    friendships = [
        ("alice", "bob"),
        ("alice", "carol"),
        ("alice", "dave"),
        ("bob",   "grace"),
        ("bob",   "dave"),
        ("carol", "frank"),
        ("carol", "eve"),
        ("dave",  "heidi"),
        ("eve",   "heidi"),
        ("frank", "grace"),
    ]

    for u, v in friendships:
        sg.add_friendship(u, v)

    # ── STEP 5: Remove 1 Connection ───────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 5 — Removing a Connection")
    print(DIVIDER)

    sg.remove_friendship("bob", "dave")

    # ── STEP 6: BFS Shortest Path Queries ────────────────────────────────────
    print(DIVIDER)
    print("  STEP 6 — BFS: Shortest Path (Degrees of Separation)")
    print(DIVIDER)

    print_bfs_result(sg, "alice", "frank")
    print_bfs_result(sg, "heidi", "grace")

    # ── STEP 7: DFS Exploration ───────────────────────────────────────────────
    print(DIVIDER)
    print("  STEP 7 — DFS: Friends-of-Friends Exploration")
    print(DIVIDER)

    print_dfs_result(sg, "alice", max_depth=2, profile_manager=pm)
    print_dfs_result(sg, "alice", max_depth=3, profile_manager=pm)

    # ── STEP 8: Friend Recommendations ───────────────────────────────────────
    print(DIVIDER)
    print("  STEP 8 — Friend Recommendations (Sorted by Common Interests)")
    print(DIVIDER)

    print_recommendations("alice", sg, pm, top_n=5)
    print_recommendations("frank", sg, pm, top_n=5)

    # ── BONUS: Geo-Proximity ──────────────────────────────────────────────────
    print(DIVIDER)
    print("  BONUS — Geo-Proximity (K-D Tree concept, linear scan for demo)")
    print(DIVIDER)

    print_nearby("alice", pm, radius_km=500)
    print_nearby("frank", pm, radius_km=800)

    print(DIVIDER)
    print("  DEMO COMPLETE — All checklist items satisfied.")
    print(DIVIDER)

    return pm, sg


# ═══════════════════════════════════════════════════════════════════════════════
#  Interactive CLI
# ═══════════════════════════════════════════════════════════════════════════════

def interactive_cli(pm, sg):
    MENU = """
  ┌─────────────────────────────────────┐
  │    Social Network Explorer CLI      │
  ├─────────────────────────────────────┤
  │  1. Add user                        │
  │  2. Get / Display profile           │
  │  3. Update profile                  │
  │  4. Add friendship                  │
  │  5. Remove friendship               │
  │  6. Show connections                │
  │  7. BFS shortest path               │
  │  8. DFS explore (depth)             │
  │  9. Friend recommendations          │
  │  10. Nearby users (geo)             │
  │  0. Exit                            │
  └─────────────────────────────────────┘"""

    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            uid = input("  User ID: ").strip()
            name = input("  Name: ").strip()
            age = int(input("  Age: ").strip())
            interests = [i.strip() for i in input("  Interests (comma-sep): ").split(",")]
            loc = input("  Location (city): ").strip()
            pm.add_user(uid, name, age, interests, loc)
            sg._ensure_node(uid)

        elif choice == "2":
            uid = input("  User ID: ").strip()
            pm.display_profile(uid)

        elif choice == "3":
            uid = input("  User ID: ").strip()
            name = input("  New name (Enter to skip): ").strip() or None
            age_str = input("  New age (Enter to skip): ").strip()
            age = int(age_str) if age_str else None
            ints_str = input("  New interests comma-sep (Enter to skip): ").strip()
            interests = [i.strip() for i in ints_str.split(",")] if ints_str else None
            loc = input("  New location (Enter to skip): ").strip() or None
            pm.update_profile(uid, name=name, age=age, interests=interests, location=loc)

        elif choice == "4":
            u = input("  User A ID: ").strip()
            v = input("  User B ID: ").strip()
            sg.add_friendship(u, v)

        elif choice == "5":
            u = input("  User A ID: ").strip()
            v = input("  User B ID: ").strip()
            sg.remove_friendship(u, v)

        elif choice == "6":
            uid = input("  User ID: ").strip()
            sg.display_connections(uid)

        elif choice == "7":
            src = input("  Source user ID: ").strip()
            dst = input("  Destination user ID: ").strip()
            print_bfs_result(sg, src, dst)

        elif choice == "8":
            uid = input("  Start user ID: ").strip()
            d = int(input("  Max depth: ").strip())
            print_dfs_result(sg, uid, d, pm)

        elif choice == "9":
            uid = input("  User ID for recommendations: ").strip()
            n = int(input("  Top N suggestions: ").strip())
            print_recommendations(uid, sg, pm, n)

        elif choice == "10":
            uid = input("  User ID: ").strip()
            r = float(input("  Radius (km): ").strip())
            print_nearby(uid, pm, r)

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  [!] Invalid choice.")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║   Social Network Explorer v1.0       ║")
    print("  ╚══════════════════════════════════════╝")

    pm, sg = demo_run()

    ans = input("\n  Launch interactive CLI? (y/n): ").strip().lower()
    if ans == "y":
        interactive_cli(pm, sg)
