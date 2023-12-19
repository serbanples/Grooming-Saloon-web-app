from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from flask_migrate import Migrate
from routes import my_blueprint

app = Flask(__name__)
app.register_blueprint(my_blueprint)

# asta e pentru sesiuni si trb env variable pe git da e problema de mai tarziu
app.config['SECRET_KEY'] = 'tre_sa_pun_un_de_asta_candva_bag_pl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# bazele de date se fac ele aici cumva candva banuiesc
# inca n am nici cea mai vaga idee cum le structurez VOM VEDEA
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=True, nullable=False)
    lastName = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    # Add more fields as needed

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)


if __name__ == '__main__':
    app.run(debug=True)
