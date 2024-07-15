from flask import Flask

app = Flask(__name__)


@app.route('/foo')
def serve_foo():
  return 'This page is served via Flask!'


# default port is 5000
app.run(port=8888)
