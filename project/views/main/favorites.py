from flask import request
from flask_restx import Namespace, Resource
from project.container import movie_service, user_service
from project.setup.api.models import movie
from project.tools.security import get_email_from_token

favorites_ns = Namespace('favorites')


@favorites_ns.route('/movies/')
class FavoriteMoviesView(Resource):
    @favorites_ns.marshal_with(movie, as_list=True)
    def get(self):
        """
        Получаем все фильмы
        """
        email = get_email_from_token(request.headers)
        return user_service.get_favorites(email)
