# Library Management Application

This repository contains a library management application built in Python. The application provides functionality for both readers and librarians, allowing users to browse books, borrow books, and manage their library activities.

## Project Structure

The project repository is organized as follows:

- **Classes:** Contains the Python class files used in the project, including classes for books, rentals, members, and the library itself.
- **Misc_functions:** Contains modules responsible for specific functions, such as plotting statistics and handling time-related operations.
- **UI:** Contains the code for the graphical user interface (GUI) implemented using PyQt and the designer tool.
- **Tests:** Contains tests for classes and functions, focusing on non-GUI-related code.
- **Jsonfiles:** Contains JSON files used to store library data.

## Getting Started

To run the library management application on your local machine, follow these steps:

1. Clone this repository to your local machine using the following command:
```
git clone https://github.com/your-username/Library-App.git
```

2. Install the required dependencies. You can use the following command to install the dependencies using pip:
```
pip install pyside2
```
```
pip install matplotlib
```

3. Launch the application by running the main script:
```
python3 main.py
```

## Usage

Upon launching the application, users are prompted to enter their login credentials. Two pre-configured accounts are available:
- **Client Mode:** Username: `testclient`
- **Librarian Mode:** Username: `testlib`

After logging in, clients can browse books by genre, borrow books, and view their current rentals. Librarians have additional capabilities, such as managing books and member accounts.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code according to your needs.

## Contact

For any inquiries or feedback, please contact [mikolajrozek0@gmail.com](mailto:mikolajrozek0@gmail.com).

