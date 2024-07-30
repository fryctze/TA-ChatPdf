from flask import request, jsonify, Blueprint, render_template, current_app
from quanta_quire.helper import append_feedback_log

blueprint = Blueprint("second", __name__)


@blueprint.route('/receive_chat_log', methods=['POST'])
def receive_chat_log():
  data = request.get_json()
  current_app.logger.info("Received chat log:", data)
  try:
    append_feedback_log(data)
    return jsonify({"success": True}, {"message": "success"}), 200
  except Exception as e:
    return jsonify({"success": False}, {"message": e}), 403


@blueprint.route('/index')
def index():
  return render_template("menu/dashboard.html", page_name='index')
