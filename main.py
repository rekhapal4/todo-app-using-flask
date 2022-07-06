from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    #creating database

class Todo(db.Model):           #creating database model
    id = db.Column(db.Integer, primary_key=True)       #unique value for each item
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list = Todo.query.all()     #return list of all todo items
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods = ["POST"])
def add():                       #add new item
    title = request.form.get("title")        
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))        #to refresh the page after adding new items

@app.route('/update/<int:todo_id>')
def update(todo_id):                       
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(to):                       
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()

    # new_todo = Todo(title="Todo 1", complete = False)
    # db.session.add(new_todo)
    # db.session.commit()


    app.run(debug=True)