from dataclasses import dataclass, field
from renting import Renting
from book import Book
from typing import List


@dataclass
class Member:
    name: str
    surname: str
    login: str
    status: str
    current_renting_list: List[Renting] = field(default_factory=list)
    renting_history: List[Renting] = field(default_factory=list)
    current_reservation_list: List[Book] = field(default_factory=list)

    @classmethod
    def import_from_json(cls, member_data):
        name = member_data['Name']
        surname = member_data['Surname']
        login = member_data['Login']
        status = member_data['Status']
        current_renting_list = [
            Renting.import_from_json(data)
            for data in member_data['Current rentings']
            ]
        renting_history = [
            Renting.import_from_json(data)
            for data in member_data['Renting history']
            ]
        current_reservation_list = [
            Book.import_from_json(data)
            for data in member_data['Current reservations']
            ]
        return cls(
            name,
            surname,
            login,
            status,
            current_renting_list,
            renting_history,
            current_reservation_list
            )

    def export_to_json(self):
        json_member_data = {
            'Name': self.name,
            'Surname': self.surname,
            'Login': self.login,
            'Status': self.status,
            'Current rentings': [
                renting.export_to_json()
                for renting in self.current_renting_list
                ],
            'Renting history': [
                renting.export_to_json()
                for renting in self.renting_history
            ],
            'Current reservations': [
                book.export_to_json()
                for book in self.current_reservation_list
            ]
        }
        return json_member_data

    def borrow_a_book(self, renting):
        self.current_renting_list.append(renting)
        # musi aktualizować plik json zapytać masarczyka w jaki sposób?
        self.renting_history.append(renting)

    def renew_a_book(self, renting):
        renting.renew()

    def return_a_book(self, renting):
        renting.return_renting()
        renting._book.change_status()
        self._current_renting_list.remove(renting)

    def make_a_reservation(self, book):
        self._current_reservation_list.append(book)
        book.change_reservation()
