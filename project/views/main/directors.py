from flask_restx import Namespace, Resource
from project.container import director_service
from project.helpers.decorators import auth_required
from project.setup.api.models import director
from project.setup.api.parsers import page_parser


#marshal_with - проверка данных, полученных на выходе (нужный ли формат?)

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    @directors_ns.expect(page_parser)
    @directors_ns.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Получаем всех режиссеров
        """
        return director_service.get_all(**page_parser.parse_args())


@directors_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    @auth_required
    @directors_ns.response(404, 'Not Found')
    @directors_ns.marshal_with(director, code=200, description='OK')
    def get(self, director_id: int):
        """
        Получаем директора по id
        """
        return director_service.get_item(director_id)
