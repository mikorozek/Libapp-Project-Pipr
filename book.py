from dataclasses import dataclass


@dataclass
class Book:
    """
    Class representing physical book object. Class
    contains attributes that are used to describe the
    book.
    :param title: str, title of the book
    :param authors: str, authors of the book
    :param genre: str, genre of the book
    :param id: str, id of the book
    :param available: bool, info if book is available
    :param reservation: bool, info if book is booked
    """
    title: str
    authors: str
    genre: str
    id: str
    available: bool
    reservation: bool

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
        reservation = book_data['Reservation']
        return cls(title, authors, genre, id, available, reservation)

    def export_to_json(self):
        """
        Creates a dictionary that can be added to JSON file with
        book information.
        :return: dic
        """
        json_book_data = {
            'Title': self.title,
            'Authors': self.authors,
            'Genre': self.genre,
            'Id': self.id,
            'Available': self.available,
            'Reservation': self.reservation
        }
        return json_book_data

    def __str__(self):
        """
        Method that when you call str(Book) it returns string
        Title - Authors.
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

    def string_reservation_status(self):
        """
        Method that prints information about book reservation status.
        :return: str, Booked or Not booked
        """
        if self.is_booked():
            return 'Booked'
        else:
            return 'Not booked'

    def change_status(self):
        """
        Method that changes book status information. If book is available
        it turns unavailable.
        """
        self.available = not self.available

    def is_booked(self):
        """
        Method that returns information whether book is booked.
        :return: bool
        """
        return self.reservation

    def change_reservation_status(self):
        """
        Method that changes book reservation status. If book is booked
        it becomes not booked and vice versa.
        """
        self.reservation = not self.reservation

    def borrow(self):
        """
        Method that checks if book is available. If book is not available
        it raises error. If book is available it simply turns book's status.
        """
        if self.available:
            self.change_status()
        else:
            raise ValueError
