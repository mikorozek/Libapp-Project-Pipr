from lists_from_files import (
    get_list_of_books_from_json,
    get_list_of_members_from_json,
    get_list_of_rentings_from_json
)
from renting import Renting
from libapp_exceptions import AvailableBookReservationError
import json


class Library:
    """
    Class representing Library which is called when the application starts.
    This class stores data about members, books and rentings.
    :param list_of_books: List[Book], imported data from
        JSON file. Variable contains list of Book class
        instances.
    :param list_of_members: List[Member], imported data from
        JSON file. Variable contains list of Member class
        instances.
    :param list_of_rentings: List[Renting], imported data from
        JSON file. Variable contains list of Renting class
        instances that have ever been made.
    """
    def __init__(self):
        self.list_of_books = get_list_of_books_from_json('books.json')
        self.list_of_members = get_list_of_members_from_json('members.json')
        self.list_of_rentings = get_list_of_rentings_from_json('rentings.json')

    def add_book_to_library(self, book):
        """
        Adds Book class instance to list of books. Then it updates JSON file
        with library books data.
        :param book: instance of Book class, which we
            want to add to library.
        """
        while book.id in [
            lib_book.id
            for lib_book in self.list_of_books
        ]:
            book.id = str(int(book.id) + 1).zfill(5)
        self.list_of_books.append(book)
        self.update_books_file('books.json')

    def remove_book_from_library(self, book):
        """
        Removes book instance from list of books. Then it updates JSON file
        with library books data.
        :param book: instance of Book class, which we
            want to remove from library.
        """
        self.list_of_books.remove(book)
        for member in self.list_of_members:
            for renting in member.current_renting_list:
                if renting.book == book:
                    renting.return_renting()
                    member.current_renting_list.remove(renting)
            for reservation in member.current_reservation_list:
                if reservation == book:
                    member.current_reservation_list.remove(reservation)
        self.update_books_file('books.json')
        self.update_members_file('members.json')
        self.update_rentings_file('rentings.json')

    def add_member_to_library(self, member):
        """
        Adds Member class instance to list of members. Then it updates JSON
        file with library members data.
        "param member: instance of Member class, which we
            want to add to library
        """
        self.list_of_members.append(member)
        self.update_members_file()

    def remove_member_from_library(self, member):
        """
        Removes member instance from list of members. Then it updates JSON
        file with library members data.
        :param member: instance of Member class, which we
            want to remove from library.
        """
        self.list_of_members.remove(member)
        self.update_members_file()

    def add_renting_to_library(self, renting):
        """
        Adds Renting class instance to list of rentings. It updates
        rentings.json file with all rentings, that
        have ever been made in library.
        :param renting: instance of Renting class, which
            we want to add to list of rentings
        """
        self.list_of_rentings.append(renting)
        self.update_rentings_file()

    def remove_renting_from_library(self, renting):
        """
        Removes Renting class instance from list of rentings. Then it updates
        rentings.json file with all rentings, that have ever been made in
        library.
        :param renting: instance of Renting class, which
            we want to remove from list of rentings
        """
        self.list_of_rentings.remove(renting)
        self.update_rentings_file()

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
        Renting to own list of rentings and updates all JSON files.
        :param user: instance of Member class, which wants to
            borrow a book.
        "param book: instance of Book class, which somebody
            wants to borrow.
        """
        book.borrow(user)
        renting = Renting(book)
        user.borrow_a_book(renting)
        self.list_of_rentings.append(renting)
        self.update_books_file('books.json')
        self.update_rentings_file('rentings.json')
        self.update_members_file('members.json')

    def make_a_reservation(self, user, book):
        """
        Method that makes reservation in database. If book is available
        it can be rented so it raises Exception. It updates the database
        JSON files.
        :raise: Exception, when book is available and can be borrowed
        """
        if book.available:
            raise AvailableBookReservationError("You can borrow the book.")
        user.make_reservation(book)
        self.update_books_file('books.json')
        self.update_members_file('members.json')

    def renew_renting(self, renting):
        """
        Method that renews renting. It also updates library database.
        :param renting: Renting class instance, renting that user wants
            to renew
        """
        renting.renew()
        self.update_members_file('members.json')
        self.update_rentings_file('rentings.json')

    def return_book(self, user, renting):
        """
        Method that returns book to library. It also updates library database.
        :param user: Member class instance, user that returns book to library
        :param renting: Renting class instance, renting that user wants to
            deactivate. Renting.book represents book that user wants to return
        """
        renting.return_renting()
        user.return_renting(renting)
        self.update_books_file('books.json')
        self.update_rentings_file('rentings.json')
        self.update_members_file('members.json')

    def cancel_reservation(self, user, reservation):
        """
        Method that cancels reservation made by the user in the past.
        It also updates library database.
        :param user: Member class instance, user that cancels the reservation
        :param reservation: Book class instance, book that will no longer be
            booked
        """
        user.cancel_reservation(reservation)
        reservation.cancel_reservation(user.login)
        self.update_books_file('books.json')
        self.update_members_file('members.json')
        self.update_rentings_file('rentings.json')

    def list_of_books_to_json(self):
        """
        Creates a dictionary that can be added to JSON file
        from list of books.
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
        Creates a dictionary that can be added to JSON file
        from list of members.
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
        Creates a dictionary that can be added to JSON file
        from list of rentings.
        :return: dic
        """
        temp_rentings_data = {
            'Rentings': [
                renting.export_to_json()
                for renting in self.list_of_rentings
            ]
        }
        return temp_rentings_data

    def update_books_file(self, filename):
        """
        Updates JSON file with data from list of books
        atribute.
        :param filename: path to JSON file which we
            want to update
        """
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_books_to_json(), file_handle)

    def update_rentings_file(self, filename):
        """
        Updates JSON file with data from list of rentings
        atribute.
        :param filename: path to JSON file which we
            want to update
        """
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_rentings_to_json(), file_handle)

    def update_members_file(self, filename):
        """
        Updates JSON file with data from list of members
        atribute.
        :param filename: path to JSON file which we
            want to update
        """
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_members_to_json(), file_handle)
