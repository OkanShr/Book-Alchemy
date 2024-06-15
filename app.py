from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from data_models import db, Author, Book
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd()) + "\library.sqlite"

app.config['SECRET_KEY'] = '123123123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Add a new author to the database.

    If the request method is POST:
        Validates the input from the form.
        Checks if the author already exists.
        If not, creates a new Author object and adds it to the database.

    Returns:
        str: Rendered HTML template with success or error message.
    """
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Validate input
        if not name or not birth_date_str:
            return "Name and birth date are required."

        try:
            birth_date = datetime.strptime(
                birth_date_str, '%Y-%m-%d').date()
            date_of_death = datetime.strptime(
                date_of_death_str, '%Y-%m-%d').date() \
                if date_of_death_str else None
        except ValueError:
            return "Incorrect date format. Please use yyyy-mm-dd."

        # Check if the Author already exists
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            message = f"Author '{name}' already exists."
            return render_template('add_author.html',
                                   message=message)

        # Create Author object and add to database
        new_author = Author(name=name, birth_date=birth_date,
                            date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        # Success message
        message = f"Author '{name}' successfully added."

        # Render template with success message
        return render_template('add_author.html',
                               message=message)

    return render_template('add_author.html',
                           message=message)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book_page():
    """
    Display the add book form and handle form submission.

    If the request method is POST:
        Validates the input from the form.
        Checks if the book already exists.
        If not, creates a new Book object and adds it to the database.

    Returns:
        str: Rendered HTML template with success or error message.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        # Validate input
        if not (isbn and title and publication_year and author_id):
            message = f"Fill the form correctly."
            return render_template('add_book.html',
                                   message=message, authors=authors)

        # Check if the ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            message = f"Book with ISBN '{isbn}' already exists."
            return render_template('add_book.html',
                                   message=message, authors=authors)

        # Create Book object and add to database
        new_book = Book(isbn=isbn,
                        title=title,
                        publication_year=publication_year,
                        author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        # Success message
        message = f"Book '{title}' successfully added."

        # Render template with success message
        return render_template('add_book.html',
                               message=message, authors=authors)

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book from the database.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        redirect: Redirects to the home page.
    """
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id

    try:
        db.session.delete(book)
        db.session.commit()

        # Check if the author has no other books
        author = Author.query.get(author_id)
        if author and not author.books:
            db.session.delete(author)
            db.session.commit()

        flash(f"Book '{book.title}' has been successfully deleted.",
              'success')
    except:
        flash(f"An error occurred while deleting the book "
              f"'{book.title}'.", 'danger')

    return redirect(url_for('home_page'))


@app.route('/')
def home_page():
    """
    Display the home page with a list of books.

    Query parameters:
        sort_by (str): Sorts books by 'title', 'author', 'published_oldest',
            'published_newest', or 'title_reverse'. Default is 'title'.
        search (str): Filters books by title containing the search term.

    Returns:
        str: Rendered HTML template with list of books, authors, and message.
    """
    sort_by = request.args.get('sort_by', 'title')  # Default sort by title
    search_term = request.args.get('search', '')

    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    elif sort_by == 'published_oldest':
        books = Book.query.order_by(Book.publication_year).all()
    elif sort_by == 'published_newest':
        books = Book.query.order_by(desc(Book.publication_year)).all()
    elif sort_by == 'title_reverse':
        books = Book.query.order_by(desc(Book.title)).all()
    else:
        books = Book.query.order_by(Book.title).all()

    if search_term:
        books = Book.query.filter(Book.title.ilike(f'%{search_term}%')).all()
        if not books:
            message = f"No books found matching '{search_term}'."
        else:
            message = f"Books matching '{search_term}':"
    else:
        message = "All books:"

    authors = Author.query.all()
    return render_template('home.html', books=books,
                           authors=authors,
                           sort_by=sort_by, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
