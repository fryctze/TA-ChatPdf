import glob
import os

from flask import current_app

from quanta_quire.app.chat_basic import basic_chat
from quanta_quire.app.chat_rag import rag_chat
from quanta_quire.app.vectorstore import load_vectorstore


def chat(session_id, message):
  #pattern = os.path.join(current_app.config['UPLOAD_PATH'], '*.pdf')
  #pdf_files = glob.glob(pattern)
  try:
    vectorstore_path = os.path.join(current_app.config['UPLOAD_PATH'], 'vectorstore')
    index_faiss_path = os.path.join(vectorstore_path, 'index.faiss')
    index_pkl_path = os.path.join(vectorstore_path, 'index.pkl')

    # if pdf_files:
    #if os.path.isfile(index_faiss_path) and os.path.isfile(index_pkl_path):
    if os.path.exists(vectorstore_path) and os.path.isdir(vectorstore_path):
      retriever = load_vectorstore().as_retriever()
      return rag_chat(retriever, session_id, message)
    else:
      return basic_chat(session_id, message)

  except Exception as e:
    print(f"openai error: {e}")
    current_app.logger.info(e)
    response_message = "Mohon maaf, Quanta Quire saat ini sedang sibuk atau tidak terhubung. Silahkan coba lagi nanti."
    return response_message

