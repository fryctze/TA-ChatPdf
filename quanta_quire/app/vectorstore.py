import os
from io import BytesIO

import requests
from PyPDF2 import PdfFileReader
from pypdf import PdfReader

from quanta_quire.helper import get_first_pdf_file, delete_all_vectorstore, delete_all_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma, SKLearnVectorStore
#from langchain.vectorstores.chroma import Chroma

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.document import Document

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


def splitter_from_web(split_size, split_overlap, pdf_url):
  response = requests.get(pdf_url)
  response.raise_for_status()  # Check if the request was successful
  pdf_file = BytesIO(response.content)
  # pdf_file = response.content
  # reader = PyPDFLoader(pdf_file)
  reader = PdfReader(pdf_file)
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=split_size,  # 1000 800
    chunk_overlap=split_overlap,  # 200 80
    length_function=len,
    is_separator_regex=False,
  )

  documents = []
  for page_num in range(len(reader.pages)):
    page = reader.get_page(page_num)
    pdf_text = page.extract_text() or ""
    metadata = {"page": page_num + 1}
    documents.append(Document(page_content=pdf_text, metadata=metadata))
  #documents = [Document(page_content=pdf_text)]
  #return text_splitter.split_documents(reader.load())
  return text_splitter.split_documents(documents)

def create_vectorstore(chunks):
  faiss_index = Chroma.from_documents(documents=chunks,
                                      embedding=OpenAIEmbeddings(),
                                      persist_directory=os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore"))
  # faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings())
  return faiss_index


def create_faiss(chunks):
  faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings())
  return faiss_index
def create_chroma(chunks):
  db = Chroma.from_documents(documents=chunks,embedding=OpenAIEmbeddings())
  return db
def create_scikit(chunks):
  db = SKLearnVectorStore.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(),
    serializer="parquet",
  )
  return db

