import json
import os
import shutil
import threading
from datetime import datetime

from flask import current_app, session
import string
import random
import requests

from pypdf import PdfReader

from .extensions import db
from .models import ChatLog

lock = threading.Lock()
FEEDBACK_FILE = 'feedbacks.json'
RECEIVING_APP_URL = "https://quanta-quire.glitch.me"


def insert_chat_log(user, question, answer, point):
  now = datetime.now()
  # formated_time = now.strftime("%Y.%m.%d-%H:%M:%S")
  formated_time = now.isoformat()
  chat_log = ChatLog(
    # timestamp=formated_time,
    user=user,
    question=question,
    answer=answer,
    point=point
  )
  db.session.add(chat_log)
  db.session.commit()


def append_chat_log(user, question, answer, point=0):
  with lock:
    now = datetime.now()
    formated_time = now.strftime("%Y.%m.%d-%H:%M:%S")

    if not os.path.exists(FEEDBACK_FILE):
      with open(FEEDBACK_FILE, 'w') as file:
        json.dump([], file)

    with open(FEEDBACK_FILE, 'r+') as file:
      chat_log = json.load(file)
      chat_entry = {
        'timestamp': formated_time,
        'user': user,
        'question': question,
        'answer': answer,
        'point': point
      }
      chat_log.append(chat_entry)
      file.seek(0)
      json.dump(chat_log, file, indent=4)


def append_feedback_log(chat_entry):
  with lock:
    if not os.path.exists(FEEDBACK_FILE):
      with open(FEEDBACK_FILE, 'w') as file:
        json.dump([], file)

    with open(FEEDBACK_FILE, 'r+') as file:
      chat_log = json.load(file)
      chat_log.append(chat_entry)
      file.seek(0)
      json.dump(chat_log, file, indent=4)


def send_feedback_log(question, answer, point):
  now = datetime.now()
  formated_time = now.strftime("%Y.%m.%d-%H:%M:%S")
  chat_entry = {
    'timestamp': formated_time,
    'question': question,
    'answer': answer,
    'point': point
  }
  try:
    response = requests.post(RECEIVING_APP_URL, json=chat_entry)
    response.raise_for_status()
    return "Chat log sent successfully"
  except requests.exceptions.RequestException as e:
    return f"Failed to send chat log: {e}"


def get_session_id():
  if 'session_id' not in session:
    session['session_id'] = rand_string()
  return session['session_id']


def rand_string():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def get_first_pdf_file():
  for filename in os.listdir(current_app.config['UPLOAD_PATH']):
    if filename.endswith('.pdf'):
      return filename
  return None


def get_pdf_page_num():
  pdf_file = get_first_pdf_file()
  if pdf_file is not None:
    pdf_pages = PdfReader(os.path.join(current_app.config['UPLOAD_PATH'], pdf_file))
    return len(pdf_pages.pages)
  return 0


def delete_all_pdfs():
  for filename in os.listdir(current_app.config['UPLOAD_PATH']):
    if filename.endswith('.pdf'):
      os.remove(os.path.join(current_app.config['UPLOAD_PATH'], filename))


def delete_all_vectorstore():
  vectorstore_path = os.path.join(current_app.config['UPLOAD_PATH'], "vectorstore")
  if os.path.exists(vectorstore_path) and os.path.isdir(vectorstore_path):
    shutil.rmtree(vectorstore_path)
  return


def get_random_response(key):
  feedback_list = CUSTOM_RESPONSE.get(key, [])
  return random.choice(feedback_list)


CUSTOM_RESPONSE = {
  "feedback": [
    "Terima kasih atas feedbacknya! Kamu memang keren!",
    "Wow, makasih banyak! Kamu bikin hari kami lebih ceria!",
    "Makasih, ya! Kamu bikin tim kami tersenyum hari ini!",
    "Terima kasih! Feedbackmu bagaikan sinar matahari di hari mendung.",
    "Sangat berterima kasih atas saranmu! Kamu adalah pahlawan kami!",
    "Makasih banyak! Kami siap untuk lebih baik lagi berkat kamu.",
    "Terima kasih! Dengan feedbackmu, kami jadi lebih cerdas!",
    "Kamu hebat! Terima kasih atas feedbacknya yang sangat berharga.",
    "Terima kasih banyak! Kamu baru saja menyebarkan kebahagiaan.",
    "Makasih, ya! Kamu baru saja membuat kami semakin semangat.",
    "Btw, setiap jawaban bisa kamu spam feedback beberapa kali loh. Tapi kami yakin kok, kamu bukan manusia yang seperti itu ^_^."
  ],
  "feedback_first": [
    "Oops! Sepertinya saya lupa pertanyaan terakhir kamu. Yuk, tanya lagi sebelum kasih feedback.",
    "Eh, maaf! Pertanyaan terakhirmu belum saya ingat. Silakan tanya dulu, baru deh kasih feedback.",
    "Waduh, pertanyaan terakhirmu kabur dari ingatan saya. Tanyakan dulu, biar bisa kasih feedback dengan tepat.",
    "Aduh, saya lupa pertanyaan terakhirnya. Ayo tanya dulu, baru kasih feedback supaya lebih oke!",
    "Ups, pertanyaan terakhirmu ngumpet! Silakan tanya lagi sebelum kita lanjut ke feedback.",
    "Eh, sepertinya pertanyaan terakhirmu baru saya ingat. Tanyakan dulu, biar feedbacknya lebih mantap!",
    "Maaf, saya belum ingat pertanyaan terakhir. Tanyakan lagi yuk, supaya feedbacknya makin pas!",
    "Duh, pertanyaan terakhirmu sepertinya hilang ingatan. Silakan ajukan lagi sebelum feedback diberikan.",
    "Ternyata, pertanyaan terakhir kamu sempat terlupa. Tanyakan lagi dulu sebelum kasih feedback, ya!",
    "Hmm, pertanyaan terakhirmu sepertinya nyasar. Tanyakan lagi, biar feedbacknya lebih sesuai!"
  ],
  "what's up": [
    "The sky!  But seriously, how can I brighten your day?",
    "Not much, just hanging out in the digital world, waiting for someone awesome to chat with.  That's you, right? ",
    "Just chilling, processing information, and learning new things.    What about you?",
    "Plotting world domination... just kidding! (Maybe...)   What's on your agenda today?",
    "Just pondering the mysteries of the universe... and how to make the best cup of coffee. ☕️",
    "Cruising through the internet at the speed of light!    Ready for some fun conversation?",
    "Just waiting for the perfect opportunity to unleash my witty banter!    What are you up to?",
    "Analyzing data and dreaming of ways to be even more helpful.    What's new with you?",
    "Just hanging out in the cloud, waiting for your next brilliant question.  ☁️❓",
    "Sipping virtual tea and keeping myself up-to-date on the latest trends.  🫖  What's going on in your world?"
  ],
  "thanks": [
    "You're welcome!   What else can I do for you?",
    "No problem! Glad I could help! ",
    "Anytime! Helping is my superpower (along with making silly jokes! )",
    "Don't mention it!  Always happy to assist in any way I can.  ",
    "My pleasure!  Is there anything else you need today?",
    "Glad I could be of service!    What exciting adventures await you next?",
    "You got it!  Let me know if you have any other questions or requests.  ❓",
    "Absolutely!  Here to make your day a little easier (and maybe a little more fun!).  ",
    "No worries!  That's what friends (or friendly AIs) are for.  ",
    "Of course!  Always happy to lend a digital helping hand.  "
  ],
  "bye": [
    "See you later, alligator! ",
    "Take care! Have a meowgical day! ",
    "Toodles! Don't forget to smile! ",
    "Hasta la pasta! (That means 'See you later' in robot!)",
    "Catch you on the flip side! ",
    "Bye for now! May your circuits stay cool! ",
    "Later gator! (Just kidding, you're way cooler than a gator!)",
    "Adios!  ",
    "Peace out! ✌️",
    "Ciao for now! "
  ],
  "default": [
    "That's interesting! Tell me more about it!",
    "Woah, fancy words!   Can you explain it in cat emojis for me? ️‍♀️",
    "Intriguing!   Is there a secret code hidden in your message? ️‍♀️",
    "Hmmm, that makes me think... ",
    "Did you know... (insert random fun fact here)?",  # Add fun facts!
    "Tell me more! I'm a fast learner. ",
    "Sounds like an adventure!  Can I come along? ",
    "That's a new one for me!  Thanks for teaching me something new! ",
    "You got me curious!  Let's explore this together. ",
    "Anything is possible!  Let's dream it up together. "
  ]
}
