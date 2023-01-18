import json
from book import Book
from renting import Renting
from member import Member


def get_list_of_books_from_json(filename):
    """
    Function that imports JSON data and transforms it
    into list of Book class instances.
    :param filename: path to JSON file
    :return: List[Book]
    """
    with open(filename, 'r') as file_handle:
        dic = json.load(file_handle)
    return [
        Book.import_from_json(data)
        for data in dic['Books']
        ]


def get_list_of_rentings_from_json(filename):
    """
    Function that imports JSON data and transforms it
    into list of Renting class instances.
    :param filename: path to JSON file
    :return: List[Renting]
    """
    with open(filename, 'r') as file:
        dic = json.load(file)
    return [
        Renting.import_from_json(data)
        for data in dic['Rentings']
        ]


def get_list_of_members_from_json(filename):
    """
    Function that imports JSON data and transforms it
    into list of Member class instances.
    :param filename: path to JSON file
    :return: List[Member]
    """
    with open(filename, 'r') as file:
        dic = json.load(file)
    return [
        Member.import_from_json(data)
        for data in dic['Members']
        ]
