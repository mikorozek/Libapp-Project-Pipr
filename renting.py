from time_functions import todays_date, default_expiration_date, update_date
from book import Book
from dataclasses import dataclass
from typing import Union


@dataclass
class Renting:
    book: Book
    beginning_date: str = todays_date()
    expire_date: Union[str, None] = default_expiration_date()
    return_date: Union[str, None] = None
    renews: int = 2

    @classmethod
    def import_from_json(cls, renting_data):
        book = Book.import_from_json(renting_data['Book'])
        beginning_date = renting_data['Beginning date']
        expire_date = renting_data['Expire date']
        return_date = renting_data['Return date']
        renews = renting_data['Renews amount']
        return cls(book, beginning_date, expire_date, return_date, renews)

    def export_to_json(self):
        json_renting_data = {
            'Book': self.book.export_to_json(),
            'Beginning date': self.beginning_date,
            'Expire date': self.expire_date,
            'Return date': self.return_date,
            'Renews amount': self.renews,
        }
        return json_renting_data

    def renew(self):
        if self._renews <= 0:
            raise ValueError
        self._renews -= 1
        self.expire_date = update_date(self.expire_date, 1)

    def return_renting(self):
        self.return_date = todays_date()
        self.expire_date = None
