from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@flaskdb.c2yc4eqv2wba.eu-west-3.rds.amazonaws.com/FlaskAWS'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key ="asecretkey"

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price


@app.route('/')
def index():  # put application's code here
    books = Book.query.all()
    return render_template('index.html',books=books)


@app.route('/add/', methods=['POST'])
def insert_book():
    if request.method == 'POST':
        book = Book(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("book added successfully")
        return redirect(url_for('index'))
@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get("id"))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book is updated")
        return  redirect(url_for('index'))
@app.route('/delete/<id>/', methods = ['GET','POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
