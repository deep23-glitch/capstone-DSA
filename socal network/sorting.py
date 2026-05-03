"""
sorting.py - Friend Recommendation Engine
Data Structures: Hash Map for interest indexing, Sorting for ranking
Bonus         : Geo-proximity scoring using simple coordinate distance
"""

import math


# ═══════════════════════════════════════════════════════════════════════════════
#  Interest-Based Recommendation
# ═══════════════════════════════════════════════════════════════════════════════

def _common_interests_count(profile_a, profile_b):
    """
    Count common interests using set intersection.
    Time Complexity: O(min(|A|, |B|)) using hash sets.
    """
    set_a = set(profile_a.interests)
    set_b = set(profile_b.interests)
    return len(set_a & set_b), list(set_a & set_b)


def recommend_friends(user_id, graph, profile_manager, top_n=5):
    """
    Recommend non-friends ranked by:
      Primary   : Number of common interests (descending)  [Hashing for O(1) set ops]
      Secondary : Number of mutual friends (descending)    [Graph traversal]
      Tertiary  : Alphabetical by name                     [Stable sort]

    Algorithm:
      1. Build candidate pool = all users - existing friends - self
      2. For each candidate, compute (common_interests, mutual_friends) score
      3. Sort by (-common_interests, -mutual_friends, name)   → O(n log n)

    Time Complexity : O(n * k) where n=candidates, k=avg interests per user
    Space Complexity: O(n) for score list
    """
    target = profile_manager.get_profile(user_id)
    if not target:
        print(f"[!] User '{user_id}' not found.")
        return []

    friends = graph.get_friends(user_id)
    excluded = friends | {user_id}

    candidates = []
    for uid in profile_manager.all_user_ids():
        if uid in excluded:
            continue
        cand = profile_manager.get_profile(uid)
        if not cand:
            continue

        common_count, common_list = _common_interests_count(target, cand)

        # Mutual friends = intersection of friend sets
        cand_friends = graph.get_friends(uid)
        mutual_count = len(friends & cand_friends)

        candidates.append({
            "user_id": uid,
            "name": cand.name,
            "common_interests": common_count,
            "common_list": common_list,
            "mutual_friends": mutual_count,
        })

    # Sort: most common interests first, then mutual friends, then name
    candidates.sort(key=lambda x: (-x["common_interests"], -x["mutual_friends"], x["name"]))

    return candidates[:top_n]


def print_recommendations(user_id, graph, profile_manager, top_n=5):
    """Pretty-print friend recommendations."""
    print(f"\n  Friend Recommendations for '{user_id}':")
    recs = recommend_friends(user_id, graph, profile_manager, top_n)

    if not recs:
        print("  No recommendations available.")
        return recs

    print(f"  {'Rank':<5} {'Name':<15} {'Common Interests':<20} {'Mutual Friends':<15} {'Shared Tags'}")
    print("  " + "─" * 75)
    for rank, r in enumerate(recs, 1):
        tags = ', '.join(r["common_list"]) if r["common_list"] else "—"
        print(f"  {rank:<5} {r['name']:<15} {r['common_interests']:<20} {r['mutual_friends']:<15} {tags}")
    return recs


# ═══════════════════════════════════════════════════════════════════════════════
#  BONUS: Geo-Proximity DS Choice
# ═══════════════════════════════════════════════════════════════════════════════
# Design Decision: For geo-proximity we conceptually use a K-D Tree.
# A K-D Tree partitions 2D space and supports O(log n) nearest-neighbour queries,
# far better than O(n) linear scan.
# In this simplified demo we use a dict of (lat, lon) tuples + linear scan
# since we have <10 users. In production, replace with scipy.spatial.KDTree.

GEO_COORDS = {
    # Approximate coordinates for demo cities
    "Delhi":     (28.6, 77.2),
    "Mumbai":    (19.1, 72.8),
    "Bangalore": (12.9, 77.6),
    "Chennai":   (13.1, 80.3),
    "Kolkata":   (22.6, 88.4),
    "Hyderabad": (17.4, 78.5),
    "Pune":      (18.5, 73.9),
    "Jaipur":    (26.9, 75.8),
}

def _haversine_km(loc1, loc2):
    """Great-circle distance between two city names. O(1)."""
    if loc1 not in GEO_COORDS or loc2 not in GEO_COORDS:
        return float("inf")
    lat1, lon1 = math.radians(GEO_COORDS[loc1][0]), math.radians(GEO_COORDS[loc1][1])
    lat2, lon2 = math.radians(GEO_COORDS[loc2][0]), math.radians(GEO_COORDS[loc2][1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(a))

def nearby_users(user_id, profile_manager, radius_km=1000):
    """Find users within radius_km of the given user (linear scan for demo)."""
    target = profile_manager.get_profile(user_id)
    if not target or not target.location:
        return []
    results = []
    for uid in profile_manager.all_user_ids():
        if uid == user_id:
            continue
        p = profile_manager.get_profile(uid)
        if p and p.location:
            dist = _haversine_km(target.location, p.location)
            if dist <= radius_km:
                results.append((uid, p.name, p.location, round(dist, 1)))
    results.sort(key=lambda x: x[3])
    return results

def print_nearby(user_id, profile_manager, radius_km=1000):
    """Pretty-print nearby users."""
    print(f"\n  [GEO] Users within {radius_km} km of '{user_id}':")
    nearby = nearby_users(user_id, profile_manager, radius_km)
    if not nearby:
        print("  No nearby users found.")
        return
    for uid, name, loc, dist in nearby:
        print(f"    {name:<15} ({loc}) — {dist} km away")
