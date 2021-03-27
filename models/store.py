from db import db

class StoreModel(db.Model) :#extend model

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")#is a query builder, not a store of all items



    def __init__ (self, name):
        self.name = name

    def json(self):
        return {
            "id" : self.id,
            "name": self.name, 
            "items": [item.json() for item in self.items.all()]
        }#all is used for the lazy 

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name  LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
