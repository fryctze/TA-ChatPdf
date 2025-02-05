from flask import current_app
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatOpenAI(
  model="gpt-3.5-turbo"
  # model="gpt-4o"
)


def get_chat_log(session_id: str) -> BaseChatMessageHistory:
  if session_id not in current_app.chats:
    current_app.chats[session_id] = InMemoryChatMessageHistory()
  return current_app.chats[session_id]


def get_rag_chat_log(session_id: str) -> BaseChatMessageHistory:
  if session_id not in current_app.chats:
    current_app.chats[session_id] = ChatMessageHistory()
  return current_app.chats[session_id]
