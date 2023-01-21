from classes.library import Library
from classes.renting import Renting
from classes.book import Book
from classes.member import Member
from misc_functions.time_functions import updated_date_format_for_renting
from misc_functions.time_functions import todays_date
from misc_functions.lists_from_files import (
    get_list_of_books_from_json,
    get_list_of_members_from_json,
    get_list_of_rentings_from_json
)
from classes.libapp_exceptions import (
    AvailableBookReservationError,
    TakenLoginError,
    UnavailableBookError
)
import json
import os
import tempfile
import pytest
import unittest.mock as mock


@pytest.fixture(autouse=True)
def json_data_setup():
    json_data = {
        "Members": [
            {
                "Name": "Name1",
                "Surname": "Surname1",
                "Login": "Login1",
                "Status": "Client",
                "Current rentings": [
                    {
                        "Book": {
                            "Title": "Book2",
                            "Authors": "Authors2",
                            "Genre": "Genre2",
                            "Id": "00001",
                            "Available": False,
                            "Current reservations": []
                        },
                        "Beginning date": "19/01/2023",
                        "Expire date": "19/04/2023",
                        "Return date": None,
                        "Renews amount": 2
                    }
                ],
                "Renting history": [
                    {
                        "Book": {
                            "Title": "Book2",
                            "Authors": "Authors2",
                            "Genre": "Genre2",
                            "Id": "00001",
                            "Available": False,
                            "Current reservations": []
                        },
                        "Beginning date": "19/01/2023",
                        "Expire date": "19/04/2023",
                        "Return date": None,
                        "Renews amount": 2
                    }
                ],
                "Current reservations": [
                    {
                        "Title": "Book1",
                        "Authors": "Authors1",
                        "Genre": "Genre1",
                        "Id": "00000",
                        "Available": False,
                        "Current reservations": [
                            "Login1"
                        ]
                    }
                ]
            },
            {
                "Name": "Name2",
                "Surname": "Surname2",
                "Login": "Login2",
                "Status": "Librarian",
                "Current rentings": [],
                "Renting history": [],
                "Current reservations": []
            }
        ],
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
            }
        ],
        "Rentings": [
            {
                "Book": {
                    "Title": "Book2",
                    "Authors": "Authors2",
                    "Genre": "Genre2",
                    "Id": "00001",
                    "Available": False,
                    "Current reservations": []
                },
                "Beginning date": "19/01/2023",
                "Expire date": "19/04/2023",
                "Return date": None,
                "Renews amount": 2
            }
        ]
    }
    yield json_data


def test_library_creation():
    library = Library()

    assert library.list_of_books == get_list_of_books_from_json()
    assert library.list_of_members == get_list_of_members_from_json()
    assert library.list_of_rentings == get_list_of_rentings_from_json()


def test_library_add_book(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book = Book.import_from_json(test_json_data["Books"][0])

    with mock.patch.object(library, 'update_books_file') as mock_update:
        library.add_book_to_library(book)
        assert book in library.list_of_books
        mock_update.assert_called()


def test_remove_book_from_library(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book = Book.import_from_json(test_json_data["Books"][1])
    member = Member.import_from_json(test_json_data["Members"][0])
    renting = member.current_renting_list[0]
    library.list_of_books.append(book)
    library.list_of_members.append(member)
    library.list_of_rentings.append(renting)

    with mock.patch.object(library, 'update_books_file') as mock_update1:
        with mock.patch.object(library, 'update_members_file') as mock_update2:
            with mock.patch.object(library, 'update_rentings_file') as mock_update3:
                library.remove_book_from_library(book)
                assert book not in library.list_of_books
                assert book not in [renting.book for renting in member.current_renting_list]
                assert renting.return_date == todays_date()
                mock_update1.assert_called()
                mock_update2.assert_called()
                mock_update3.assert_called()




def test_add_member_to_library(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    member1 = Member.import_from_json(test_json_data["Members"][0])
    member2 = Member.import_from_json(test_json_data["Members"][0])

    with mock.patch.object(library, 'update_members_file') as mock_update:
        library.add_member_to_library(member1)
        assert member1 in library.list_of_members
        mock_update.assert_called()

    with pytest.raises(TakenLoginError):
        library.add_member_to_library(member2)


def test_remove_member_from_library(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book = Book.import_from_json(test_json_data["Books"][1])
    member = Member.import_from_json(test_json_data["Members"][0])
    reservation = member.current_reservation_list[0]
    renting = member.current_renting_list[0]

    library.list_of_books.append(book)
    library.list_of_members.append(member)
    library.list_of_rentings.append(renting)

    with mock.patch.object(library, 'update_books_file') as mock_update1:
        with mock.patch.object(library, 'update_members_file') as mock_update2:
            with mock.patch.object(library, 'update_rentings_file') as mock_update3:
                library.remove_member_from_library(member)
                assert member not in library.list_of_members
                assert renting in library.list_of_rentings
                assert book in library.list_of_books
                assert renting.book.available
                assert renting.return_date == todays_date()
                assert reservation.current_reservations == []
                mock_update1.assert_called()
                mock_update2.assert_called()
                mock_update3.assert_called()


def test_genres(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book1 = Book.import_from_json(test_json_data["Books"][0])
    book2 = Book.import_from_json(test_json_data["Books"][1])
    library.list_of_books = [book1, book2]
    assert "Genre1" in library.genres()
    assert "Genre2" in library.genres()


def test_genre_list_of_books(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book1 = Book.import_from_json(test_json_data["Books"][0])
    book2 = Book.import_from_json(test_json_data["Books"][1])
    library.list_of_books = [book1, book2]
    assert book1 in library.genre_list_of_books('Genre1')
    assert book2 in library.genre_list_of_books('Genre2')


def test_library_borrow_book(json_data_setup):
    test_json_data = json_data_setup
    library = Library()
    book = Book.import_from_json(test_json_data["Books"][0])
    member = Member.import_from_json(test_json_data["Members"][0])
    renting = member.current_renting_list[0]
    temp_renting = Renting(book)

    library.list_of_books.append(book)
    library.list_of_members.append(member)
    library.list_of_rentings.append(renting)

    with mock.patch.object(library, 'update_books_file') as mock_update1:
        with mock.patch.object(library, 'update_members_file') as mock_update2:
            with mock.patch.object(library, 'update_rentings_file') as mock_update3:
                library.borrow_book(member, book)
                assert member.login not in book.current_reservations
                assert not book.available
                assert book in [renting.book for renting in member.current_renting_list]
                assert not member.current_reservation_list
                assert temp_renting in member.current_renting_list
                assert temp_renting in member.renting_history

                with pytest.raises(UnavailableBookError):
                    library.borrow_book(member, book)
