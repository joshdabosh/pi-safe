from flask import flask

app = Flask(__name__)

@app.route("/asdffdsa123")
def open():
    print(1)
    return "1"

app.run()