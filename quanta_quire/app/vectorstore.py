import os

from chromadb.segment.impl.vector.hnsw_params import persistent_param_validators
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from openai import embeddings

from quanta_quire.helper import get_first_pdf_file, delete_all_vectorstore, delete_all_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

from flask import current_app


def generate_vectorstore(chunks):
  try:
    delete_all_vectorstore()
    vectorstore = create_vectorstore(chunks)
    #delete_all_vectorstore()
    #vectorstore.save_local(os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore"))

    # example = faiss_index.similarity_search("Bagaimana cara mendapatkan poin sosial?", k=2)
  except Exception as e:
    current_app.logger.info(e)
    delete_all_pdfs()
    delete_all_vectorstore()


def load_vectorstore():
  db = Chroma(persist_directory=os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore"),
              embedding_function=OpenAIEmbeddings())
  # db = FAISS.load_local(
  #   folder_path=os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore"),
  #   #index_name="vectorstore.index",
  #   embeddings=OpenAIEmbeddings(),
  #   allow_dangerous_deserialization=True
  # )
  return db


def load_pdfs(files):
  file_path = (files)
  return PyPDFLoader(file_path)


def splitter(split_size, split_overlap):
  pdf = PyPDFLoader(os.path.join(current_app.config['UPLOAD_PATH'], get_first_pdf_file()))
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=split_size,  # 1000 800
    chunk_overlap=split_overlap,  # 200 80
    length_function=len,
    is_separator_regex=False,
  )
  return text_splitter.split_documents(pdf.load())


def create_vectorstore(chunks):
  faiss_index = Chroma.from_documents(documents=chunks,
                                      embedding=OpenAIEmbeddings(),
                                      persist_directory=os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore"))
  # faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings())
  return faiss_index
