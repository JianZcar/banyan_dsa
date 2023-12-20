import pickle


def load_users():
    try:
        with open('user.pickle', 'rb') as f:
            users = pickle.load(f)
    except FileNotFoundError:
        users = []
    return users


def save_user(user):
    users = load_users()
    users.append(user)
    with open('user.pickle', 'wb') as f:
        pickle.dump(users, f)


def get_user(username):
    users = load_users()
    for user in users:
        if user.username == username:
            return user
    return None
