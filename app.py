from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False #modification tracker is not turnon 
app.secret_key = "mael"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #create a new endpoint /auth  it return a JWT token



#add resource to api and route
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__== "__main__": #prevent the running from other files
    db.init_app(app)
    app.run(port=5000, debug=True)
