class User:
    def __init__(self, id, username, password, role="user"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data["id"],
            username=data["username"],
            password=data["password"],
            role=data.get("role", "user")
        )
