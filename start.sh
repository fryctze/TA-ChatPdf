# For development use (simple logging, etc):
#pip3 install -r requirements_second.txt
# flask --app server run --port $PORT
python app.py
# For production use: 
#gunicorn wsgi:app -w 1 --log-file -
#gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:application