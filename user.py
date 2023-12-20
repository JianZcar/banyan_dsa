class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._items = []

    def __repr__(self):
        return f"{self.username}"

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def items(self):
        return self._items
