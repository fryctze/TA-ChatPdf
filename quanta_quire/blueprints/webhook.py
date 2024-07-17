from flask import Blueprint, request
from quanta_quire.app.whatsapp import verify, handle_message

blueprint = Blueprint("wa", __name__)


@blueprint.route("/webhook", methods=["POST", "GET"])
def webhook():
  if request.method == "GET":
    return verify(request)
  elif request.method == "POST":
    return handle_message(request)
