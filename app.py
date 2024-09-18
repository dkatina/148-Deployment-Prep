from math import prod
from flask import Flask
from database import db
from models.schemas import ma
from limiter import limiter
from cache import cache


#models
from models.customer import Customer
from models.product import Product
from models.order import Order
from models.orderProduct import order_product

#blueprints
from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint


def create_app(config_name):

    app = Flask(__name__) #instantiate the Flask app

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    blueprint_config(app)
    rate_limit_config(app)
    cache.init_app(app)

    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix="/customers")
    app.register_blueprint(product_blueprint, url_prefix="/products")
    app.register_blueprint(order_blueprint, url_prefix="/orders")

def rate_limit_config(app):
    limiter.init_app(app)
    limiter.limit("100 per hour")(customer_blueprint)



app = create_app('ProductionConfig')

with app.app_context():
        db.create_all()

