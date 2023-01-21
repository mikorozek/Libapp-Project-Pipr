from misc_functions.lists_from_files import (
    get_list_of_books_from_json,
    get_list_of_members_from_json,
    get_list_of_rentings_from_json
)
from misc_functions.time_functions import updated_date_format_for_renting
from classes.renting import Renting
from classes.libapp_exceptions import (
    AvailableBookReservationError,
    TakenLoginError
)
import json


BOOKS_PATH = "jsonfiles/books.json"
MEMBERS_PATH = "jsonfiles/members.json"
RENTINGS_PATH = "jsonfiles/rentings.json"


class Library:
    """
    Class representing Library which is called when the application starts.
    This class stores data about members, books and rentings.
    :param list_of_books: List[Book], imported data from JSON file. Variable
        contains list of Book class instances.
    :param list_of_members: List[Member], imported data from JSON file.
        Variable contains list of Member class instances.
    :param list_of_rentings: List[Renting], imported data from JSON file.
        Variable contains list of Renting class instances that have ever been
        made.
    """
    def __init__(self):
        self.list_of_books = get_list_of_books_from_json()
        self.list_of_members = get_list_of_members_from_json()
        self.list_of_rentings = get_list_of_rentings_from_json()

    def add_book_to_library(self, book):
        """
        Adds Book class instance to list of books. Then it updates JSON file
        with library books data.
        :param book: Book class instance, which we librarian wants to add to
            library
        """
        while book.id in [
            lib_book.id
            for lib_book in self.list_of_books
        ]:
            book.id = str(int(book.id) + 1).zfill(5)
        self.list_of_books.append(book)
        self.update_books_file()

    def remove_book_from_library(self, book):
        """
        Removes book instance from list of books. If book was on any member
        renting list it returns renting. It does same thing with reservation
        list. Then it updates JSON file with library books data.
        :param book: instance of Book class, which we
            want to remove from library.
        """
        for member in self.list_of_members:
            for renting in member.current_renting_list:
                if renting.book == book:
                    renting.return_renting()
                    member.return_renting(renting)
            for reservation in member.current_reservation_list:
                if reservation == book:
                    member.cancel_reservation(reservation)
        self.list_of_books.remove(book)
        self.update_books_file()
        self.update_members_file()
        self.update_rentings_file()

    def add_member_to_library(self, member):
        """
        Adds Member class instance to list of members. It checks if login is
        not taken. If it is it raises exception. Then it updates JSON file
        with library members data.
        :param member: instance of Member class, which we
            want to add to library
        :raise: Exception, raised when login has already been taken
        """
        if member.login in [
            lib_member.login
            for lib_member in self.list_of_members
        ]:
            raise TakenLoginError("This login has already been taken!")
        self.list_of_members.append(member)
        self.update_members_file()

    def remove_member_from_library(self, member):
        """
        Removes member instance from list of members. It checks if member has
        any active rentings, if yes it returns all of them. It does the same
        thing with reservations. Then it updates JSON files.
        :param member: instance of Member class, which we
            want to remove from library.
        """
        for renting in member.current_renting_list:
            renting.return_renting()
        for reservation in member.current_reservation_list:
            reservation.cancel_reservation(member.login)
        self.update_books_file()
        self.update_rentings_file()
        self.list_of_members.remove(member)
        self.update_members_file()

    def genres(self):
        """
        Method that returns list of genres of books in library.
        :return: List[str]
        """
        return list(set([book.genre for book in self.list_of_books]))

    def genre_list_of_books(self, genre):
        """
        Method that returns list of books of one specified genre.
        :param genre: str, represents genre of the books
        :return: List[Book]
        """
        return [
            book for book in self.list_of_books
            if book.genre == genre
        ]

    def borrow_book(self, user, book):
        """
        Method that checks if book is available. If book is available the
        renting class instance is created with default expire_date and renews
        params. Member class method Member.borrow_a_book() adds renting to
        current_rentings and renting_history member atributes. Then it adds
        Renting to library list of rentings and updates all JSON files.
        :param user: instance of Member class, which wants to
            borrow a book.
        "param book: instance of Book class, which somebody
            wants to borrow.
        """
        book.borrow()
        renting = Renting(book)
        user.borrow_a_book(renting)
        self.list_of_rentings.append(renting)
        self.update_books_file()
        self.update_rentings_file()
        self.update_members_file()

    def make_a_reservation(self, user, book):
        """
        Method that makes reservation in database. If book is available it can
        be rented so it raises Exception. It updates the database JSON files.
        :param user: Member class instance, client that is making a reservation
        :param book: Book class instance, book that client is reserving
        :raise: Exception, when book is available and can be borrowed
        """
        if book.available:
            raise AvailableBookReservationError("You can borrow the book.")
        user.make_reservation(book)
        self.update_books_file()
        self.update_members_file()
        self.update_rentings_file()

    def renew_renting(self, renting):
        """
        Method that renews renting. It also updates library database.
        :param renting: Renting class instance, renting that user wants
            to renew
        """
        renting.renew()
        self.update_members_file()
        self.update_rentings_file()

    def return_book(self, user, renting):
        """
        Method that returns book to library. It also updates library database.
        :param user: Member class instance, user that returns book to library
        :param renting: Renting class instance, renting that user wants to
            make unactive. Renting.book represents book that user wants to
            return
        """
        renting.return_renting()
        user.return_renting(renting)
        self.update_books_file()
        self.update_rentings_file()
        self.update_members_file()

    def cancel_reservation(self, user, reservation):
        """
        Method that cancels reservation made by the user in the past. It also
        updates library database.
        :param user: Member class instance, client that cancels the reservation
        :param reservation: Book class instance, book that will no longer be
            booked by user
        """
        user.cancel_reservation(reservation)
        reservation.cancel_reservation(user.login)
        self.update_books_file()
        self.update_members_file()
        self.update_rentings_file()

    def month_amount_of_rentings(self, month):
        """
        Method that returns list of rentings done in the library last 12
        months. That is why list has 12 elements. It is used in plot display.
        """
        amount = 0
        for renting in self.list_of_rentings:
            if updated_date_format_for_renting(
                renting.beginning_date
            ) == month:
                amount += 1
        return amount

    def list_of_books_to_json(self):
        """
        Creates a dictionary that can be added to JSON file from list of books.
        :return: dic
        """
        temp_books_data = {
            'Books': [
                book.export_to_json()
                for book in self.list_of_books
            ]
        }
        return temp_books_data

    def list_of_members_to_json(self):
        """
        Creates a dictionary that can be added to JSON file from list of
        members.
        :return: dic
        """
        temp_members_data = {
            'Members': [
                member.export_to_json()
                for member in self.list_of_members
            ]
        }
        return temp_members_data

    def list_of_rentings_to_json(self):
        """
        Creates a dictionary that can be added to JSON file from list of
        rentings.
        :return: dic
        """
        temp_rentings_data = {
            'Rentings': [
                renting.export_to_json()
                for renting in self.list_of_rentings
            ]
        }
        return temp_rentings_data

    def update_books_file(self, path=BOOKS_PATH):
        """
        Updates JSON file with data from list of books atribute.
        :param path: path to JSON file which we want to update, defaultly set
            to books.json file
        """
        with open(path, 'w+') as file_handle:
            json.dump(self.list_of_books_to_json(), file_handle)

    def update_rentings_file(self, path=RENTINGS_PATH):
        """
        Updates JSON file with data from list of rentings atribute.
        :param path: path to JSON file which we want to update, defaultly set
            to rentings.json file
        """
        with open(path, 'w+') as file_handle:
            json.dump(self.list_of_rentings_to_json(), file_handle)

    def update_members_file(self, path=MEMBERS_PATH):
        """
        Updates JSON file with data from list of members atribute.
        :param path: path to JSON file which we want to update, defaultly set
            to members.json file
        """
        with open(path, 'w+') as file_handle:
            json.dump(self.list_of_members_to_json(), file_handle)
