from flask import Blueprint, request, current_app
from quanta_quire.app.whatsapp import verify, handle_message
from quanta_quire.database_util import clean_up_duplicates, recreate_table

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
