from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import time
import sqlite3

app = Flask(__name__)

class Todo:
	def __init__(self, todo, publ):
		self.name = todo
		self.publ = publ

def init_db():
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	try:
		c.execute("SELECT * FROM todos")
	except:
		c.execute("""CREATE TABLE todos (
				todo text,
				publ text
			)""")
	conn.commit()
	conn.close()

init_db()

def new_todo(todo):
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	c.execute("INSERT INTO todos VALUES (?, ?)",(todo,
		time.strftime("%D.%M.%Y")))
	conn.commit()
	conn.close()

def clear_todo(todo):
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	c.execute("DELETE FROM todos WHERE todo == ?", todo)
	conn.commit()
	conn.close()

def get_all_todos():
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	res = []
	for todo in c.execute("SELECT * FROM todos"):
		res.append(Todo(
				todo[0],
				todo[1]
			))
	return res
	conn.commit()
	conn.close()

@app.route("/")
def index():
	return render_template("index.html", todos=get_all_todos())

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/confirm")
def confirm():
	return render_template("confirm.html")

@app.route("/create", methods=["POST"])
def create():
	todo_name = request.form.get("todo")
	new_todo(todo_name)
	return redirect(url_for("confirm"))

if __name__ == "__main__":
	app.run(debug=True)