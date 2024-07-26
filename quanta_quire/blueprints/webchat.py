from flask import request, jsonify, Blueprint, current_app, session

from quanta_quire.app.chat import chat
from quanta_quire.helper import get_session_id

blueprint = Blueprint("webchat", __name__)


@blueprint.route('/web_chatting', methods=['POST'])
def web_chatting():
  current_app.logger.info("Receive chat message from user. Waiting response...")

  data = request.get_json()
  user_message = data['message']
  current_app.logger.info(user_message)

  username = get_session_id()

  bot_response, ask_feedback = chat(username, user_message)
  current_app.logger.info("chat gpt received ")

  current_app.logger.info(bot_response)
  current_app.logger.info(ask_feedback)
  data = jsonify({
    'response': str(bot_response),
    'feedback': str(ask_feedback)
  })

  return data

@blueprint.route('/update_session', methods=['POST'])
def update_session_id():
  data = request.get_json()
  new_id = data['message']
  session['session_id'] = new_id
  current_app.logger.info("updated session id " + new_id)
  response = jsonify({'response': session['session_id']})
  return response
