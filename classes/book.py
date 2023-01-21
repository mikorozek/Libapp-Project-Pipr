from dataclasses import dataclass, field
from classes.libapp_exceptions import UnavailableBookError
from typing import List


@dataclass
class Book:
    """
    Class representing physical book object. Class contains attributes that
    are used to describe the book.
    :param title: str, title of the book
    :param authors: str, authors of the book
    :param genre: str, genre of the book
    :param id: str, id of the book
    :param available: bool, info if book is available
    :param current_reservations: List[str], list that contains logins
    """
    title: str
    authors: str
    genre: str
    id: str
    available: bool = True
    current_reservations: List[str] = field(default_factory=list)

    @classmethod
    def import_from_json(cls, book_data):
        """
        Creates a Book class instance from JSON data.
        :param book_data: JSON data that contains book information
        :return: Book class instance
        """
        title = book_data['Title']
        authors = book_data['Authors']
        genre = book_data['Genre']
        id = book_data['Id']
        available = book_data['Available']
        current_reservations = book_data['Current reservations']
        return cls(title, authors, genre, id, available, current_reservations)

    def export_to_json(self):
        """
        Creates a dictionary that can be added to JSON file with book
        information.
        :return: dic
        """
        json_book_data = {
            'Title': self.title,
            'Authors': self.authors,
            'Genre': self.genre,
            'Id': self.id,
            'Available': self.available,
            'Current reservations': self.current_reservations
        }
        return json_book_data

    def __str__(self):
        """
        Method that when you call str(Book) it returns book info in
        Title - Authors format.
        :return: str
        """
        return f'{self.title} - {self.authors}'

    def status(self):
        """
        Method that prints information about book status.
        :return: str, Available or Unavailable
        """
        if self.available:
            return 'Available'
        return 'Unavailable'

    def amount_of_reservations(self):
        """
        Method that returns amount of current reservations.
        :return: str
        """
        return str(len(self.current_reservations))

    def change_status(self):
        """
        Method that changes book status information. If book is available it
        turns unavailable.
        """
        self.available = not self.available

    def add_reservation(self, login):
        """
        Method that adds client login to reservation list.
        """
        self.current_reservations.append(login)

    def cancel_reservation(self, login):
        """
        Method that cancels reservation. It removes client login from
        reservation list.
        """
        self.current_reservations.remove(login)

    def borrow(self, user):
        """
        Method that checks if book is available. If book is not available
        it raises exception. If book is available it simply changes book's
        status.
        :raise: Exception, when book is unavailable and has been borrowed
            by user or somebody else
        """
        if self.available:
            if user.login in self.current_reservations:
                self.current_reservations.remove(user.login)
            self.change_status()
        else:
            raise UnavailableBookError("The book is already borrowed.")
