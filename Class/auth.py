import bcrypt as bcrypt


class Auth:

    def __init__(self, user_model):
        self.user_model = user_model

    def is_user(self, user: tuple) -> bool:
        result = False
        if user is not None:
            result = True

        return result

    def check_password(self, user: tuple, plain_password: str) -> bool:
        result = False
        password_hash = user[2]
        if bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8')):
            result = True

        return result

    def auth_user(self, user: tuple, pseudo: str, password: str) -> int:
        result = 0
        if pseudo and password:
            if self.is_user(user):
                if self.check_password(user, password):
                    result = 1
        else:
            result = -1

        return result


# hashpass = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())
# print(hashpass.decode('utf-8'))
