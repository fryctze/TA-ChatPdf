import os
from flask import Flask

from quanta_quire.app.vectorstore import create_faiss, splitter, splitter_from_web, create_chroma, create_scikit
from quanta_quire.blueprints import website, webchat, webapp
import logging

from quanta_quire.helper import get_first_pdf_file


def start_app():
  app = Flask(__name__)

  chats = {}
  app.chats = chats
# /tmp/venv/lib/python3.10/site-packages/langchain_core/utils/utils.py
  splitter = splitter_from_web(
    1000,
    200,
    "https://cdn.glitch.global/3d92198f-56d0-4fd6-87c3-3626f4e81afa/Student-Guide-UMC-2023.pdf"
  )
  vectorstore = create_scikit(splitter)
  app.vectorstore = vectorstore

  logging.basicConfig(level=logging.DEBUG)

  register_config(app)
  register_blueprints(app)

  # default port is 5000
  return app


def register_blueprints(app):
  app.register_blueprint(website.blueprint)
  app.register_blueprint(webchat.blueprint)
  app.register_blueprint(webapp.blueprint)


def register_config(app):
  app.secret_key = os.getenv('SECRET_KEY')

  app.config['WHATSAPP_TOKEN'] = os.getenv('WHATSAPP_TOKEN')
  app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')
  app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

  app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), os.getenv('UPLOAD_PATH'))
  os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)
