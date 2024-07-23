import threading
import json
import os

data_lock = threading.Lock()

DATA_FILE = 'chat_log.json'


def load_data():
  with data_lock:
    if os.path.exists(DATA_FILE):
      with open(DATA_FILE, 'r') as file:
        return json.load(file)
    return {}


def save_data(data):
  with data_lock:
    with open(DATA_FILE, 'w') as file:
      json.dump(data, file)
