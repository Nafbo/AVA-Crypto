from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Response
from faker import Faker
fake = Faker()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ylugkowjgizjws:0058e3fd2d0e7f13189f9c21da297682235b7a24334e26c07b4439431434b9a8@ec2-176-34-211-0.eu-west-1.compute.amazonaws.com:5432/de3pmgr9nekvkf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

def client_table():
    for i in range(50):
        email = fake.email()
        password = fake.password()
        new_user = Users(email, password)
        db.session.add(new_user)
    db.session.commit()
    
if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    client_table()      