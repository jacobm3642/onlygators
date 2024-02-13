import flask
import sqlite3
from handers import db_tools

db_handler = db_tools.db_handler()
users = db_handler.add_db("Users", "users.db")
db_handler.add_query("Users", "register_user", "INSERT INTO Users (UserName, Password, Email) VALUES (?, ?, ?);")
db_handler.add_query("Users", "get_all_users", "SELECT * FROM users", read_only=True)
db_handler.add_query("Users", "remove_all_users", "DELETE FROM Users;")
db_handler.databases["Users"].set_perms(0, 2, 99)
#`print(db_handler.execute_premade_query("Users","get_all_users",0))

app = flask.Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    pass

@app.route("/register", methods=['POST'])
def register():
    data = flask.request.get_json()
    username, password, email = data
    db_handler.execute_premade_query("Users", "register_user", permission_level=2, parameters=(username, password, email))
    out_db()
    return flask.jsonify([""]), 200

def out_db():
    print(db_handler.execute_premade_query("Users","get_all_users",0))

def clear():
    db_handler.execute_premade_query("Users", "remove_all_users", 2)

@app.route("/test", methods=['POST'])
def test():
    data = flask.request.get_json()
    return flask.jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
