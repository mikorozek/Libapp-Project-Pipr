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
from ui.ui_libapp import Ui_MainWindow
from classes.libapp_exceptions import (
    AvailableBookReservationError,
    InvalidLoginError,
    UnavailableBookError,
    DoubleReservationError,
    RentedBookReservationError,
    NoRenewalsError,
    InvalidDateSelectionError,
    EmptyLineError,
    WrongStatusError,
    TakenLoginError
)
from misc_functions.plot_functions import (
    generate_plot_for_member,
    generate_plot_for_library
)
from classes.book import Book
from classes.member import Member
from classes.library import Library
import sys


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
        self.currentUser = None
        self.setupHomePage()

        self.setupClientHomePage()
        self.setupClientDisplayBooksPage()
        self.setupClientDisplayRentingsPage()
        self.setupClientRentingHistoryPage()
        self.setupClientDisplayReservationsPage()

        self.setupMainMenuButtons()

        self.setupLibrarianHomePage()
        self.setupLibrarianAddBookPage()
        self.setupLibrarianRemoveBookPage()
        self.setupLibrarianAddMemberPage()
        self.setupLibrarianDisplayMembersPage()
        self.setupButtonsAddMemberBookPages()

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
            if self.currentUser.status == 'Client':
                self.setupCurrentRentingList()
                self.setupGenreList()
                self.setupReservationList()
                self.setGreenBackgroundEffectCalendar()
                self.ui.Stack.setCurrentWidget(self.ui.client_home_page)
            elif self.currentUser.status == 'Librarian':
                self.setupRemoveBookList()
                self.setupMembersList()
                self.ui.Stack.setCurrentWidget(self.ui.librarian_home_page)
        except InvalidLoginError as e:
            self.errorMessageBox(str(e))

    def setCurrentUser(self):
        """
        This method is called when client clicks submit button on the first
        page It checks if the entered login occur in library member database.
        If not, it raises exception. If it does it sets up self.currentUser
        variable, which represents Member class instance that is currently
        using the library.
        :raise: Exception, no login in library database
        """
        for member in self.library.list_of_members:
            if member.login == self.login:
                self.currentUser = member
                return None
        raise InvalidLoginError(
            "There is no account with such login in database."
            )

    def setupClientHomePage(self):
        """
        This method sets up the buttons on client's main menu page.
        """
        self.ui.clientLogoutButton.clicked.connect(
            self.clientLogout
            )
        self.ui.clientDisplayBooksButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.client_display_books_page
                )
            )
        self.ui.clientDisplayHistoryButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.client_display_history_page
                )
            )
        self.ui.clientDisplayRentingsButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.client_display_rentings_page
                )
            )
        self.ui.clientDisplayReservationsButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.client_display_reservations_page
                )
            )

    def setupClientDisplayBooksPage(self):
        """
        This method sets up the buttons on client's page where client can
        browse the Library books that are currently in the database.
        """
        self.ui.bookBorrowButton.clicked.connect(
            lambda: self.borrowBook(self.bookSelected)
            )
        self.ui.reservationButton.clicked.connect(
            lambda: self.reserveBook(self.bookSelected)
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
        self.bookSelected = item.book
        self.ui.bookStack.setCurrentIndex(1)
        self.ui.bookInfo.setText(
            f"Title: {item.book.title}\n"
            f"Authors: {item.book.authors}\n"
            f"Genre: {item.book.genre}\n"
            f"Id: {item.book.id}\n"
            f"Status: {item.book.status()}\n"
            f"Amount of reservations: {item.book.amount_of_reservations()}"
        )

    def borrowBook(self, book):
        """
        This method is called when client clicks on borrow book button on
        page where genres and books are displayed. It updates the library
        database and updates the app output. When book is already borrowed
        it shows up error message. If client borrows a book it shows message
        that book has succesfully been borrowed.
        """
        try:
            self.library.borrow_book(self.currentUser, book)
            self.doneMessageBox("You succesfully borrowed a book.")
            self.setupGenreList()
            self.setupCurrentRentingList()
            self.setupRentingHistoryList()
            self.setupReservationList()
            self.setGreenBackgroundEffectCalendar()
        except UnavailableBookError as e:
            self.errorMessageBox(str(e))

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
            self.library.make_a_reservation(self.currentUser, book)
            self.doneMessageBox("You succesfully made a reservation.")
            self.setupGenreList()
            self.setupReservationList()
        except (
            DoubleReservationError,
            RentedBookReservationError,
            AvailableBookReservationError
        ) as e:
            self.errorMessageBox(str(e))

    def setupClientDisplayRentingsPage(self):
        """
        This method sets up the buttons on client's page where client can
        browse books that he borrowed from library.
        """
        self.ui.returnBookButton.clicked.connect(
            lambda: self.returnBook(self.rentingSelected)
        )
        self.ui.renewRentingButton.clicked.connect(
            lambda: self.renewRenting(self.rentingSelected)
        )

    def setupCurrentRentingList(self):
        """
        Method that sets up renting list for client's current rentings. If
        client has no active rentings it displays information about it. If
        not client can browse books that are still borrowed and not returned.
        """
        self.ui.listOfCurrentRentings.clear()
        rentings = self.currentUser.current_renting_list
        if not rentings:
            self.ui.ifClientHasRentingStack.setCurrentIndex(1)
            return None
        self.ui.ifClientHasRentingStack.setCurrentIndex(0)
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
        self.rentingSelected = item.renting
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

    def returnBook(self, renting):
        """
        This method is called when client clicks return book button on page
        where client's current rentings are displayed. It updates the library
        database and updates the app output. It informs client that book has
        succesfully been returned to library.
        """
        self.library.return_book(self.currentUser, renting)
        self.doneMessageBox("You succesfully returned book to library.")
        self.setupGenreList()
        self.setupCurrentRentingList()
        self.setupRentingHistoryList()
        self.setupReservationList()

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
            self.doneMessageBox("You succesfully renewed renting.")
            self.setupCurrentRentingList()
        except NoRenewalsError as e:
            self.errorMessageBox(str(e))

    def setupClientRentingHistoryPage(self):
        """
        This method sets up the calendar on client's history page. Client
        can click on the calendar date that is highlighted with green colour
        to display info about rentings that have been made that day.
        """
        self.dateSelected = None
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
        :raise: Exception, when user clicks date with no rentings in his
            history
        """
        try:
            self.dateSelected = str(
                self.ui.rentingHistoryCalendar.selectedDate().toString(
                    "dd/MM/yyyy"
                    )
                )
            if self.dateSelected not in [
                renting.beginning_date
                for renting in self.currentUser.renting_history
            ]:
                raise InvalidDateSelectionError(
                    "You did not rent anything this day."
                    )
            self.setupRentingHistoryList()
        except InvalidDateSelectionError as e:
            self.ui.calendarStack.setCurrentIndex(0)
            self.errorMessageBox(str(e))

    def setupRentingHistoryList(self):
        """
        This method sets up list of rentings for a day on calendar which user
        clicked. If there was no renting during clicked day, it simply shows up
        error. If there was renting during clicked day it displays list of
        rentings that had been made that time.
        """
        if not self.dateSelected:
            return None
        self.ui.listOfRentingsHistory.clear()
        rentings = self.currentUser.renting_history_date_rentings(
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

    def setGreenBackgroundEffectCalendar(self):
        """
        This method sets up green background effect to dates that client made a
        renting in the past or present.
        """
        self.date_list = list(set([
                QDate.fromString(renting.beginning_date, "dd/MM/yyyy")
                for renting in self.currentUser.renting_history
                ]))
        dateFormat = QTextCharFormat()
        dateFormat.setBackground(QBrush(QColor("green")))
        for date in self.date_list:
            self.ui.rentingHistoryCalendar.setDateTextFormat(date, dateFormat)

    def setDefaultBackgroundEffectCalendar(self):
        """
        This method sets up default background effect to all dates on
        QCalendarWidget.
        """
        defaultDateFormat = QTextCharFormat()
        for date in self.date_list:
            self.ui.rentingHistoryCalendar.setDateTextFormat(
                date, defaultDateFormat
                )

    def setupClientDisplayReservationsPage(self):
        """
        This method sets up the buttons on client's page where client can
        browse current reservations.
        """
        self.ui.cancelReservationButton.clicked.connect(
            lambda: self.cancelReservation(self.reservationSelected)
        )
        self.ui.reservationBorrowButton.clicked.connect(
            lambda: self.borrowBook(self.reservationSelected)
        )

    def setupReservationList(self):
        """
        This method sets up client's reservation list. If client has no
        active reservations it displays information about it. If not client
        can browse active reservations.
        """
        self.ui.listOfReservations.clear()
        reservations = self.currentUser.current_reservation_list
        if not reservations:
            self.ui.ifClientHasNoReservationsStack.setCurrentIndex(1)
            return None
        self.ui.ifClientHasNoReservationsStack.setCurrentIndex(0)
        self.ui.reservationStack.setCurrentIndex(0)
        for reservation in reservations:
            item = QListWidgetItem(str(reservation))
            item.reservation = reservation
            self.ui.listOfReservations.addItem(item)
        self.ui.listOfReservations.itemClicked.connect(
            self.reservationSelection
            )

    def reservationSelection(self, item):
        """
        This method is called when client clicks on item on reservation list.
        It displays info about client reservation.
        """
        self.reservationSelected = item.reservation
        self.ui.reservationStack.setCurrentIndex(1)
        self.ui.reservationInfo.setText(
            f"Title: {item.reservation.title}\n"
            f"Authors: {item.reservation.authors}\n"
            f"Genre: {item.reservation.genre}\n"
            f"Id: {item.reservation.id}\n"
            f"Status: {item.reservation.status()}"
        )

    def cancelReservation(self, reservation):
        """
        This method is called when client clicks on cancel reservation button
        on client's reservations page. It cancels client's selected
        reservation.
        """
        self.library.cancel_reservation(self.currentUser, reservation)
        self.doneMessageBox("You succesfully cancelled reservation.")
        self.setupReservationList()
        self.setupGenreList()

    def clientLogout(self):
        """
        This method is called when client clicks on logout button on client's
        main menu page. It brings user back to very first page.
        """
        self.setDefaultBackgroundEffectCalendar()
        self.currentUser = None
        self.bookSelected = None
        self.rentingSelected = None
        self.dateSelected = None
        self.ui.loginLineEdit.clear()
        self.ui.Stack.setCurrentWidget(self.ui.home)

    def setupLibrarianHomePage(self):
        """
        Method that setups all buttons on librarian's home page.
        """
        self.ui.librarianAddBookButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.librarian_add_book_page
                )
            )
        self.ui.librarianRemoveBookButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.librarian_remove_book_page
                )
            )
        self.ui.librarianAddMemberButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.librarian_add_member_page
                )
            )
        self.ui.librarianDisplayMembersButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(
                self.ui.librarian_display_members_page
                )
            )
        self.ui.librarianDisplayRentingsInfoButton.clicked.connect(
            lambda: generate_plot_for_library(self.library)
            )
        self.ui.librarianLogoutButton.clicked.connect(
            self.librarianLogout
            )

    def setupLibrarianAddBookPage(self):
        """
        Method that sets up librarian page that shows up after clicking
        significant button.
        """
        self.addBookTitle = None
        self.addBookAuthors = None
        self.addBookGenre = None
        self.addBookId = None
        self.ui.addBookTitleLineEdit.clear()
        self.ui.addBookAuthorsLineEdit.clear()
        self.ui.addBookGenreLineEdit.clear()
        self.ui.addBookIdLineEdit.clear()

    def addBookToLibrary(self):
        """
        Method that is called when librarian clicks on button on page where
        he can add books to library. It raises Exceptions if any of the lines
        is empty except id line. If id line is empty it will take 00000 id.
        If this id is taken by another book, it will add 1 until it meets
        not taken id.
        :raise: Exception, if librarian wants to add book with no title,
            authors or genre it will show up error message.
        """
        try:
            self.addBookTitle = self.ui.addBookTitleLineEdit.text()
            self.addBookAuthors = self.ui.addBookAuthorsLineEdit.text()
            self.addBookGenre = self.ui.addBookGenreLineEdit.text()
            self.addBookId = self.ui.addBookIdLineEdit.text().zfill(5)
            if not self.addBookTitle:
                raise EmptyLineError("Book title field is empty!")
            if not self.addBookAuthors:
                raise EmptyLineError("Book authors field is empty!")
            if not self.addBookGenre:
                raise EmptyLineError("Book genre field is empty!")
            book = Book(
                self.addBookTitle,
                self.addBookAuthors,
                self.addBookGenre,
                self.addBookId
                )
            self.library.add_book_to_library(book)
            self.doneMessageBox("You succesfully added book to library.")
            self.setupLibrarianAddBookPage()
            self.setupRemoveBookList()
        except EmptyLineError as e:
            self.errorMessageBox(str(e))

    def setupLibrarianRemoveBookPage(self):
        """
        This method sets up button on book removal page. If user clicks on
        button the book currently chosen is removed.
        """
        self.ui.removeBookButton.clicked.connect(
            lambda: self.removeBook(self.bookSelected)
        )

    def setupRemoveBookList(self):
        """
        This method sets up list of books that appear after clicking remove
        book from library button while in librarian mode. If there is no
        any book in the database it shows info about it.
        """
        self.ui.removalListOfBooks.clear()
        books = self.library.list_of_books
        if not books:
            self.ui.checkIfBooksInLibraryStack.setCurrentIndex(0)
            return None
        self.ui.checkIfBooksInLibraryStack.setCurrentIndex(1)
        self.ui.bookRemovalStack.setCurrentIndex(0)
        for book in books:
            item = QListWidgetItem(str(book))
            item.book = book
            self.ui.removalListOfBooks.addItem(item)
        self.ui.removalListOfBooks.itemClicked.connect(
            self.removalBookSelection
        )

    def removalBookSelection(self, item):
        """
        This method is called when user clicks on item on list which appears
        after clicking remove book from library button. It shows info about
        chosen book item.
        """
        self.bookSelected = item.book
        self.ui.bookRemovalStack.setCurrentIndex(1)
        self.ui.bookRemoveInfo.setText(
            f"Title: {item.book.title}\n"
            f"Authors: {item.book.authors}\n"
            f"Genre: {item.book.genre}\n"
            f"Id : {item.book.id}\n"
            f"Status: {item.book.status()}\n"
            f"Amount of reservations: {item.book.amount_of_reservations()}"
        )

    def removeBook(self, book):
        """
        This method is called when user clicks on book removal button.
        It removes book from library. It also updates the library
        database and app.
        """
        self.library.remove_book_from_library(book)
        self.doneMessageBox("You succesfully removed book from library.")
        self.setupRemoveBookList()

    def setupButtonsAddMemberBookPages(self):
        """
        Method that sets up buttons on page where librarian can add member and
        on page where librarian can add book to library.
        """
        self.ui.addMemberButton.clicked.connect(self.addMemberToLibrary)
        self.ui.addBookButton.clicked.connect(self.addBookToLibrary)

    def setupLibrarianAddMemberPage(self):
        """
        This method sets up page in librarian mode that appears after clicking
        add member to library button.
        """
        self.addMemberName = None
        self.addMemberSurname = None
        self.addMemberLogin = None
        self.addMemberStatus = None
        self.ui.addMemberNameLineEdit.clear()
        self.ui.addMemberSurnameLineEdit.clear()
        self.ui.addMemberLoginLineEdit.clear()
        self.ui.addMemberStatusLineEdit.clear()

    def addMemberToLibrary(self):
        """
        This method allows librarian to add member to library. It is called
        when librarian clicks on add member to library button. It raises
        exception if any text line is not fulfilled. If every line is filled
        it creates Member class instance and adds it to library.
        """
        try:
            self.addMemberName = self.ui.addMemberNameLineEdit.text()
            self.addMemberSurname = self.ui.addMemberSurnameLineEdit.text()
            self.addMemberLogin = self.ui.addMemberLoginLineEdit.text()
            self.addMemberStatus = self.ui.addMemberStatusLineEdit.text()
            if not self.addMemberName:
                raise EmptyLineError("Member name field is empty!")
            if not self.addMemberSurname:
                raise EmptyLineError("Member surname field is empty!")
            if not self.addMemberLogin:
                raise EmptyLineError("Member login field is empty!")
            if self.addMemberStatus not in ["Client", "Librarian"]:
                raise WrongStatusError(
                    "Invalid member status!"
                    )
            member = Member(
                self.addMemberName,
                self.addMemberSurname,
                self.addMemberLogin,
                self.addMemberStatus
            )
            self.library.add_member_to_library(member)
            self.doneMessageBox("You succesfully added member to library.")
            self.setupLibrarianAddMemberPage()
            self.setupMembersList()
        except (
            EmptyLineError,
            WrongStatusError,
            TakenLoginError
        ) as e:
            self.errorMessageBox(str(e))

    def setupLibrarianDisplayMembersPage(self):
        """
        Method that sets up librarian page where he can browse clients.
        """
        self.ui.displayMemberStatisticsButton.clicked.connect(
            lambda: generate_plot_for_member(self.memberSelected)
        )
        self.ui.removeMemberButton.clicked.connect(
            lambda: self.removeMember(self.memberSelected)
        )

    def setupMembersList(self):
        """
        Method that sets up list of clients active in library. If there is no
        client in library it displays info about it. Otherwise it takes every
        client in library and adds him to the list.
        """
        self.ui.listOfMembers.clear()
        members = [
            member for member in self.library.list_of_members
            if member.status == "Client"
        ]
        if not members:
            self.ui.checkIfMemberInLibraryStack.setCurrentIndex(0)
            return None
        self.ui.checkIfMemberInLibraryStack.setCurrentIndex(1)
        self.ui.chooseMemberStack.setCurrentIndex(0)
        for member in members:
            item = QListWidgetItem(str(member))
            item.member = member
            self.ui.listOfMembers.addItem(item)
        self.ui.listOfMembers.itemClicked.connect(
            self.memberSelection
        )

    def memberSelection(self, item):
        """
        Method that is called when librarian clicks on item on member list.
        It then displays info about client of library.
        """
        self.memberSelected = item.member
        self.ui.chooseMemberStack.setCurrentIndex(1)
        self.ui.memberInfo.setText(
            f"Name: {item.member.name}\n"
            f"Surname: {item.member.surname}\n"
            f"Login: {item.member.login}\n"
            f"Active rentings: {item.member.active_rentings_amount()}\n"
            f"Active reservations: {item.member.active_reservations_amount()}"
        )

    def removeMember(self, member):
        """
        Method that is called when librarian clicks on client removal button.
        It then removes client from library and updates displayed from library
        database.
        """
        self.library.remove_member_from_library(member)
        self.doneMessageBox("You succesfully removed member from library.")
        self.setupMembersList()
        self.setupRemoveBookList()

    def librarianLogout(self):
        """
        Method that is called when librarian clicks on logout button. It
        displays very first page in the app.
        """
        self.currentUser = None
        self.bookSelected = None
        self.memberSelected = None
        self.ui.loginLineEdit.clear()
        self.ui.Stack.setCurrentWidget(self.ui.home)

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
        self.ui.mainMenuButton3.clicked.connect(
            self.clientMainMenuButtonClicked
            )
        self.ui.mainMenuButton4.clicked.connect(
            self.librarianMainMenuButtonClicked
            )
        self.ui.mainMenuButton5.clicked.connect(
            self.librarianMainMenuButtonClicked
            )
        self.ui.mainMenuButton6.clicked.connect(
            self.librarianMainMenuButtonClicked
            )
        self.ui.mainMenuButton7.clicked.connect(
            self.librarianMainMenuButtonClicked
            )

    def clientMainMenuButtonClicked(self):
        """
        This method is called when client clicks on any main menu button.
        """
        self.ui.Stack.setCurrentWidget(self.ui.client_home_page)
        self.ui.calendarStack.setCurrentIndex(0)
        self.ui.genreStack.setCurrentIndex(1)
        self.ui.curRentingStack.setCurrentIndex(0)
        self.ui.reservationStack.setCurrentIndex(0)

    def librarianMainMenuButtonClicked(self):
        """
        This method is called when librarian clicks on any main menu button.
        """
        self.ui.Stack.setCurrentWidget(self.ui.librarian_home_page)
        self.ui.chooseMemberStack.setCurrentIndex(0)
        self.ui.bookRemovalStack.setCurrentIndex(0)

    def errorMessageBox(self, e):
        """
        This method is called to signalize error.
        """
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText(e)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def doneMessageBox(self, content):
        """
        This method is called to signalize that something has been done.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Done!")
        msg.setText(content)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


def main(args):
    app = QApplication(args)
    window = LibAppWindow()
    window.show()

    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
