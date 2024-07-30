import os
from flask import Flask

from quanta_quire.app.vectorstore import create_faiss, splitter, splitter_from_web
from quanta_quire.blueprints import website, webchat, webapp, second
import logging

from .extensions import db


def start_app():
  app = Flask(__name__)

  logging.basicConfig(level=logging.DEBUG)

  register_config(app)
  register_extension(app)
  register_blueprints(app)
  register_vars(app)


  # default port is 5000
  return app


def register_blueprints(app):
  app.register_blueprint(website.blueprint)
  app.register_blueprint(webchat.blueprint)
  app.register_blueprint(webapp.blueprint)
  # app.register_blueprint(second.blueprint)


def register_config(app):
  app.secret_key = os.getenv('SECRET_KEY')

  app.config['WHATSAPP_TOKEN'] = os.getenv('WHATSAPP_TOKEN')
  app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')
  app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

  app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), os.getenv('UPLOAD_PATH'))
  os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)


def register_vars(app):
  app.chats = {}
  app.chunks = 0
  app.feedbacks = {}


def register_extension(app):
  app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
  db.init_app(app)
