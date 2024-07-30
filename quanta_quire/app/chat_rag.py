from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from quanta_quire.app import llm, get_rag_chat_log


def history_aware_retriever(retriever):
  # Contextualize question for chat history
  contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
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


def rag_chain(retriever):
  # System prompt for answer
  system_prompt = (
    "Your name is Quanta Quire. You are a bot created specifically for the Universitas Ma Chung research experiments."
    "You are acting as a customer support that can help with whatever user "
    "need about information related"
    # "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question."
    "If you don't know the answer, see the previous conversation to find the answer."
    "Then, if you still don't know the answer, say that you don't know. "
    # "If you don't know the answer, say that you don't know. "
    "Use three sentences maximum and keep the answer concise."
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

  return create_retrieval_chain(history_aware_retriever(retriever), question_answer_chain)


def chat_rag_chain(retriever):
  return RunnableWithMessageHistory(
    rag_chain(retriever),
    get_rag_chat_log,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
  )


def rag_chat(retriever, session_id, message):
  response = chat_rag_chain(retriever).invoke(
    {"input": message},
    config={"configurable": {"session_id": session_id}},
  )["answer"]
  # save_data(chats)
  return response
