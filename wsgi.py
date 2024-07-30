import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path)

from quanta_quire import start_app

app = start_app()
if __name__ == "__main__":
    app.run()
