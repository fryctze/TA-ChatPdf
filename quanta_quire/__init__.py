import os
from flask import Flask
from quanta_quire.blueprints import website


def start_app():
  app = Flask(__name__)

  app.secret_key = os.getenv('SECRET_KEY')

  app.config['WHATSAPP_TOKEN'] = os.getenv('WHATSAPP_TOKEN')
  app.config['VERIFY_TOKEN'] = os.getenv('VERIFY_TOKEN')
  app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

  app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), os.getenv('UPLOAD_PATH'))
  os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)

  app.register_blueprint(website.blueprint)
  # default port is 5000
  return app
