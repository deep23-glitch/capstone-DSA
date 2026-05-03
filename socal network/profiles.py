"""
profiles.py - User Profile Management
Data Structures: Hash Map (dict) for O(1) lookups, Lists for interests/location
"""

class UserProfile:
    def __init__(self, user_id, name, age, interests=None, location=None):
        self.user_id = user_id          # Hash key
        self.name = name
        self.age = age
        self.interests = interests or []  # List/Array of interests
        self.location = location or ""

    def __repr__(self):
        return (f"UserProfile(id={self.user_id}, name={self.name}, "
                f"age={self.age}, interests={self.interests}, location={self.location})")


class ProfileManager:
    """
    Manages user profiles using a Hash Map (Python dict) for O(1) average-case
    add, get, and update operations.
    Space Complexity: O(n) where n = number of users.
    """

    def __init__(self):
        self._profiles = {}   # Hash Map: user_id -> UserProfile

    def add_user(self, user_id, name, age, interests=None, location=None):
        """Add a new user. O(1) average."""
        if user_id in self._profiles:
            print(f"[!] User '{user_id}' already exists.")
            return False
        self._profiles[user_id] = UserProfile(user_id, name, age, interests, location)
        print(f"[+] User '{name}' (id={user_id}) added.")
        return True

    def get_profile(self, user_id):
        """Retrieve a profile by ID. O(1) average."""
        return self._profiles.get(user_id, None)

    def update_profile(self, user_id, name=None, age=None, interests=None, location=None):
        """Update one or more fields of a user profile. O(1) average."""
        profile = self._profiles.get(user_id)
        if not profile:
            print(f"[!] User '{user_id}' not found.")
            return False
        if name is not None:
            profile.name = name
        if age is not None:
            profile.age = age
        if interests is not None:
            profile.interests = interests
        if location is not None:
            profile.location = location
        print(f"[~] Profile '{user_id}' updated.")
        return True

    def display_profile(self, user_id):
        """Pretty-print a user profile."""
        p = self.get_profile(user_id)
        if not p:
            print(f"[!] User '{user_id}' not found.")
            return
        print(f"""
  ┌─────────────────────────────────┐
  │  Profile: {p.name:<22} │
  ├─────────────────────────────────┤
  │  ID       : {p.user_id:<21} │
  │  Age      : {str(p.age):<21} │
  │  Location : {p.location:<21} │
  │  Interests: {', '.join(p.interests):<21} │
  └─────────────────────────────────┘""")

    def all_user_ids(self):
        """Return list of all user IDs. O(n)."""
        return list(self._profiles.keys())

    def user_exists(self, user_id):
        return user_id in self._profiles
