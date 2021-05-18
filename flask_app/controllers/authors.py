from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author

@app.route('/authors')
def authors_page():
    return render_template("authors.html", authors = Author.get_all())

@app.route('/authors/add', methods=["POST"])
def add_author():
    data = {
        "name": request.form["author_name"]
    }
    Author.add(data)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_author(id):
    return render_template("author_show.html", author = Author.get_with_favorites(id))

@app.route('/authors/<int:id>/add_book', methods = ["POST"])
def add_favorite_book(id):
    book_id = request.form["book_id"]
    Author.add_favorite(id, book_id)
    return redirect(f'/authors/{id}')