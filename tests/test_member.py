from classes.member import Member
from classes.renting import Renting
from classes.book import Book
from classes.libapp_exceptions import (
    DoubleReservationError,
    RentedBookReservationError
)
import pytest

MEMBER_JSON = {
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
    ]
}


def test_member_creation():
    member = Member('Name1', 'Surname1', 'Login1', 'Client')
    assert member.name == "Name1"
    assert member.surname == "Surname1"
    assert member.login == "Login1"
    assert member.status == "Client"
    assert not member.current_renting_list
    assert not member.renting_history
    assert not member.current_reservation_list


def test_member_creation_from_json():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert member.name == "Name1"
    assert member.surname == "Surname1"
    assert member.login == "Login1"
    assert member.status == "Client"
    assert member.current_renting_list[0].book.title == "Book2"
    assert member.current_renting_list[0].book.genre == "Genre2"
    assert member.current_renting_list[0].beginning_date == "19/01/2023"
    assert member.renting_history[0].book.title == "Book2"
    assert member.renting_history[0].book.genre == "Genre2"
    assert not member.renting_history[0].return_date
    assert member.current_reservation_list[0].title == "Book1"
    assert member.current_reservation_list[0].id == "00000"


def test_member_imoprt_to_json():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert member.export_to_json() == MEMBER_JSON["Members"][0]


def test_member_borrow_a_book():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    renting = Renting(
        Book("Title1", "Authors6", "Genre4", "00009"))
    member.borrow_a_book(renting)
    assert renting in member.current_renting_list
    assert renting in member.renting_history


def test_member_make_reservation():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    reservation = Book("Title1", "Authors6", "Genre4", "00009")
    member.make_reservation(reservation)
    assert member.login in reservation.current_reservations
    assert reservation in member.current_reservation_list
    with pytest.raises(DoubleReservationError):
        member.make_reservation(reservation)


def test_member_make_reservation_rented_book():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    reservation = Book.import_from_json({
                        "Title": "Book2",
                        "Authors": "Authors2",
                        "Genre": "Genre2",
                        "Id": "00001",
                        "Available": False,
                        "Current reservations": []
                    })
    with pytest.raises(RentedBookReservationError):
        member.make_reservation(reservation)


def test_cancel_reservation():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    reservation = Book("Title1", "Authors6", "Genre4", "00009")
    member.current_reservation_list.append(reservation)
    member.cancel_reservation(reservation)
    assert reservation not in member.current_reservation_list


def test_return_renting():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    renting = Renting(
        Book("Title1", "Authors6", "Genre4", "00009")
    )
    member.current_renting_list.append(renting)
    member.return_renting(renting)
    assert renting not in member.current_renting_list


def test_history_date_rentings():
    date = "19/01/2023"
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    renting = Renting(
        Book("Title1", "Authors6", "Genre4", "00009")
    )
    member.renting_history.append(renting)
    assert member.current_renting_list[0].beginning_date == "19/01/2023"
    assert member.renting_history_date_rentings(date)[0].beginning_date == "19/01/2023"
    assert renting not in member.renting_history_date_rentings(date)


def test_active_rentings_amount():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert member.active_rentings_amount() == 1


def test_active_reservations_amount():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert member.active_reservations_amount() == 1


def test_month_amount_of_renting_in_history():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert member.month_amount_of_rentings_in_history("01/2023") == 1


def test_str():
    member = Member.import_from_json(MEMBER_JSON["Members"][0])
    assert str(member) == "Name1 Surname1 - Login1"
