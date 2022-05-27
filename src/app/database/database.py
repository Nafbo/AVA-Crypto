import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Response
import numpy as np

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yeplwxjlhbauvi:48668289ae0c54004d2e532014cdcf6a2e9d34b4b63b74f0c35801b6b6bdc7dd@ec2-54-228-125-183.eu-west-1.compute.amazonaws.com:5432/d5e834h92a2de1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    portefolios = db.relationship('Portofolio')
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Portofolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(100))
    chain_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, wallet, chain_id, user_id):
        self.wallet = wallet
        self.chain_id = chain_id
        self.user_id = user_id
  
    
def create_user(email,password):
    '''Create an user in the database
    
    Parameters:
    email (string): email of the user
    password (string): password of the user
    
    Returns:
    '''
    email = email
    password = password
    new_user = Users(email, password)
    db.session.add(new_user)
    db.session.commit()
    return()
    

def add_wallet(email, wallet, chain_id):
    '''Add a wallet at an user in the database
    
    Parameters:
    email (string): email of the user
    wallet (string): wallet of the user
    chain_id (int): chain id of the wallet
    
    Returns:
    '''
    result_user = Users.query.filter_by(email = email).first_or_404()
    wallet = wallet
    chain_id = chain_id
    user_id = result_user.id
    new_portofolio = Portofolio(wallet, chain_id, user_id)
    db.session.add(new_portofolio)
    db.session.commit()
    return()

def portefolio_by_user(email, password):
    '''displays the portfolios of an user
    
    Parameters:
    email (string): email of the user
    password (string): password of the user
    
    Returns:
    portefolios (array): wallets and chain id of the wallet 
    '''
    result_user = Users.query.filter_by(email = email).first_or_404()
    portefolios = []
    if result_user.password== password:  
        user = {
            "id": result_user.id,
            "email": result_user.email,
            "portefolios": result_user.portefolios
            }
        portefolios = []
        for i in user['portefolios']:
            result_portefolio = [i.wallet, i.chain_id]
            portefolios.append(result_portefolio)
        return(portefolios)
    else:
        return("Wrong password")


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # create_user("victor.bonnaf@gmail.com", "victor")  
    # add_wallet("victor.bonnaf@gmail.com", "ZREWTXRYCVYIHUJOIP", 4567)
    print(portefolio_by_user("victor.bonnaf@gmail.com", "victor"))