import os
from flask import Flask

from quanta_quire.app.vectorstore import create_faiss, splitter, splitter_from_web
from quanta_quire.blueprints import website, webchat, webapp, second
import logging


def start_app():
  app = Flask(__name__)


# /tmp/venv/lib/python3.10/site-packages/langchain_core/utils/utils.py
  # splitter = splitter_from_web(
  #   1000,
  #   200,
  #   "https://cdn.glitch.global/3d92198f-56d0-4fd6-87c3-3626f4e81afa/Student-Guide-UMC-2023.pdf"
  # )
  # vectorstore = create_scikit(splitter)
  # app.vectorstore = vectorstore

  logging.basicConfig(level=logging.DEBUG)

  register_config(app)
  register_blueprints(app)

  chats = {}
  app.chats = chats
  chunks = 0
  app.chunks = chunks
  feedbacks = {}
  app.feedbacks = feedbacks

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
