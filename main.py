from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidgetItem,
    QMessageBox
)
from library import Library
import sys
from ui_project import Ui_MainWindow


class LibAppWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.library = Library()
        self.ui.Stack.setCurrentWidget(self.ui.home)
        self.current_user = None
        self.setupHomePage()
        self.setupClientDisplayBooksPage()

    def setupHomePage(self):
        self.ui.SubmitLoginButton.clicked.connect(self.submitHomeButtonClick)

    def setupClientHomePage(self):
        self.ui.ClientLogoutButton.clicked.connect(
            self.logout
        )
        self.ui.ClientDisplayBooksButton.clicked.connect(
            self.clientDisplayBooksPage
        )
        self.ui.ClientDisplayHistoryButton.clicked.connect(
            self.clientDisplayHistoryPage
        )
        self.ui.ClientDisplayRentingsButton.clicked.connect(
            self.clientDisplayRentingsPage
        )

    def setupClientDisplayBooksPage(self):
        self.setupBookList()
        self.ui.BookBorrowButton.clicked.connect(
            lambda: self.borrowBook(self.current_book)
            )
        self.ui.ReservationButton.clicked.connect(
            lambda: self.reserveBook(self.current_book)
            )

    def submitHomeButtonClick(self):
        self.login = self.ui.LoginLineEdit.text()
        try:
            self.setCurrentUser()
            if self.current_user.status == 'Client':
                self.ui.Stack.setCurrentWidget(self.ui.client_home_page)
                self.setupClientHomePage()
            elif self.current_user.status == 'Librarian':
                self.ui.Stack.setCurrentWidget(self.ui.librarian_home_page)
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("There is no account with such login in database.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def setupBookList(self):
        self.ui.ListOfBooks.clear()
        books = self.library.list_of_books
        self.ui.BookListStack.setCurrentIndex(1)
        for book in books:
            item = QListWidgetItem(str(book))
            item.book = book
            self.ui.ListOfBooks.addItem(item)
        self.ui.ListOfBooks.itemClicked.connect(self.bookSelection)

    def bookSelection(self, item):
        self.current_book = item.book
        self.ui.BookListStack.setCurrentIndex(0)
        self.ui.BookTitle.setText(f'Title: {item.book.title}')
        self.ui.BookAuthors.setText(f'Authors: {item.book.authors}')
        self.ui.BookGenre.setText(f'Genre: {item.book.genre}')
        self.ui.BookId.setText(f'Id: {item.book.id}')
        self.ui.BookStatus.setText(f'Status: {item.book.status()}')
        self.ui.BookReservation.setText(
            f'Reservation status: {item.book.reservation}')

    def borrowBook(self, item):
        try:
            self.library.borrow_book(self.current_user, item)
            self.setupBookList()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("The book is already borrowed.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def logout(self):
        self.current_user = None
        self.ui.Stack.setCurrentWidget(self.ui.home)

    def setCurrentUser(self):
        for member in self.library.list_of_members:
            if member.login == self.login:
                self.current_user = member
                return None
        raise ValueError

    def clientDisplayBooksPage(self):
        self.ui.Stack.setCurrentWidget(self.ui.client_display_books_page)

    def clientDisplayRentingsPage(self):
        self.ui.Stack.setCurrentWidget(self.ui.client_display_rentings_page)

    def clientDisplayHistoryPage(self):
        self.ui.Stack.setCurrentWidget(self.ui.client_display_history_page)


def main(args):
    app = QApplication(args)
    window = LibAppWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
