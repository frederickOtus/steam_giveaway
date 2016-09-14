from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('steam_away.config')
db = SQLAlchemy(app)

# I appologize for the circular imports, Flask docs told me
#   it was OK: http://flask.pocoo.org/docs/0.10/patterns/packages/
import steam_away.authorization
import steam_away.views
