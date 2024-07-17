# For development use (simple logging, etc):
#pip3 install -r requirements_second.txt
python app.py
# For production use: 
#gunicorn app:app -w 1 --log-file -