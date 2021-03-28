from flask import Flask
from flask import Flask, jsonify
from flask_restful import  Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefersh, UserLogout
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList
from blacklist import BLACKLIST


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False #modification tracker is not turnon 
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "mael" #app.config['JWT_SECRETE_KEY']
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) #no create /auth

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: 
        return {"is_admin": True}
    return{"is_admin" : False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        "description": "The token has expired",
        "error": "token_expired"
    }),401

@jwt.invalid_token_loader
def invalid_token_loader(jwt_headers, jwt_payload):
    return jsonify({
        "description": "Signature verification failed",
        "error": "invalid_token"
    }),401

@jwt.unauthorized_loader
def unauthorized_loader(jwt_headers, jwt_payload):
    return jsonify({
        "description": "JWT Needed",
        "error": "unautohrized_loader"
    }),401

@jwt.needs_fresh_token_loader
def needs_fresh_token_loader(jwt_headers, jwt_payload):
    return jsonify({
        "description": "fresh token needed",
        "error": "needs_fresh_token"
    }),401

@jwt.revoked_token_loader
def revoked_token_loader(jwt_headers, jwt_payload):
    return jsonify({
        "description": "token is not longer valid",
        "error": "token_expired"
    }),401


#add resource to api and route
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefersh, "/refresh")
api.add_resource(UserLogout, "/logout")



if __name__== "__main__": #prevent the running from other files
    db.init_app(app)
    app.run(port=5000, debug=True)

