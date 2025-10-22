from flask_login import UserMixin

class User(UserMixin):
    def __init__ (self, id, user_type, user_first_name, user_last_name, username, password):
        self.id = id
        self.user_type = user_type
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.username = username
        self.password = password

    def get_id(self):
        return self.username