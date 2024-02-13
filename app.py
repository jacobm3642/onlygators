import flask
import sqlite3
from handers import db_tools
from secrets import token_urlsafe
from flask_cors import CORS

db_handler = db_tools.db_handler()
users = db_handler.add_db("Users", "users.db")
db_handler.add_query("Users", "register_user", "INSERT INTO Users (UserName, Password, Email) VALUES (?, ?, ?);")
db_handler.add_query("Users", "get_all_users", "SELECT * FROM users", read_only=True)
db_handler.add_query("Users", "remove_all_users", "DELETE FROM Users;")
db_handler.add_query("Users", "create_token_table", "CREATE TABLE token_table(userID INTEGER, token varchar(255), FOREIGN KEY(userID) REFERENCES users(Id))")
db_handler.add_query("Users", "display_tables", "SELECT name FROM sqlite_master WHERE type='table'")
db_handler.add_query("Users", "add_token", "INSERT INTO your_table_name (userID, token) VALUES (?, ?)")
db_handler.add_query("Users", "get_user_id", "SELECT Id FROM Users WHERE UserName = ?", read_only=True)
db_handler.databases["Users"].set_perms(0, 2, 99)
# print(db_handler.execute_premade_query("Users","get_all_users",0))
# db_handler.execute_premade_query("Users","create_token_table", 2)
print(db_handler.execute_premade_query("Users", "display_tables", 2))

def insert_token(userId):
    token = token_urlsafe(32)
    try:
        db_handler.execute_premade_query("Users", "add_token", 2, parameters=(userId, token))
    except:
        return insert_token(userId)


app = flask.Flask(__name__, static_url_path='/static')
CORS(app)

CORS(app, resources={r"/register": {"origins": "http://localhost:5000"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    pass

def data_stringify(string):
    string = str(string)
    if string.legnth()>=255:
        raise ValueError("TO LONG")
    return string

@app.route("/register", methods=['POST'])
def register():
    data = [str(i) for i in flask.request.get_json()]
    username, password, email = data
    db_handler.execute_premade_query("Users", "register_user", permission_level=2, parameters=(username, password, email))
    out_db()
    id = db_handler.execute_premade_query("Users", "get_user_id", 0, parameters=(username))
    print(id)
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
    clear()
    app.run(host="127.0.0.1", port=5000)
