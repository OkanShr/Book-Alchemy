from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an author in the library database.

    Attributes:
        id (int): Primary key, unique identifier for each author.
        name (str): Name of the author, cannot be null.
        birth_date (date): Birth date of the author, cannot be null.
        date_of_death (date): Date of death of the author, can be null.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __init__(self, name, birth_date, date_of_death=None):
        """
        Initializes an Author instance.

        """
        self.name = name
        self.birth_date = birth_date
        self.date_of_death = date_of_death

    def __repr__(self):
        """
        Provides a string representation of an Author instance for debugging.

        Returns:
            str: String representation of the Author.
        """
        return f"<Author {self.name}>"

    def __str__(self):
        """
        Provides a string representation of an Author instance for display.

        Returns:
            str: Name of the Author.
        """
        return self.name


class Book(db.Model):
    """
    Represents a book in the library database.

    Attributes:
        id (int): Primary key, unique identifier for each book.
        isbn (str): International Standard Book Number, unique for each book,
         cannot be null.
        title (str): Title of the book, cannot be null.
        publication_year (int): Year the book was published, cannot be null.
        author_id (int): Foreign key linking to the author of the book,
        cannot be null.
        author (Author): Relationship to the Author model.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)

    author = db.relationship('Author', backref=db.backref('books',
                                                          lazy=True))

    def __init__(self, isbn, title, publication_year, author_id):
        """
        Initializes a Book instance.

        """
        self.isbn = isbn
        self.title = title
        self.publication_year = publication_year
        self.author_id = author_id

    def __repr__(self):
        """
        Provides a string representation of a Book instance for debugging.

        Returns:
            str: String representation of the Book.
        """
        return f"<Book {self.title} (ISBN: {self.isbn})>"

    def __str__(self):
        """
        Provides a string representation of a Book instance for display.

        Returns:
            str: Title of the Book.
        """
        return self.title
