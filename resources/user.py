from blacklist import BLACKLIST
import sqlite3
from flask.globals import request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required= True, help ="This field cannot be blank")
_user_parser.add_argument("password", type=str, required= True, help ="This field cannot be blank")

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()#get the data

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with this username already exists"}, 400

        user = UserModel(**data)#for each key pass to the correct parameter
        user.save_to_db()

        return {"message" : "User created sucesfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        #get data from parser
        data = _user_parser.parse_args()
        
        #find user in database
        user = UserModel.find_by_username(data["username"])

        #check psw  like authenticate() function
        if user and safe_str_cmp(user.password, data["password"]):
            # identity()
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return{
                "access_token": access_token,
                "refresh_token":refresh_token
            }, 200
        return {"message": "Invalid credentials"},401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jti #jti is a JWT ID 
        BLACKLIST.add(jti)
        return {"message": "Succesfully logout"}


class TokenRefersh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user=get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token},200

