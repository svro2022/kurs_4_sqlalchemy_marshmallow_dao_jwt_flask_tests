import logging
from flask import render_template
from project.config import config
from project.models import Genre, Director, Movie, User
from project.server import create_app, db

#логирование - время - уровень лога - сообщение

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')

app = create_app(config)

@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
    }


if __name__ == '__main__':
    app.run(debug=True)