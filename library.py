from lists_from_files import (
    get_list_of_books_from_json,
    get_list_of_members_from_json,
    get_list_of_rentings_from_json
)
from renting import Renting
import json


class Library:
    def __init__(self):
        self.list_of_books = get_list_of_books_from_json('books.json')
        self.list_of_members = get_list_of_members_from_json('members.json')
        self.list_of_rentings = get_list_of_rentings_from_json('rentings.json')

    def add_book_to_library(self, book):
        self.list_of_books.append(book)
        self.update_books_file()

    def remove_book_from_library(self, book):
        self.list_of_books.remove(book)
        self.update_books_file()

    def add_member_to_library(self, member):
        self.list_of_members.append(member)
        self.update_members_file()

    def remove_member_from_library(self, member):
        self.list_of_members.remove(member)
        self.update_members_file()

    def add_renting_to_library(self, renting):
        self.list_of_rentings.append(renting)
        self.update_rentings_file()

    def remove_renting_from_library(self, renting):
        self.list_of_rentings.remove(renting)
        self.update_rentings_file()

    def borrow_book(self, user, book):
        book.borrow()
        renting = Renting(book)
        user.borrow_a_book(renting)
        self.list_of_rentings.append(renting)
        self.update_books_file('books.json')
        self.update_rentings_file('rentings.json')
        self.update_members_file('members.json')

    def list_of_books_to_json(self):
        temp_books_data = {
            'Books': [
                book.export_to_json()
                for book in self.list_of_books
            ]
        }
        return temp_books_data

    def list_of_members_to_json(self):
        temp_members_data = {
            'Members': [
                member.export_to_json()
                for member in self.list_of_members
            ]
        }
        return temp_members_data

    def list_of_rentings_to_json(self):
        temp_rentings_data = {
            'Rentings': [
                renting.export_to_json()
                for renting in self.list_of_rentings
            ]
        }
        return temp_rentings_data

    def update_books_file(self, filename):
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_books_to_json(), file_handle)

    def update_rentings_file(self, filename):
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_rentings_to_json(), file_handle)

    def update_members_file(self, filename):
        with open(filename, 'w+') as file_handle:
            json.dump(self.list_of_members_to_json(), file_handle)
