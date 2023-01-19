from time_functions import todays_date, default_expiration_date, update_date
from book import Book
from dataclasses import dataclass
from typing import Union


@dataclass
class Renting:
    """
    Class representing renting of book. It contains attributes that
    describe renting.
    :param book: Book class instance, book that is being borrowed
    :param beginning_date: str, date in day/month/year format. Contains
        info when renting has been made. Defaultly set to day of Renting
        creation.
    :param expire_date: str | None, date in day/month/year format. Contains
        info about renting expiration date. Defaultly set 3 months after
        beginning_date. If book was returned to library it changes
        itself to None
    :param return_date: str | None, date in day/month/year format. Contains
        info whether renting ended or not. If its value is None the book is
        still borrowed. If its value is str the book was returned to library.
    :param renew: int, conatins info about amount of renews. Defaultly set to
        2.
    """
    book: Book
    beginning_date: str = todays_date()
    expire_date: Union[str, None] = default_expiration_date()
    return_date: Union[str, None] = None
    renews: Union[int, None] = 2

    @classmethod
    def import_from_json(cls, renting_data):
        """
        Creates a Renting class instance from JSON data.
        :param renting_data: JSON data that contains renting information
        :return: Renting class instance
        """
        book = Book.import_from_json(renting_data['Book'])
        beginning_date = renting_data['Beginning date']
        expire_date = renting_data['Expire date']
        return_date = renting_data['Return date']
        renews = renting_data['Renews amount']
        return cls(book, beginning_date, expire_date, return_date, renews)

    def export_to_json(self):
        """
        Creates a dictionary that can be added to JSON file with renting
        information.
        :return: dic
        """
        json_renting_data = {
            'Book': self.book.export_to_json(),
            'Beginning date': self.beginning_date,
            'Expire date': self.expire_date,
            'Return date': self.return_date,
            'Renews amount': self.renews,
        }
        return json_renting_data

    def renew(self):
        """
        Renews the renting. Elongates the time by one month. If amount
        of renews is lesser or equal to 0 it raises error.
        """
        if not self.renews:
            raise ValueError
        self.renews -= 1
        if self.renews == 0:
            self.renews = None
        self.expire_date = update_date(self.expire_date, 1)

    def return_renting(self):
        """
        Method that returns book to library. This method updates book status,
        sets expire_date to None and return_date to day of returning.
        """
        self.book.change_status()
        self.return_date = todays_date()
        self.expire_date = None

    def __str__(self):
        """
        Method that returns string in Title - Authors of rented book format.
        :return: str
        """
        return f'{self.book.title} - {self.book.authors}'
