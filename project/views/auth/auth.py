from flask import request
from flask_restx import Namespace, Resource, abort

from project.container import auth_service, user_service
from project.setup.api.models import auth, auth_result

api = Namespace('auth')

@api.route('/register/')
class AuthView(Resource):
    @api.expect(auth)
    @api.response(201, description='OK')
    def post(self):
        """
        Регистрация пользователя (создание в БД)
        :return:
        """
        user_service.create(request.json)
        return "OK", 201


@api.route('/login/')
class AuthView(Resource):
    @api.expect(auth)
    @api.marshal_with(auth_result, code=200)
    def post(self):
        """
        Аутентификация пользователя (вход пользователя в систему)
        :return:
        """

        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            abort(400)

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 200

    def put(self):
        """
        Создание новой пары токенов
        :return:
        """

        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 200

