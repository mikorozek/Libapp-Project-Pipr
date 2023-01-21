from classes.book import Book
from classes.libapp_exceptions import UnavailableBookError
import pytest


BOOKS_JSON = {
    "Books": [
            {
                "Title": "Book1",
                "Authors": "Authors1",
                "Genre": "Genre1",
                "Id": "00000",
                "Available": True,
                "Current reservations": [
                    "Login1"
                ]
            },
            {
                "Title": "Book2",
                "Authors": "Authors2",
                "Genre": "Genre2",
                "Id": "00001",
                "Available": False,
                "Current reservations": []
            },
            {
                "Title": "Book3",
                "Authors": "Authors3",
                "Genre": "Genre3",
                "Id": "00002",
                "Available": False,
                "Current reservations": []
            }
    ]
}


def test_book_creation():
    book = Book('Title1', 'Authors1', 'Genre1', '00009', False)
    assert book.title == "Title1"
    assert book.authors == "Authors1"
    assert book.genre == "Genre1"
    assert book.id == "00009"
    assert not book.available
    assert not book.current_reservations


def test_book_import_from_json():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.title == "Book1"
    assert book.authors == "Authors1"
    assert book.genre == "Genre1"
    assert book.id == "00000"
    assert book.available
    assert book.current_reservations[0] == "Login1"


def test_book_export_to_json():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.export_to_json() == BOOKS_JSON["Books"][0]


def test_book_str():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert str(book) == "Book1 - Authors1"


def test_book_status():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.status() == "Available"


def test_book_amount_of_reservations():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.amount_of_reservations() == "1"


def test_book_change_status():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.available
    book.change_status()
    assert not book.available


def test_add_reservation():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    login = "Login2"
    book.add_reservation(login)
    assert book.amount_of_reservations() == "2"
    assert login in book.current_reservations


def test_cancel_reservation():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    login = "Login2"
    book.add_reservation(login)
    assert login in book.current_reservations
    book.cancel_reservation(login)
    assert login not in book.current_reservations


def test_borrow_book():
    book = Book.import_from_json(BOOKS_JSON["Books"][0])
    assert book.available
    book.borrow()
    assert not book.available
    with pytest.raises(UnavailableBookError):
        book.borrow()