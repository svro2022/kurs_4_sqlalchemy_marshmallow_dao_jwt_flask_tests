import functools

import jwt
from flask import current_app, request
from flask_restx import abort


def auth_required(func):
    """
    Декоратор аутентификации пользователя по имени и паролю
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(
                token,
                key=current_app.config['SECRET_KEY'],
                algorithms=current_app.config['JWT_ALGORITHM'],
            )

        except jwt.PyJWTError as e:
            current_app.logger.error("JWT Decode Exception: %s", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper