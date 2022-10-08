# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

import config

from flask import (
    Flask, 
    request,
    render_template
)

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Application initialization
app = Flask(__name__, 
            template_folder='views',
            static_folder='public')

app.config.from_object(config.DevelopmentConfig)

api_router = Api(app, prefix='/api/v1')  # API Initialization
db = SQLAlchemy(app)                     # Database Initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'


"""
404 Page not found error default handler
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', error=e), 404



"""
Controllers and API Resources import
and register blueprints and resources 
"""

from app.models import *
from app.controllers import main    # Controllers
from app.api import price
from app.api import damage

# Register resources
api_router.add_resource(price.PricePrediction, '/predict-price')
api_router.add_resource(damage.DamagePrediction, '/predict-damage')

# Register Blueprints
app.register_blueprint(main.bp)
