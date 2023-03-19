from sqlalchemy.exc import IntegrityError

from project.exceptions import UserAlreadyExists
from project.models import User, Movie, FavoriteMovies
from project.tools.security import generate_password_hash


# IntegrityError - ошибка нарушения целостности базы (нарушаем уникальный индекс)
# user и email не должны повторяться в базе


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        try:
            user = User(**user_d)
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists
        return user

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if user_d.get("email"):
            user.email = user_d.get("email")
        if user_d.get("password"):
            user.password = user_d.get("password")
        if user_d.get("name"):
            user.name = user_d.get("name")
        if user_d.get("surname"):
            user.surname = user_d.get("surname")
        #if user_d.get("favourite_genre"):
            #user.favourite_genre = user_d.get("favourite_genre")
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise UserAlreadyExists

    def update_password(self, email, new_password):
        user = self.get_by_email(email)
        user.password = generate_password_hash(new_password)

        self.session.add(user)
        self.session.commit()

    def get_favorites(self, user_id):
        result = self.session.query(
            Movie,
        ).join(
            FavoriteMovies,
        ).filter(
            FavoriteMovies.user_id == user_id,
        ).all()
        return result

