from flask import Flask, render_template, request

app = Flask(__name__)

class Book:
    def __init__(self, title, author, ISBN, genre, available=True):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.genre = genre
        self.available = available

    def is_available(self):
        return self.available

    def borrow(self):
        if self.available:
            self.available = False
            return "BORROWING SUCCESSFUL"
        else:
            return "BORROWING UNSUCCESSFUL: Book is not available."

    def return_book(self):
        self.available = True
        return "BOOK RETURNED SUCCESSFUL"

class Member:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

class Library:
    def __init__(self):
        self.book_list = []
        self.member_list = []

    def add_book(self, book):
        self.book_list.append(book)

    def add_member(self, member):
        self.member_list.append(member)

    def borrow_book(self, book_title):
        for book in self.book_list:
            if book.title == book_title and book.is_available():
                return book.borrow()
        return "BOOK NOT FOUND OR NOT AVAILABLE"

    def return_book(self, book_title):
        for book in self.book_list:
            if book.title == book_title:
                return book.return_book()

library = Library()

book1 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "9780345391803", "Science Fiction")
book2 = Book("Pride and Prejudice", "Jane Austen", "9780140439516", "Classic Fiction")
book3 = Book("The Lord of the Rings", "J. R. R. Tolkien", "9780007527617", "Fantasy")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

member1 = Member("Mayank", 12345)
member2 = Member("Vansh", 54321)

library.add_member(member1)
library.add_member(member2)

@app.route('/')
def home():
    return render_template('index.html', books=library.book_list)

@app.route('/borrow', methods=['POST'])
def borrow():
    book_title = request.form['book_title']
    result = library.borrow_book(book_title)
    return render_template('index.html', books=library.book_list, message=result)

@app.route('/return', methods=['POST'])
def return_book():
    book_title = request.form['book_title']
    result = library.return_book(book_title)
    return render_template('index.html', books=library.book_list, message=result)

if __name__ == '__main__':
    app.run(debug=True)
