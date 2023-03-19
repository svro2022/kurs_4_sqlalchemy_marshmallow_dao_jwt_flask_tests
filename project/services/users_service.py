from project.dao.user import UserDAO
from project.tools.security import generate_password_hash


class UsersService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        """
        Сервис получения одного пользователя
        :param uid:
        :return:
        """
        return self.dao.get_one(uid)

    def get_by_email(self, email):
        """
        Сервис поиска пользователя по email
        :param email:
        :return:
        """
        return self.dao.get_by_email(email)

    def get_all(self):
        """
        Сервис получения всех пользователей
        :return:
        """
        users = self.dao.get_all()
        return users

    def create(self, user_d: dict[str, str]):
        """
        Сервис создания пользователя
        :param user_d:
        :return:
        """
        user_d['password'] = generate_password_hash(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        """
        Сервис обновления данных о пользователе
        :param user_d:
        :return:
        """
        self.dao.update(user_d)
        return self.dao

    def update_password(self, email, new_password):
        """
        Сервис обновления пароля пользователя
        :param email:
        :param new_password:
        :return:
        """
        self.dao.update_password(email, new_password)

    def delete(self, uid):
        """
        Сервис удаления пользователя
        :param uid:
        :return:
        """
        self.dao.delete(uid)

    def get_favorites(self, email):
        user = self.get_by_email(email)
        favorites = self.dao.get_favorites(user.id)
        return favorites

