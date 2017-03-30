# Matchmaking algorithm

# Randomly group people into "buckets" of 2, plus maybe 1 unmatched person
# If we want to prevent duplicates in the future:
    # - 



def match_users(users):
    """Returns a tuple: a list of pairs of users and a list of unmatched users."""
    user_list = users.copy()
    matched = []
    print(user_list)
    while len(user_list) > 1:
        matched.append(
            (user_list.pop(), user_list.pop())
        )

    return matched, user_list
