import os
os.environ["OPENAI_API_KEY"] = "tada"

my_file = '/content/drive/MyDrive/TA Chat PDF/example_pdf/monopoly.pdf'
prod_file = '/content/drive/MyDrive/TA Chat PDF/Student-Guide-UMC-2023.pdf'

# !pip install -q \
#     openai langchain pypdf \
#     langchain_community \
#     langchain_openai \
#     faiss-gpu


from langchain_community.document_loaders import PyPDFLoader
file_path = (prod_file)
loader = PyPDFLoader(file_path)
# PyPDFLoader(DATA_PATH, glob="*.md")


# from langchain.schema.document import Document
# document: list[Document]
# text_splitter.split_documents(document)
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, # 1000 800
    chunk_overlap = 200, # 200 80
    length_function = len,
    is_separator_regex=False,
)
pages = text_splitter.split_documents(loader.load())
#pages = loader.load_and_split()


pages[32]
len(pages)


from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# embeddings = OpenAIEmbeddings()
# knowledgeBase = FAISS.from_texts(chunks, embeddings)
faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())

# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)
# vectorstore = Chroma.from_documents(documents=pages, embedding=OpenAIEmbeddings())

retriever = faiss_index.as_retriever()

# example = faiss_index.similarity_search("How to get jail?", k=2)


example = faiss_index.similarity_search("Bagaimana cara mendapatkan poin sosial?", k=2)
example





from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo"
)


from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed"
    # "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

### Answer question ###
system_prompt = (
    # "You are a customer support that can help with whatever user need about information related to the retrieved context. "
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the answer concise."
    "response with Bahasa Indonesia. response as other language if i told you to do so."
    # "Also please inform me about the source page number of your answer."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


while True:
  # Prompt user for input
  message = input("User: ")

  # Exit program if user inputs "quit"
  if message.lower() == "quit":
    break

  print(conversational_rag_chain.invoke(
      {"input": message},
      config={"configurable": {"session_id": "abc123"}},
  )["answer"])

  print(store)

