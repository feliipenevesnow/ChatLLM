
from werkzeug.security import check_password_hash

class User:
    def __init__(self, id, first_name, last_name, email, password, theme='light', created_at=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.theme = theme
        self.created_at = created_at

    def check_password(self, password):
        return check_password_hash(self.password, password)
