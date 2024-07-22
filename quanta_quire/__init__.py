import os
from flask import Flask
from quanta_quire.blueprints import website, webchat
import logging


def start_app():
  app = Flask(__name__)

  chats = {}
  app.chats = chats

  logging.basicConfig(level=logging.DEBUG)

  register_config(app)
  register_blueprints(app)

  # default port is 5000
  return app


def register_blueprints(app):
  app.register_blueprint(website.blueprint)
  app.register_blueprint(webchat.blueprint)


def register_config(app):
  app.secret_key = os.getenv('SECRET_KEY')

  app.config['WHATSAPP_TOKEN'] = os.getenv('WHATSAPP_TOKEN')
  app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')
  app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

  app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), os.getenv('UPLOAD_PATH'))
  os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)
