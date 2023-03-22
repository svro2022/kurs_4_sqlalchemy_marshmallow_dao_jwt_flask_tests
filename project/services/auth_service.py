import calendar
import datetime

import jwt

from flask_restx import abort

from project.services.users_service import UsersService
from project.tools.security import compare_passwords, generate_password_hash

from project.config import BaseConfig


class AuthService:
    def __init__(self, user_service: UsersService):
        self.user_service = user_service

    def create(self, data: dict):
        data['password'] = generate_password_hash(data['password'])
        return self.user_service.create(data)


    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compare_passwords(user.password, password):
                abort(400)

        data = {
            "email": user.email,
            'password': user.password
        }

        # 30 min access_token живет
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGO)

        # 130 days refresh_token живет
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGO)


        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        """
        Функция создания новой пары access_token и refresh_token по refresh_token
        """
        data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=BaseConfig.ALGO)
        email = data.get('email')

        return self.generate_tokens(email, None, is_refresh=True)
