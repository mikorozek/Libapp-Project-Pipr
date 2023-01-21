from classes.renting import Renting
from classes.book import Book
from classes.libapp_exceptions import (
    NoRenewalsError
)
from misc_functions.time_functions import (
    todays_date,
    default_expiration_date
    )
import pytest


RENTINGS_JSON = {
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
            },
        ]
    }


def test_renting_creation():
    renting = Renting(Book('Book1', 'Authors1', 'Genre1', '00003', False))
    assert renting.book.title == 'Book1'
    assert renting.book.authors == 'Authors1'
    assert renting.book.genre == 'Genre1'
    assert renting.book.id == '00003'
    assert not renting.book.available
    assert renting.beginning_date == todays_date()
    assert renting.expire_date == default_expiration_date()
    assert not renting.return_date
    assert renting.renews == 2


def test_renting_import_from_json():
    renting = Renting.import_from_json(RENTINGS_JSON["Rentings"][0])
    assert renting.book.title == 'Book2'
    assert renting.book.authors == 'Authors2'
    assert renting.book.genre == 'Genre2'
    assert renting.book.id == '00001'
    assert not renting.book.available
    assert renting.beginning_date == "19/01/2023"
    assert renting.expire_date == "19/04/2023"
    assert not renting.return_date
    assert renting.renews == 2


def test_renting_export_to_json():
    renting = Renting.import_from_json(RENTINGS_JSON["Rentings"][0])
    assert renting.export_to_json() == RENTINGS_JSON["Rentings"][0]


def test_renew():
    renting = Renting.import_from_json(RENTINGS_JSON["Rentings"][0])
    assert renting.expire_date == "19/04/2023"
    renting.renew()
    assert renting.expire_date == "19/05/2023"
    assert renting.renews == 1
    renting.renew()
    assert renting.expire_date == "19/06/2023"
    assert not renting.renews
    with pytest.raises(NoRenewalsError):
        renting.renew()


def test_return_renting():
    renting = Renting.import_from_json(RENTINGS_JSON["Rentings"][0])
    assert not renting.book.available
    assert renting.expire_date == "19/04/2023"
    assert not renting.return_date
    renting.return_renting()
    assert renting.book.available
    assert not renting.expire_date
    assert renting.return_date == todays_date()


def test_renting_str():
    renting = Renting.import_from_json(RENTINGS_JSON["Rentings"][0])
    assert str(renting) == "Book2 - Authors2"

