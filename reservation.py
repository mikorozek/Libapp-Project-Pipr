from dataclasses import dataclass
from book import Book


@dataclass
class Reservation:
    """
    Class representing reservation. It represents amount of time
    when reservation is active and book which is being booked.
    :param book: Book class instance, book that is being booked
    :param beginning_date: str, date in day/month/year format
    :param expire_date: str, date in day/month/year format, defaultly
        set week after beginning_date
    """
    book: Book
    beginning_date: str
    expire_date: str

    @classmethod
    def import_from_json(cls, reservation_data):
        """
        Creates a Reservation class instance from JSON data.
        :param reservation_data: JSON data that contains information
            about book, and reservation dates
        :return: Reservation class instance
        """
        book = Book.import_from_json(reservation_data['Book'])
        beginning_date = reservation_data['Beginning date']
        expire_date = reservation_data['Expire date']
        return cls(book, beginning_date, expire_date)

    def export_to_json(self):
        """
        Creates a dictionary that can be added to JSON file with
        booking information.
        :return: dic
        """
        json_reservation_data = {
            'Book': self.book.export_to_json(),
            'Beginning date': self.beginning_date,
            'Expire date': self.expire_date
        }
        return json_reservation_data
