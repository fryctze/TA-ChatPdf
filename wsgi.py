import os
from dotenv import load_dotenv
from quanta_quire import start_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path)

app = start_app()
