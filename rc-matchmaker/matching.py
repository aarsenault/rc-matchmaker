# Matchmaking algorithm
def match_users(users):
    """Returns a tuple: a list of pairs of users and a list of unmatched users."""
    user_list = users.copy()
    matched = []
    print(user_list)
    while len(user_list) > 1:
        matched.append(
            (user_list.pop(), user_list.pop())
        )

    print('Finished matching')
    print(user_list)
    print(matched)

    return matched, user_list
