from flask import Blueprint, request, current_app, jsonify
from quanta_quire.app.whatsapp import verify, handle_message
from quanta_quire.database_util import clean_up_duplicates, recreate_table, count_total, count_by_user, \
  sum_by_user_and_category, exporting_data

blueprint = Blueprint("wa", __name__)


@blueprint.route("/webhook", methods=["POST", "GET"])
def webhook():
  if request.method == "GET":
    return verify(request)
  elif request.method == "POST":
    return handle_message(request)


@blueprint.route("/cleanup", methods=["GET"])
def cleanup():
  clean_up_duplicates()
  current_app.logger.info("Cleaning up database...")
  return "Cleanup complete"


@blueprint.route("/recreate", methods=["GET"])
def recreate():
  recreate_table()
  current_app.logger.info("Recreating database...")
  return "Cleanup complete"


@blueprint.route("/test", methods=["POST", "GET"])
def test():
  current_app.logger.info(current_app.chats)
  return 'hello'


@blueprint.route('/count_by_category')
def count_by_category():
  return jsonify(count_total())


@blueprint.route('/count_user')
def count_user():
  return jsonify(count_by_user())


@blueprint.route('/count_user_category')
def count_user_category():
  return jsonify(sum_by_user_and_category())



@blueprint.route('/export_data')
def export_data():
  # logs = ChatLog.query.all()
  # return render_template("menu/data.html", page_name='data', data=logs)
  data = exporting_data()
  return jsonify(data)
