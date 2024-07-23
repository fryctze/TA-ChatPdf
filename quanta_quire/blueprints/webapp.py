from flask import Blueprint, request, current_app
from quanta_quire.app.whatsapp import verify, handle_message

blueprint = Blueprint("wa", __name__)


@blueprint.route("/webhook", methods=["POST", "GET"])
def webhook():
  if request.method == "GET":
    return verify(request)
  elif request.method == "POST":
    return handle_message(request)


@blueprint.route("/test", methods=["POST", "GET"])
def test():
  current_app.logger.info(current_app.chats)
  return 'hello'