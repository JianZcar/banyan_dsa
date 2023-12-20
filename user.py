class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._items = []

    def to_dict(self):
        return {'username': self.username, 'password': self.password}

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def items(self):
        return self._items
