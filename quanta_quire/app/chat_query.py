from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Statefully manage chat history ###
store = {}

llm = ChatOpenAI(
  model="gpt-3.5-turbo"
)


def history_aware_retriever(retriever):
  # Contextualize question ###
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
  return create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
  )


def rag_chain(history_aware_retriever):
  # Answer question ###
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

  return create_retrieval_chain(history_aware_retriever, question_answer_chain)


def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = ChatMessageHistory()
  return store[session_id]


def chat_rag_chain(rag_chain):
  return RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
  )


message = input("User: ")
print(chat_rag_chain(rag_chain).invoke(
  {"input": message},
  config={"configurable": {"session_id": "abc123"}},
)["answer"])


def chat(retriever):
  question_template = history_aware_retriever(retriever)
  return rag_chain(question_template)


def test():
  while True:
    # Prompt user for input
    message = input("User: ")

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      break

    # print(chat_rag_chain(rag_chain).invoke(
    #   {"input": message},
    #   config={"configurable": {"session_id": "abc123"}},
    # )["answer"])

    print(store)
