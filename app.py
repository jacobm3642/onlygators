import flask
import sqlite3
import hashlib
from handers import db_tools
from secrets import token_urlsafe
from flask_cors import CORS

db_handler = db_tools.db_handler()
users = db_handler.add_db("Users", "users.db")
db_handler.databases["Users"].set_perms(0, 2, 99)

app = flask.Flask(__name__, static_url_path='/static')
CORS(app)

CORS(app, resources={r"/register": {"origins": "http://localhost:5000"}})

def hash_b(data):
    salt = "silly96"
    data_with_salt = data + salt
    hashed = hashlib.sha256(data_with_salt.encode()).hexdigest()
    return hashed

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/getRegister", methods=['POST'])
def getRegister():
    return flask.render_template("register.html")

@app.route("/getLogin", methods=['POST'])
def getLogin():
    return flask.render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    try:
        data = [data_stringify(i) for i in flask.request.get_json()]
        print(hash_b(data[1]))
        print(data)
    except:
        pass
    return flask.jsonify([]), 200

@app.route("/arb", methods=["POST"])
def pull_html():
    try:
        data = [data_stringify(i) for i in flask.request.get_json()]
        code, html = data
        if code == "jacob12345":
            return flask.render_template(f"./{html}.html")
        else:
            raise ValueError("unauthorized")
    except:
        return flask.jsonify(["unauthorized"]), 401

@app.route("/register", methods=['POST'])
def register():
    try:
        data = [data_stringify(i) for i in flask.request.get_json()]
        email, username, password = data
        password = hash_b(password)
        if not db_handler.execute_premade_query("Users", "register_user", permission_level=2, parameters=(username, password, email)):
            return flask.jsonify(["user already exsits"]), 400
        out_db()
        print(username)
        id = db_handler.execute_premade_query("Users", "get_user_id", 0, parameters=(username,))

        token = insert_token(id[0][0])
        return flask.jsonify([token]), 200
    except:
        return  flask.jsonify(["Panic"]), 500


@app.route("/test", methods=['POST'])
def test():
    data = flask.request.get_json()
    return flask.jsonify(data)

def data_stringify(string):
    string = str(string)
    if len(string) >= 255:
        raise ValueError("TO LONG")
    return string

def out_db():
    print(db_handler.execute_premade_query("Users","get_all_users",0))

def clear():
    db_handler.execute_premade_query("Users", "remove_all_users", 2)

def insert_token(userId):
    token = token_urlsafe(32)
    print(token)
    try:
        if db_handler.execute_premade_query("Users", "add_token", 2, parameters=(userId, token)) != False:
            return token
        raise ValueError("token already exsiests")
    except:
        return insert_token(userId)

def init_db_handler():
    db_handler.add_query("Users", "create_token_table", "CREATE TABLE token_table(userID INTEGER, token varchar(255), FOREIGN KEY(userID) REFERENCES users(Id))")
    db_handler.add_query("Users", "create_user_table", "create table users( Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName varchar(255) NOT NULL UNIQUE, Password varchar(255) NOT NULL, Email varchar(255) NOT NULL UNIQUE);")


    db_handler.add_query("Users", "register_user", "INSERT INTO Users (UserName, Password, Email) VALUES (?, ?, ?);")
    db_handler.add_query("Users", "get_all_users", "SELECT * FROM users", read_only=True)
    db_handler.add_query("Users", "remove_all_users", "DELETE FROM Users;")
    db_handler.add_query("Users", "display_tables", "SELECT name FROM sqlite_master WHERE type='table'")
    db_handler.add_query("Users", "add_token", "INSERT INTO token_table(userID, token) VALUES (?, ?)")
    db_handler.add_query("Users", "get_user_id", "SELECT Id FROM Users WHERE UserName = ?", read_only=True)
    db_handler.add_query("Users", "drop_table_user", "DROP TABLE users;")
    db_handler.add_query("Users", "drop_table_token", "DROP TABLE token_table;")

def runtime_test():
    print(db_handler.execute_premade_query("Users","get_all_users",0))
    # db_handler.execute_premade_query("Users","create_token_table", 2)
    print(db_handler.execute_premade_query("Users", "display_tables", 2))

def reset_db():
    db_handler.execute_premade_query("Users","drop_table_user", 99)
    db_handler.execute_premade_query("Users","drop_table_token", 99)
    db_handler.execute_premade_query("Users","create_user_table", 99)
    db_handler.execute_premade_query("Users","create_token_table", 99)

if __name__ == "__main__":
    init_db_handler()
    reset_db()
    app.run(host="127.0.0.1", port=5000)
