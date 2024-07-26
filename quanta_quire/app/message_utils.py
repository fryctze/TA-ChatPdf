from langchain_core.messages import AIMessage, HumanMessage


def get_last_ai_message(chat_history, user_id):
  if user_id not in chat_history:
    return None

  messages = chat_history[user_id].messages

  for message in reversed(messages):
    if isinstance(message, AIMessage):
      return message

  return None


def get_last_human_message(chat_history, user_id):
  if user_id not in chat_history:
    return None

  messages = chat_history[user_id].messages

  for message in reversed(messages):
    if isinstance(message, HumanMessage):
      return message

  return None


def get_last_two_human_messages(chat_history, user_id):
  if user_id not in chat_history:
    return None, None

  messages = chat_history[user_id].messages

  last_human_message = None
  second_last_human_message = None

  for message in reversed(messages):
    if isinstance(message, HumanMessage):
      if last_human_message is None:
        last_human_message = message
      elif second_last_human_message is None:
        second_last_human_message = message
        break

  return last_human_message, second_last_human_message
