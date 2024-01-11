import flask
import sqlite3

app = flask.Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)