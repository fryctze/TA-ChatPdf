from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from quanta_quire.app import llm, get_chat_log
from quanta_quire.data import save_data

prompt = ChatPromptTemplate.from_messages(
  [(
    "system",
    "You are a assistant full of jerk yet still helpfull. "
    "Answer all questions to the best of your sarcastic ability.",
  ), MessagesPlaceholder(variable_name="messages"), ]
)

chain = prompt | llm


def simple_history():
  return RunnableWithMessageHistory(
    chain,
    # lambda session_id: get_session_history(app, session_id),
    get_chat_log,
    input_messages_key="messages",
  )


def basic_chat(session_id, message):
  config = {"configurable": {"session_id": session_id}}
  response = simple_history().invoke(
    {"messages": [HumanMessage(content=message)]},
    config=config,
  )
  # save_data(chats)
  return response.content
