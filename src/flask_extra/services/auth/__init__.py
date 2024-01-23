from flask import g
from flask_super.decorators import service


@service
class AuthService:
    @staticmethod
    def get_user():
        return g.user
