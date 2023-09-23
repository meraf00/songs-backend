from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS

from db import db
from songs import songs_bp
from auth import auth_bp


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

app.register_blueprint(songs_bp, url_prefix='/songs')
app.register_blueprint(auth_bp, url_prefix='/auth')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0")