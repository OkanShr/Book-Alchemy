# Book-Alchemy

A simple web application for managing a library's authors and books, built with Flask and SQLAlchemy.

## Features

- Add and delete authors.
- Add and delete books.
- Search and sort books.

# Setup Instructions
## Prerequisites
- Python 3.7+
- SQLite (included with Python standard library)
Installation

## Installation

1. Clone this repository 

- git clone https://github.com/OkanShr/Book-Alchemy.git
- cd bookalchemy

2. Create and activate virtual environment

3. Install dependencies

- pip install -r requirements.txt

4. Set up the database

- python init_db.py

5. Run the application

- python app.py

6. Open your browser and navigate to http://127.0.0.1:5000/

# Usage
## Add Author
1. Navigate to http://127.0.0.1:5000/add_author
2. Fill in the author's name, birth date, and optional date of death.
3. Click "Submit" to add the author.
## Add Book
1. Navigate to http://127.0.0.1:5000/add_book
2. Fill in the book's ISBN, title, publication year, and select the author from the dropdown.
3. Click "Submit" to add the book.
## Delete Book
1. On the home page, find the book you want to delete.
2. Click the "Delete" button next to the book.

