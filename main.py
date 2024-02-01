from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# calling the app and tell her what she can access
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# create the database with the corresponding keys
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# ensure that the database tables are created
with app.app_context():
    db.create_all()

# create the route books which should show the list of books after adding them
@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

# you can add a book here
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
  # using the POST method to make sure we can post data here, with all the needed keys
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
      
# this helps with context issues
        with app.app_context():
            new_book = Book(title=title, author=author, publication_year=publication_year)
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('list_books'))

    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
