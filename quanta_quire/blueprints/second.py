from flask import request, jsonify, Blueprint, render_template
from quanta_quire.helper import append_feedback_log

blueprint = Blueprint("second", __name__)


@blueprint.route('/receive_chat_log', methods=['POST'])
def receive_chat_log():
  data = request.get_json()
  print("Received chat log:", data)
  append_feedback_log(data)
  return jsonify({"success": True}), 200


@blueprint.route('/index')
def index():
  return render_template("menu/dashboard.html", page_name='index')
