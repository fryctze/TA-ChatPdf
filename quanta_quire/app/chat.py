import glob
import os

from flask import current_app

from quanta_quire.app.chat_basic import basic_chat
from quanta_quire.app.chat_rag import rag_chat
from quanta_quire.app.vectorstore import load_vectorstore


def chat(session_id, message):
  #pattern = os.path.join(current_app.config['UPLOAD_PATH'], '*.pdf')
  #pdf_files = glob.glob(pattern)
  vectorstore_path = os.path.join(current_app.config['UPLOAD_PATH'], 'vectorstore')
  index_faiss_path = os.path.join(vectorstore_path, 'index.faiss')
  index_pkl_path = os.path.join(vectorstore_path, 'index.pkl')

  #if pdf_files:
  if os.path.isfile(index_faiss_path) and os.path.isfile(index_pkl_path):
    retriever = load_vectorstore().as_retriever()
    return rag_chat(retriever, session_id, message)
  else:
    return basic_chat(session_id, message)