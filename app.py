import flask
import sqlite3
from handers import db_tools

#db_handler = db_tools.db_handler()
#users = db_handler.add_db("Users", "users.db")
#db_handler.add_query("Users", "get_all_users", "SELECT * FROM users", read_only=True)
#db_handler.databases["Users"].set_perms(0, 99, 99)
#print(db_handler.execute_premade_query("Users","get_all_users",0))


app = flask.Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
