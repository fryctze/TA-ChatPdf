import os
from quanta_quire.helper import get_first_pdf_file, delete_all_vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from flask import current_app


def generate_vectorstore():
  pdf = load_pdf(get_first_pdf_file())
  chunks = splitter(pdf)
  vectorstore = create_vectorstore(chunks)
  delete_all_vectorstore()
  vectorstore.save_local(os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore.index"))
  # example = faiss_index.similarity_search("Bagaimana cara mendapatkan poin sosial?", k=2)


def load_vectorstore():
  db = FAISS.load_local(
    folder_path=os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore.index"),
    index_name="vectorstore.index",
    embeddings=OpenAIEmbeddings()
  )
  return db


def load_pdf(files):
  from langchain_community.document_loaders import PyPDFLoader
  file_path = (files)
  return PyPDFLoader(file_path)


def splitter(docs):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # 1000 800
    chunk_overlap=200,  # 200 80
    length_function=len,
    is_separator_regex=False,
  )
  return text_splitter.split_documents(docs.load())


def create_vectorstore(chunks):
  faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings())
  return faiss_index
