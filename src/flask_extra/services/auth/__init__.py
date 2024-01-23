from flask import g
from flask_super.decorators import service


@service
class AuthService:
    def get_user(self):
        return g.user
