import os

from flask import current_app

from quanta_quire.app.chat_basic import basic_chat
from quanta_quire.app.chat_rag import rag_chat
from quanta_quire.app.message_utils import get_last_ai_message, get_last_human_message
from quanta_quire.app.vectorstore import faiss_load_vectorstore
from quanta_quire.helper import get_random_response, insert_chat_log


def chat(session_id, message):
  flask_env = os.getenv('FLASK_ENV', 'real_development')

  if flask_env == 'real_development':
    current_app.logger.info('Return chat is in development mode....')
    return 'Mohon maaf, saya sedang dalam maintenance'
  else:
    current_app.logger.info('Querying to vectorstore...')
    response = qna(session_id, message)
    save_chat_log(session_id, message)

    return response


def chat_with_feedback(session_id, message):
  ask_feedback = ("Apakah jawaban saya sudah tepat? Lewati, dengan langsung bertanya lagi atau pilih: \n"
                  "[0] *Tidak* sesuai; \n"
                  "[1] *Kurang* sesuai; \n"
                  "[2] *Sesuai*; \n"
                  "[3] *Sangat* sesuai!")

  try:  # Check if the message is a feedback number
    number = int(message)
    if 0 <= number <= 3:  # Save the feedback
      if session_id not in current_app.chats:
        return get_random_response("feedback_first"), None
      save_chat_feedback(session_id=session_id, point=message)
      return get_random_response("feedback"), None
  except ValueError:
    pass  # The message is not a number, so it might be a new question

  # Check if the session has previous chats
  # if session_id not in current_app.chats:
  #   response = qna(session_id, message)
  #   return response, ask_feedback

  # Save the new question and mark that feedback is needed
  response = qna(session_id, message)
  save_chat_log(session_id, message)
  return response, ask_feedback


def save_chat_log(session_id, message):
  ai = get_last_ai_message(current_app.chats, session_id)
  # question = get_last_human_message(current_app.chats, session_id)
  # append_chat_log(session_id, question.content, ai.content, message)
  # current_app.logger.info(f"Inserting Chat WITHOUT Feedback....\n{message}\n{ai.content}")
  insert_chat_log(
    user=session_id,
    question=message,
    answer=ai.content)


# UNUSED FEEDBACK
def save_chat_feedback(session_id, point):
  ai = get_last_ai_message(current_app.chats, session_id)
  question = get_last_human_message(current_app.chats, session_id)
  # append_chat_log(session_id, question.content, ai.content, message)
  # current_app.logger.info(f"Inserting Chat Feedback....\n{question.content}\n{point}")

  # insert_chat_log(user=session_id,point=point,feedback=True)


def qna(session_id, message):
  try:
    vectorstore_path = os.path.join(current_app.config['UPLOAD_PATH'], 'vectorstore')
    index_faiss_path = os.path.join(vectorstore_path, 'index.faiss')
    index_pkl_path = os.path.join(vectorstore_path, 'index.pkl')

    # if pdf_files:
    # if os.path.isfile(index_faiss_path) and os.path.isfile(index_pkl_path):

    if os.path.exists(vectorstore_path) and os.path.isdir(vectorstore_path):

      current_app.logger.info("Vectorstore exists, processing to rag chat")
      retriever = faiss_load_vectorstore().as_retriever()
      return rag_chat(retriever, session_id, message)

    else:

      current_app.logger.info("There is no vectorstore to be found, processing to BASIC chat")
      return basic_chat(session_id, message)

  except Exception as e:
    current_app.logger.warning(f"OPENAI SIBUK Error: {e}")
    response_message = "Mohon maaf, Quanta Quire saat ini sedang sibuk atau tidak terhubung. Silahkan coba lagi nanti."
    return response_message
  # "Sepertinya Anda menemukan glitch dalam matriks. Silahkan hubungi developer untuk diperbaiki."
