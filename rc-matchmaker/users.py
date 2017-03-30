from test_data import users as user_data

def _get_hardcoded_users():
    """Return a hardcoded list of users for testing purposes."""
    users = [{'name': name}
                for (name) in user_data]
    # users = [{'first_name': first_name, 'last_name': last_name}
    #             for (first_name, last_name) in users]

    return users

def fetch_users():
    """Return a list of users."""
    users = _get_hardcoded_users()
    return users
