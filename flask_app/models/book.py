from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author as a

class Book:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.pages = int(data["num_of_pages"])
        self.fav_authors = []
        self.not_fav_authors = []

    @classmethod
    def get_all(cls):
        books = []
        query = "SELECT * FROM books;"
        books_from_db = connectToMySQL('books_schema').query_db(query)
        for book in books_from_db:
            books.append(cls(book))
        return books

    @classmethod
    def add(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(pages)s);"
        book_id = connectToMySQL('books_schema').query_db(query, data)
        return book_id

    @classmethod
    def get_with_favorites(cls, id):
        book = cls(connectToMySQL('books_schema').query_db(f"SELECT * FROM books WHERE id={int(id)}")[0])
        query1 = f"SELECT * FROM books JOIN favorites ON books.id = favorites.book_id JOIN authors ON authors.id = favorites.author_id WHERE books.id = {int(id)};"
        book_fav_authors = connectToMySQL('books_schema').query_db(query1)
        fav_author_ids = []
        for author in book_fav_authors:
            author_data = {
                "id": author["authors.id"],
                "name": author["name"]
            }
            fav_author_ids.append(str(author["author_id"]))
            book.fav_authors.append(a.Author(author_data))

        fav_author_ids = ','.join(fav_author_ids)
        query2 = f"SELECT * FROM authors WHERE NOT FIND_IN_SET(id, '{fav_author_ids}');"
        book_not_fav_authors = connectToMySQL('books_schema').query_db(query2)
        for author in book_not_fav_authors:
            book.not_fav_authors.append(a.Author(author))
        return book

    @classmethod
    def add_favorite(cls, id, author_id):
        query = f"INSERT INTO favorites (book_id, author_id) VALUES ({id}, {author_id});"
        return connectToMySQL('books_schema').query_db(query)