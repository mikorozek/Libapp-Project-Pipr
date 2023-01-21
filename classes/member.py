from dataclasses import dataclass, field
from misc_functions.time_functions import updated_date_format_for_renting
from classes.libapp_exceptions import (
    DoubleReservationError,
    RentedBookReservationError
)
from classes.renting import Renting
from classes.book import Book
from typing import List


@dataclass
class Member:
    """
    Class representing member of library. Class contains attributes
    that describes information about member.
    :param name: str, name of member
    :param surname: str, surname of member
    :param login: str, member's login
    :param status: str, information whether member is client or librarian
    :param current_renting_list: List[Renting], list that contains
        Renting class instances that are active
    :param renting_history: List[Renting], list that contains Renting
        class instances that have ever been made
    :param current_reservation_list: List[Book], list that contains
        Reservation class instances that are active
    """
    name: str
    surname: str
    login: str
    status: str
    current_renting_list: List[Renting] = field(default_factory=list)
    renting_history: List[Renting] = field(default_factory=list)
    current_reservation_list: List[Book] = field(default_factory=list)

    @classmethod
    def import_from_json(cls, member_data):
        """
        Creates a Member class instance from JSON data.
            :param member_data: JSON data that contains information
                about renting
            :return: Member class instance
        """
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
        """
        Creates a dictionary that can be added to JSON file with member
        information.
        :return: dic
        """
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
        """
        Method adds info about book Renting to current renting list and
        renting history.
        """
        if renting.book in self.current_reservation_list:
            self.current_reservation_list.remove(renting.book)
        self.current_renting_list.append(renting)
        self.renting_history.append(renting)

    def make_reservation(self, book):
        """
        Method that makes reservation. It adds book to member's current
        reservation list. Exceptions are raised if user has already
        made a reservation for book and if user wants to make a reservation
        for a book that he borrowed.
        :raise0: Exception, when user wants to make a reservation on book
            which he has already booked
        :raise1: Exception, when user wants to make a reservation on book
            which he has already borrowed
        """
        if self.login in book.current_reservations:
            raise DoubleReservationError(
                "You already made a reservation for that book."
                )
        if book in [renting.book for renting in self.current_renting_list]:
            raise RentedBookReservationError(
                "You cannot reserve book which you have borrowed."
                )
        book.add_reservation(self.login)
        self.current_reservation_list.append(book)

    def cancel_reservation(self, book):
        """
        Method that cancels reservation. It removes user login from
        book reservation list.
        """
        self.current_reservation_list.remove(book)

    def return_renting(self, renting):
        """
        When book is returned to library it removes renting from current
        renting list.
        """
        self.current_renting_list.remove(renting)

    def renting_history_date_rentings(self, date):
        """
        Method that returns list of rentings in history with specific date.
        :param date: str, date in day/month/year format
        :return: List[Renting]
        """
        return [
            renting for renting in self.renting_history
            if renting.beginning_date == date
        ]

    def active_rentings_amount(self):
        """
        Method that returns amount of active rentings.
        :return: int
        """
        return len(self.current_renting_list)

    def active_reservations_amount(self):
        """
        Method that returns amount of active reservations.
        :return: int
        """
        return len(self.current_reservation_list)

    def month_amount_of_rentings_in_history(self, month):
        """
        Method that returns amount of rentings in history of specified month.
        :param month: str, month in month/year format
        :return: int
        """
        amount = 0
        for renting in self.renting_history:
            if updated_date_format_for_renting(
                renting.beginning_date
            ) == month:
                amount += 1
        return amount

    def __str__(self):
        """
        Method that returns info about user in Name Surname - Login format.
        :return: str
        """
        return f"{self.name} {self.surname} - {self.login}"
