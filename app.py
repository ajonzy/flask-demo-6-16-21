from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    author = db.Column(db.String, nullable=False)
    review = db.Column(db.String)

    def __init__(self, title, author, review):
        self.title = title
        self.author = author
        self.review = review

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "review")

book_schema = BookSchema()
multiple_book_schema = BookSchema(many=True)


@app.route("/book/add", methods=["POST"])
def add_book():
    post_data = request.get_json()
    title = post_data.get("title")
    author = post_data.get("author")
    review = post_data.get("review")

    record = Book(title, author, review)

    db.session.add(record)
    db.session.commit()

    return jsonify("Book added successfully")

@app.route("/book/get", methods=["GET"])
def get_all_books():
    all_books = db.session.query(Book).all()
    return jsonify(multiple_book_schema.dump(all_books))

@app.route("/book/get/<id>", methods=["GET"])
def get_book(id):
    book = db.session.query(Book).filter(Book.id == id).first()
    return jsonify(book_schema.dump(book))

@app.route("/book/update/<id>", methods=["PUT"])
def update_book(id):
    book = db.session.query(Book).filter(Book.id == id).first()

    put_data = request.get_json()
    title = put_data.get("title")
    author = put_data.get("author")
    review = put_data.get("review")

    if title:
        book.title = title

    if author:
        book.author = author

    if review:
        book.review = review

    db.session.commit()

    return jsonify("Book updated successfully")

@app.route("/book/delete/<id>", methods=["DELETE"])
def delete_book(id):
    book = db.session.query(Book).filter(Book.id == id).first()
    db.session.delete(book)
    db.session.commit()

    return jsonify("Book deleted successfully")


if __name__ == "__main__":
    app.run(debug=True)