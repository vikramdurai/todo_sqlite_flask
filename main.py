# get dependencies
from flask import Flask
# Flask function to render a Jinja template
# If you don't know what Jinja is, head
# over to jinja.pocoo.org
from flask import render_template
# Flask function to get form 
# data
from flask import request
# these say what they mean
from flask import redirect
from flask import url_for

# also we need 
# a database to store the to-dos in
import sqlite3
# and we need time to tell the time
# at the time the to-do is created
import time

# create our Flask app instance
app = Flask(__name__)

# We need this to store a recognizable to-do
# format for our templates to process
class Todo:
	def __init__(self, todo, publ):
		self.name = todo
		self.publ = publ

# initialize the database if it hasn't
# been created yet
def init_db():
	# connect to the database, "database.db"
	conn = sqlite3.connect("database.db")
	# create a cursor to manipulate database
	# data
	c = conn.cursor()
	try:
		# get all todos
		# to check if there even is a 
		# "todos" table
		c.execute("SELECT * FROM todos")
	except:
		# create the table
		c.execute("""CREATE TABLE todos (
				todo text,
				publ text
			)""")
	# commit and remove
	# the connection
	conn.commit()
	conn.close()

init_db()

# create a new to-do
def new_todo(todo):
	# again, connect to the database
	conn = sqlite3.connect("database.db")
	# and create a cursor
	c = conn.cursor()
	# create a new row in the table with "todo"
	# set to the name of the todo
	# and "publ" set to the current time
	c.execute("INSERT INTO todos VALUES (?, ?)",(todo,
		time.strftime("%D.%M.%Y")))
	conn.commit()
	conn.close()

# remove a todo
def clear_todo(todo):
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	# remove all rows from the database
	# in which the rows in question must 
	# have "todo" set to todo
	c.execute("DELETE FROM todos WHERE todo == ?", (todo))
	conn.commit()
	conn.close()

# this is needed by
# the index to fetch all
# todos.
# this returns an array of
# instances of the Todo class
# we made earlier
def get_all_todos():
	conn = sqlite3.connect("database.db")
	c = conn.cursor()
	# the array
	res = []
	# fetch all todos and append them to 
	# "res". What "SELECT" returns is a tuple,
	# so we convert it to a instance of the
	# "Todo" class
	for todo in c.execute("SELECT * FROM todos"):
		res.append(Todo(
				todo[0],
				todo[1]
			))
	# return the array
	return res
	conn.commit()
	conn.close()

# map the route for 
# the root url ("/")
# to the "index.html" template
@app.route("/")
def index():
	return render_template("index.html", todos=get_all_todos())

# same
@app.route("/new")
def new():
	return render_template("new.html")

# confirm if the todo
# was created succesfully
@app.route("/confirm")
def confirm():
	return render_template("confirm.html")

# actually call the "new_todo" method
# to create the todo
@app.route("/create", methods=["POST"])
def create():
	todo_name = request.form.get("todo")
	new_todo(todo_name)
	return redirect(url_for("confirm"))

# run the app
if __name__ == "__main__":
	app.run(debug=True)