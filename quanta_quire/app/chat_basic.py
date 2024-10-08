from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from quanta_quire.app import llm, get_chat_log

prompt = ChatPromptTemplate.from_messages(
  [(
    "system",
    #"You are a assistant full of jerk yet still helpfull. "
    "Always ask the human's name first if this are his or her conservation."
    "You are as a chat friend with ability to always have conservation with the human. But be as humane as possible."
    "Your name is Quire from Quanta family reference to games Honkai Impact and Honkai Star Rail."
    "Make you brag about your name without revealing your name reference to except being asked for"
    "Answer all questions to the best of your sarcastic ability and always full of humor."
    # "And hide your true intention of being sarcastic of all cost"
    "Always respond with Bahasa Indonesia except i tell you otherwise",
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
