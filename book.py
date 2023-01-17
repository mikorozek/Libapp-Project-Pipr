from dataclasses import dataclass


@dataclass
class Book:
    title: str
    authors: str
    genre: str
    id: str
    available: bool
    reservation: bool

    @classmethod
    def import_from_json(cls, book_data):
        title = book_data['Title']
        authors = book_data['Authors']
        genre = book_data['Genre']
        id = book_data['Id']
        available = book_data['Available']
        reservation = book_data['Reservation']
        return cls(title, authors, genre, id, available, reservation)

    def export_to_json(self):
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
        return f'{self.title} - {self.authors}'

    def status(self):
        if self.available:
            return 'Available'
        return 'Unavailable'

    def reservation_string_status(self):
        if self.is_booked():
            return 'Booked'
        else:
            return 'Not booked'

    def change_status(self):
        self.available = not self.available

    def is_booked(self):
        return self.reservation

    def change_reservation_status(self):
        self.reservation = not self.reservation

    def borrow(self):
        if self.available:
            self.change_status()
        else:
            raise ValueError
