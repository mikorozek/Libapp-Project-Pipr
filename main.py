from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidgetItem,
    QMessageBox
)
from PySide2.QtGui import (
    QTextCharFormat,
    QBrush,
    QColor
)
from PySide2.QtCore import QDate
from library import Library
import sys
from ui_libapp import Ui_MainWindow


class LibAppWindow(QMainWindow):
    """
    This class represents window that is displayed when the application starts.
    In __init__ every method that sets up the app is initialized.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.library = Library()
        self.ui.Stack.setCurrentWidget(self.ui.home)
        self.current_user = None
        self.setupHomePage()
        self.setupClientHomePage()
        self.setupMainMenuButtons()
        self.setupClientDisplayBooksPage()
        self.setupClientDisplayRentingsPage()
        self.setupClientRentingHistoryPage()

    def setupHomePage(self):
        """
        This method sets up submit button at the very first page.
        """
        self.ui.submitLoginButton.clicked.connect(self.submitHomeButtonClick)

    def submitHomeButtonClick(self):
        """
        This method is called when Submit button is clicked at the very
        first page. It asks user to enter his login to verify whether he is
        librarian or client. If user is a client it sets up for Client-Mode.
        If he is a librarian it sets up for Librarian-Mode. If entered value
        is not in the database it simply shows error.
        """
        self.login = self.ui.loginLineEdit.text()
        try:
            self.setCurrentUser()
            if self.current_user.status == 'Client':
                self.setupCurrentRentingList()
                self.setupGenreList()
                self.setGreenBackgroundEffectCalendar()
                self.ui.Stack.setCurrentWidget(self.ui.client_home_page)
            elif self.current_user.status == 'Librarian':
                self.ui.Stack.setCurrentWidget(self.ui.librarian_home_page)
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("There is no account with such login in database.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def setupClientHomePage(self):
        """
        This method sets up the buttons on client's main menu page.
        """
        self.ui.clientLogoutButton.clicked.connect(
            self.logout
        )
        self.ui.clientDisplayBooksButton.clicked.connect(
            self.clientDisplayBooksPage
        )
        self.ui.clientDisplayHistoryButton.clicked.connect(
            self.clientDisplayHistoryPage
        )
        self.ui.clientDisplayRentingsButton.clicked.connect(
            self.clientDisplayRentingsPage
        )

    def setupClientDisplayBooksPage(self):
        """
        This method sets up the buttons on client's page where client can
        browse the Library books that are currently in the database.
        """
        self.ui.bookBorrowButton.clicked.connect(
            lambda: self.borrowBook(self.current_book)
            )
        self.ui.reservationButton.clicked.connect(
            lambda: self.reserveBook(self.current_book)
            )

    def setupClientDisplayRentingsPage(self):
        """
        This method sets up the buttons on client's page where client can
        browse books that he borrowed from library.
        """
        self.ui.returnBookButton.clicked.connect(
            lambda: self.returnBook(self.current_renting)
        )
        self.ui.renewRentingButton.clicked.connect(
            lambda: self.renewRenting(self.current_renting)
        )

    def setupClientRentingHistoryPage(self):
        """
        This method sets up the calendar on client's history page. Client
        can click on the calendar date that is highlighted with green colour
        to display info about rentings that have been made that day.
        """
        self.ui.rentingHistoryCalendar.selectionChanged.connect(
            self.chooseDate
            )
        self.ui.calendarStack.setCurrentIndex(0)

    def chooseDate(self):
        """
        This method is called when client click on the date button on calendar
        on renting history page. It transform QDate object from calendar which
        is returned when selected and transforms it into day/monty/year format
        string.
        """
        self.dateSelected = str(
            self.ui.rentingHistoryCalendar.selectedDate().toString("dd/MM/yyyy")
            )
        self.setupRentingHistoryList()

    def setupRentingHistoryList(self):
        """
        This method sets up list of rentings for a day on calendar which user
        clicked. If there was no renting during clicked day, it simply shows up
        error. If there was renting during clicked day it displays list of
        rentings that had been made that time.
        """
        try:
            self.ui.listOfRentingsHistory.clear()
            rentings = self.current_user.renting_history_date_rentings(
                self.dateSelected
                )
            self.ui.calendarStack.setCurrentIndex(1)
            self.ui.rentingHistoryStack.setCurrentIndex(0)
            for renting in rentings:
                item = QListWidgetItem(str(renting))
                item.renting = renting
                self.ui.listOfRentingsHistory.addItem(item)
            self.ui.listOfRentingsHistory.itemClicked.connect(
                self.rentingFromHistorySelection
            )
        except ValueError:
            self.ui.calendarStack.setCurrentIndex(0)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("You did not rent anything this day.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def rentingFromHistorySelection(self, item):
        """
        Method that is called when client clicks item on the renting history
        list for chosen day. It shows info about book that client borrowed and
        if the book was already returned or not.
        """
        self.ui.rentingHistoryStack.setCurrentIndex(1)
        self.ui.rentingHistoryRentingInfo.setText(
            f"Title: {item.renting.book.title}\n"
            f"Authors: {item.renting.book.authors}\n"
            f"Genre: {item.renting.book.genre}\n"
            f"Id: {item.renting.book.id}\n"
            f"Beginning date: {item.renting.beginning_date}\n"
            f"Returning date: {item.renting.return_date}"
        )

    def setupCurrentRentingList(self):
        """
        Method that sets up renting list for client's current rentings. Client
        can browse books that are still borrowed and not returned.
        """
        self.ui.listOfCurrentRentings.clear()
        rentings = self.current_user.current_renting_list
        self.ui.curRentingStack.setCurrentIndex(0)
        for renting in rentings:
            item = QListWidgetItem(str(renting))
            item.renting = renting
            self.ui.listOfCurrentRentings.addItem(item)
        self.ui.listOfCurrentRentings.itemClicked.connect(
            self.currentRentingSelection
            )

    def currentRentingSelection(self, item):
        """
        Method that is called when client clicks on renting representation
        on the current renting list. It shows info about renting that user
        clicks on.
        """
        self.current_renting = item.renting
        self.ui.curRentingStack.setCurrentIndex(1)
        self.ui.rentingBookInfo.setText(
            f"Title: {item.renting.book.title}\n"
            f"Authors: {item.renting.book.authors}\n"
            f"Genre: {item.renting.book.genre}\n"
            f"Id: {item.renting.book.id}"
        )
        self.ui.rentingInfo.setText(
            f"Date of renting: {item.renting.beginning_date}\n"
            f"Expiration date: {item.renting.expire_date}\n"
            f"Amount of renews: {str(item.renting.renews)}"
        )

    def setupGenreList(self):
        """
        This method sets up list of genres of books that are in library book
        database.
        """
        self.ui.listOfGenres.clear()
        genres = self.library.genres()
        self.ui.genreStack.setCurrentIndex(1)
        for genre in genres:
            item = QListWidgetItem(genre)
            item.genre = genre
            self.ui.listOfGenres.addItem(item)
        self.ui.listOfGenres.itemClicked.connect(self.genreSelection)

    def genreSelection(self, item):
        """
        This method is called when client clicks on genre representation
        on genre list. It then displays list of books from genre that had been
        clicked.
        """
        self.ui.genreStack.setCurrentIndex(0)
        self.ui.bookStack.setCurrentIndex(0)
        self.ui.listOfBooks.clear()
        books = self.library.genre_list_of_books(item.genre)
        for book in books:
            bookItem = QListWidgetItem(str(book))
            bookItem.book = book
            self.ui.listOfBooks.addItem(bookItem)
        self.ui.listOfBooks.itemClicked.connect(self.bookSelection)

    def bookSelection(self, item):
        """
        This method is called when client clicks on book representation
        on book list. It then displays info about book that client clicked
        on list.
        """
        self.current_book = item.book
        self.ui.bookStack.setCurrentIndex(1)
        self.ui.bookInfo.setText(
            f"Title: {item.book.title}\n"
            f"Authors: {item.book.authors}\n"
            f"Genre: {item.book.genre}\n"
            f"Id: {item.book.id}\n"
            f"Status: {item.book.status()}\n"
            f"Amount of reservations: {item.book.amount_of_reservations()}"
        )

    def setGreenBackgroundEffectCalendar(self):
        """
        This method sets up background effect to dates that client made a
        renting in the past or present.
        """
        self.date_list = list(set([
                QDate.fromString(renting.beginning_date, "dd/MM/yyyy")
                for renting in self.current_user.renting_history
                ]))
        dateFormat = QTextCharFormat()
        dateFormat.setBackground(QBrush(QColor("green")))
        for date in self.date_list:
            self.ui.rentingHistoryCalendar.setDateTextFormat(date, dateFormat)

    def borrowBook(self, book):
        """
        This method is called when client clicks on borrow book button on
        page where genres and books are displayed. It updates the library
        database and updates the app output. When book is already borrowed
        it shows up error message. If client borrows a book it shows message
        that book has succesfully been borrowed.
        """
        try:
            self.library.borrow_book(self.current_user, book)
            msg = QMessageBox()
            msg.setWindowTitle("Done!")
            msg.setText("You succesfully borrowed a book.")
            msg.exec_()
            self.setupGenreList()
            self.setupCurrentRentingList()
            self.setupRentingHistoryList()
            self.setGreenBackgroundEffectCalendar()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("The book is already borrowed.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def reserveBook(self, book):
        """
        This method is called when client clicks on make a reservation button
        on page where genres and books are displayed. It updates the library
        database and updates the app output. If reservation for book has
        already been made it shows up error message. If client can make a
        reservation it shows up the message that reservation has succesfully
        been made.
        """
        try:
            self.library.make_a_reservation(self.current_user, book)
            msg = QMessageBox()
            msg.setWindowTitle("Done!")
            msg.setText("You succesfully made a reservation.")
            msg.exec_()
            self.setupGenreList()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("You already made a reservation for that book.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def renewRenting(self, renting):
        """
        This method is called when client clicks on renew renting button on
        page where client's current rentings are displayed. It updates the
        library database and updates the app output. If there is no renewal
        left for the renting it shows up error message. If client can
        succesfully renew renting it shows up message that renting renewal
        has succesfully been made.
        """
        try:
            self.library.renew_renting(renting)
            msg = QMessageBox()
            msg.setWindowTitle("Done!")
            msg.setText("You succesfully renewed renting.")
            msg.exec_()
            self.setupCurrentRentingList()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("This renting has no renewal option left.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def returnBook(self, renting):
        """
        This method is called when client clicks return book button on page
        where client's current rentings are displayed. It updates the library
        database and updates the app output. It informs client that book has
        succesfully been returned to library.
        """
        self.library.return_book(self.current_user, renting)
        msg = QMessageBox()
        msg.setWindowTitle("Done!")
        msg.setText("You succesfully returned book to library.")
        msg.exec_()
        self.setupCurrentRentingList()
        self.setupRentingHistoryList()

    def logout(self):
        """
        This method is called when client clicks on logout button on client's
        main menu page. It brings user back to very first page.
        """
        self.current_user = None
        self.current_book = None
        self.current_renting = None
        self.ui.loginLineEdit.clear()
        self.ui.Stack.setCurrentWidget(self.ui.home)

    def setCurrentUser(self):
        """
        This method is called when client clicks submit button on the first
        page It checks if the entered login occur in library member database.
        If not raises error. If it does it makes self.current_user variable,
        which contains Member class instance that is currently using the
        library.
        """
        for member in self.library.list_of_members:
            if member.login == self.login:
                self.current_user = member
                return None
        raise ValueError

    def setupMainMenuButtons(self):
        """
        This method sets up buttons that take client to client's main menu.
        """
        self.ui.mainMenuButton0.clicked.connect(
            self.clientMainMenuButtonClicked
            )
        self.ui.mainMenuButton1.clicked.connect(
            self.clientMainMenuButtonClicked
            )
        self.ui.mainMenuButton2.clicked.connect(
            self.clientMainMenuButtonClicked
            )

    def clientMainMenuButtonClicked(self):
        """
        This method is called when client clicks on any main menu button.
        """
        self.ui.Stack.setCurrentWidget(self.ui.client_home_page)

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
