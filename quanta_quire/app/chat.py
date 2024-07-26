import os
from flask import current_app
from quanta_quire.app.chat_basic import basic_chat
from quanta_quire.app.chat_rag import rag_chat
from quanta_quire.app.message_utils import get_last_ai_message, get_last_human_message
from quanta_quire.app.vectorstore import faiss_load_vectorstore
from quanta_quire.helper import get_random_response, append_chat_log


def chat(session_id, message):
  ask_feedback = "Apakah jawaban saya sudah tepat? Lewati, dengan langsung bertanya lagi atau pilih: [1] Sudah tepat; [2] Masih ada yang kurang; [3] Tidak tepat!"
  try:
    number = float(message)  # Convert to float to handle both integer and decimal numbers
    if 1 <= number <= 3:
      if session_id not in current_app.chats:
        return get_random_response("feedback_first"), None
      return feedback(session_id, message), None
  except ValueError:
    pass
  return qna(session_id, message), ask_feedback


def feedback(session_id, message):
  ai = get_last_ai_message(current_app.chats, session_id)
  question = get_last_human_message(current_app.chats, session_id)
  append_chat_log(question.content, ai.content, message)
  return get_random_response("feedback")


def qna(session_id, message):
  try:
    vectorstore_path = os.path.join(current_app.config['UPLOAD_PATH'], 'vectorstore')
    index_faiss_path = os.path.join(vectorstore_path, 'index.faiss')
    index_pkl_path = os.path.join(vectorstore_path, 'index.pkl')

    # if pdf_files:
    #if os.path.isfile(index_faiss_path) and os.path.isfile(index_pkl_path):
    if os.path.exists(vectorstore_path) and os.path.isdir(vectorstore_path):
      retriever = faiss_load_vectorstore().as_retriever()
      return rag_chat(retriever, session_id, message)
    else:
      return basic_chat(session_id, message)

  except Exception as e:
    print(f"openai error: {e}")
    current_app.logger.info(e)
    response_message = "Mohon maaf, Quanta Quire saat ini sedang sibuk atau tidak terhubung. Silahkan coba lagi nanti."
    # "Sepertinya Anda menemukan glitch dalam matriks. Silahkan hubungi developer untuk diperbaiki."
    return response_message
