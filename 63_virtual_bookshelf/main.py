# Virtual Bookshelf

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # no need for the title to be UNIQUE
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    # allow None as a value for the rating
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Book: {self.title} by {self.author}>"


with app.app_context():
    db.create_all()


def parse_rating(raw_rating):
    """Convert rating text to float, return None when invalid."""
    try:
        rating = float(raw_rating)
    except ValueError:
        return None
    return round(rating, 1)


@app.route("/")
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books, count=len(all_books))


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        rating = parse_rating(request.form["rating"])
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    book_id = request.args.get("id")
    book = Book.query.get(book_id)
    if book is not None and request.method == "POST":
        book.rating = parse_rating(request.form["new_rating"])
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book=book)


@app.route("/delete")
def delete_book():
    book_id = request.args.get("id")
    book = Book.query.get(book_id)
    if book is not None:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
