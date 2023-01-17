import json
from book import Book
from renting import Renting
from member import Member


def get_list_of_books_from_json(filename):
    with open(filename, 'r') as file_handle:
        dic = json.load(file_handle)
    return [
        Book.import_from_json(data)
        for data in dic['Books']
        ]


def get_list_of_rentings_from_json(filename):
    with open(filename, 'r') as file:
        dic = json.load(file)
    return [
        Renting.import_from_json(data)
        for data in dic['Rentings']
        ]


def get_list_of_members_from_json(filename):
    with open(filename, 'r') as file:
        dic = json.load(file)
    return [
        Member.import_from_json(data)
        for data in dic['Members']
        ]
