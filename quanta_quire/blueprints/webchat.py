from flask import request, jsonify, Blueprint, current_app
from quanta_quire.app.experiment import with_message_history
from quanta_quire.helper import get_session_id

blueprint = Blueprint("webchat", __name__)


@blueprint.route('/web_chatting', methods=['POST'])
def web_chatting():
  current_app.logger.info("Receive chat message from user. Waiting response...")

  data = request.get_json()
  user_message = data['message']
  current_app.logger.info(user_message)

  username = get_session_id()

  bot_response = with_message_history(username, user_message)
  current_app.logger.info("chat gpt received ")

  current_app.logger.info(bot_response)
  data = jsonify({'response': str(bot_response.content)})

  print(data)
  return data
