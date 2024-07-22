from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
  SystemMessage,
  AIMessage,
  HumanMessage
)

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from flask import current_app

# for rag system with history
from langchain_community.chat_message_histories import ChatMessageHistory
# for basic chat history
from langchain_core.chat_history import (
  BaseChatMessageHistory,
  InMemoryChatMessageHistory,
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo"
)

def get_rag_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in current_app.chats:
    current_app.chats[session_id] = ChatMessageHistory()
  return current_app.chats[session_id]


def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in current_app.chats:
    current_app.chats[session_id] = InMemoryChatMessageHistory()
  return current_app.chats[session_id]


def simple_history():
  return RunnableWithMessageHistory(
    llm,
    #lambda session_id: get_session_history(app, session_id),
    get_session_history,
  )

def with_message_history(session_id, input):
  config = {"configurable": {"session_id": session_id}}
  return simple_history().invoke(
    [HumanMessage(content=input)],
    config=config,
  )