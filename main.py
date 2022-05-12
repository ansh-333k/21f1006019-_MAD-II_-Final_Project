from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore

app = Flask(__name__)
app.secret_key = 'P@ssw0rd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ansh/flashcard/database/database.sqlite3'
db = SQLAlchemy(app)

from applications.controllers.controllers import *
from applications.data.models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
#security = Security(app, user_datastore)
decks = list()
decks.append('Antonyms')
decks.append('Synonyms')

if __name__ == '__main__':
    app.run(debug = True)