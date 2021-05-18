from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.book import Book

@app.route('/books')
def books_page():
    return render_template("books.html", books=Book.get_all())

@app.route('/books/add', methods=["POST"])
def add_book():
    data = {
        "title": request.form["book_title"],
        "pages": int(request.form["num_pages"])
    }
    book_id = Book.add(data)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    return render_template("book_show.html", book = Book.get_with_favorites(id))

@app.route('/books/<int:id>/add_author', methods=["POST"])
def add_favorite_author(id):
    author_id = request.form["author_id"]
    Book.add_favorite(id, author_id)
    return redirect(f'/books/{id}')