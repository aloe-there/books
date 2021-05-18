from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book

class Author:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.fav_books = []
        self.not_fav_books = []

    @classmethod
    def get_all(cls):
        authors = []
        query = "SELECT * FROM authors;"
        authors_from_db = connectToMySQL('books_schema').query_db(query)
        for author in authors_from_db:
            authors.append(cls(author))
        return authors

    @classmethod
    def add(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        author_id = connectToMySQL('books_schema').query_db(query, data)
        return author_id

    @classmethod
    def get_with_favorites(cls, id):
        author = cls(connectToMySQL('books_schema').query_db(f"SELECT * FROM authors WHERE id={int(id)}")[0])
        query1 = f"SELECT * FROM authors JOIN favorites ON authors.id = favorites.author_id JOIN books ON books.id = favorites.book_id WHERE authors.id = {int(id)};"
        author_fav_books = connectToMySQL('books_schema').query_db(query1)
        fav_book_ids = []
        for book in author_fav_books:
            book_data = {
                "id": book["books.id"],
                "title": book["title"],
                "num_of_pages": book["num_of_pages"]
            }
            fav_book_ids.append(str(book["book_id"]))
            author.fav_books.append(Book(book_data))

        fav_book_ids = ','.join(fav_book_ids)
        query2 = f"SELECT * FROM books WHERE NOT FIND_IN_SET(id, '{fav_book_ids}');"
        author_not_fav_books = connectToMySQL('books_schema').query_db(query2)
        for book in author_not_fav_books:
            author.not_fav_books.append(Book(book))
        return author
    
    @classmethod
    def add_favorite(cls, id, book_id):
        query = f"INSERT INTO favorites (author_id, book_id) VALUES ({id}, {book_id});"
        return connectToMySQL('books_schema').query_db(query)
