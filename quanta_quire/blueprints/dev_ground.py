from flask import request, jsonify, Blueprint, render_template, current_app
import requests
from quanta_quire.app.whatsapp import send_whatsapp_message
from quanta_quire.database_util import recreate_table
from quanta_quire.helper import append_feedback_log

blueprint = Blueprint("devs_field", __name__)


@blueprint.route('/index')
def index():
  return render_template("menu/dashboard.html", page_name='index')

@blueprint.route('/send_message')
def send_message():
  headers = {
    "Authorization": f"Bearer {current_app.config['WHATSAPP_TOKEN']}",
    "Content-Type": "application/json",
  }
  url = "https://graph.facebook.com/v20.0/" + "371105279409151" + "/messages"
  data = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "628973201171",
    "type": "text",
    "text": {"body": "Testing desu!!!"},
  }
  response = requests.post(url, json=data, headers=headers)
  return jsonify(f"whatsapp message response: {response.json()}")


@blueprint.route('/testing')
def testing():
  return jsonify(current_app.config['OPENAI_API_KEY'])

@blueprint.route('/db_reset')
def db_reset():
  recreate_table()
  return jsonify('Database reset')