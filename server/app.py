#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Resource, Api
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app=app)
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

class BakeriesResource(Resource):
    def get(self):
        bakeries = [bake.to_dict() for bake in Bakery.query.all()]
        return bakeries, 200
    
api.add_resource(BakeriesResource, "/bakeries", endpoint="bakeries")

class BakeriesIdResource(Resource):
    def get(self,id):
        bakeries = Bakery.query.get(id)
        bakeries_dict = bakeries.to_dict()
        return bakeries_dict, 200
api.add_resource(BakeriesIdResource, "/bakeries/<int:id>",  endpoint="bakery")

class BakeByPriceResource(Resource): #add dec but where
    def get(self):
        price = BakedGood.query.order_by(BakedGood.price.desc()).all()
        price_dict = [p.to_dict() for p in price]
        return price_dict, 200
api.add_resource(BakeByPriceResource, "/baked_goods/by_price", endpoint="pricedesc")

class BakeByPriceMostExpensiveResource(Resource):
    def get(self):
        price = BakedGood.query.order_by(BakedGood.price.desc()).first()
        p = price.to_dict()
        return p , 200
api.add_resource(BakeByPriceMostExpensiveResource, "/baked_goods/most_expensive", endpoint="most_expensive")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
