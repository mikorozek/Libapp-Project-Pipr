# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1121, 761)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Stack = QStackedWidget(self.centralwidget)
        self.Stack.setObjectName(u"Stack")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.verticalLayout_3 = QVBoxLayout(self.home)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TitleLabel1 = QLabel(self.home)
        self.TitleLabel1.setObjectName(u"TitleLabel1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TitleLabel1.sizePolicy().hasHeightForWidth())
        self.TitleLabel1.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(28)
        self.TitleLabel1.setFont(font1)
        self.TitleLabel1.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.TitleLabel1)

        self.TitleLabel2 = QLabel(self.home)
        self.TitleLabel2.setObjectName(u"TitleLabel2")
        font2 = QFont()
        font2.setPointSize(19)
        self.TitleLabel2.setFont(font2)
        self.TitleLabel2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.TitleLabel2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.LoginLineEdit = QLineEdit(self.home)
        self.LoginLineEdit.setObjectName(u"LoginLineEdit")
        self.LoginLineEdit.setEnabled(True)
        font3 = QFont()
        font3.setPointSize(15)
        self.LoginLineEdit.setFont(font3)

        self.horizontalLayout_2.addWidget(self.LoginLineEdit)

        self.SubmitLoginButton = QPushButton(self.home)
        self.SubmitLoginButton.setObjectName(u"SubmitLoginButton")
        self.SubmitLoginButton.setFont(font3)

        self.horizontalLayout_2.addWidget(self.SubmitLoginButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.InvalidLoginErrorLabel = QLabel(self.home)
        self.InvalidLoginErrorLabel.setObjectName(u"InvalidLoginErrorLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.InvalidLoginErrorLabel.sizePolicy().hasHeightForWidth())
        self.InvalidLoginErrorLabel.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setPointSize(11)
        self.InvalidLoginErrorLabel.setFont(font4)
        self.InvalidLoginErrorLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.InvalidLoginErrorLabel)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.Stack.addWidget(self.home)
        self.client_home_page = QWidget()
        self.client_home_page.setObjectName(u"client_home_page")
        self.gridLayout_3 = QGridLayout(self.client_home_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.ClientHomeQstLabel = QLabel(self.client_home_page)
        self.ClientHomeQstLabel.setObjectName(u"ClientHomeQstLabel")
        font5 = QFont()
        font5.setFamily(u"DejaVu Serif")
        font5.setPointSize(20)
        font5.setBold(True)
        font5.setWeight(75)
        self.ClientHomeQstLabel.setFont(font5)
        self.ClientHomeQstLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.ClientHomeQstLabel, 2, 0, 1, 1)

        self.ClientHomeWelcomeLabel = QLabel(self.client_home_page)
        self.ClientHomeWelcomeLabel.setObjectName(u"ClientHomeWelcomeLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ClientHomeWelcomeLabel.sizePolicy().hasHeightForWidth())
        self.ClientHomeWelcomeLabel.setSizePolicy(sizePolicy3)
        self.ClientHomeWelcomeLabel.setFont(font5)
        self.ClientHomeWelcomeLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.ClientHomeWelcomeLabel, 1, 0, 1, 1)

        self.HelloClientLabel = QLabel(self.client_home_page)
        self.HelloClientLabel.setObjectName(u"HelloClientLabel")
        sizePolicy3.setHeightForWidth(self.HelloClientLabel.sizePolicy().hasHeightForWidth())
        self.HelloClientLabel.setSizePolicy(sizePolicy3)
        font6 = QFont()
        font6.setFamily(u"DejaVu Serif")
        font6.setPointSize(29)
        font6.setBold(True)
        font6.setWeight(75)
        self.HelloClientLabel.setFont(font6)
        self.HelloClientLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.HelloClientLabel, 0, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ClientDisplayRentingsButton = QPushButton(self.client_home_page)
        self.ClientDisplayRentingsButton.setObjectName(u"ClientDisplayRentingsButton")
        self.ClientDisplayRentingsButton.setFont(font5)

        self.gridLayout_2.addWidget(self.ClientDisplayRentingsButton, 1, 0, 1, 1)

        self.ClientDisplayHistoryButton = QPushButton(self.client_home_page)
        self.ClientDisplayHistoryButton.setObjectName(u"ClientDisplayHistoryButton")
        self.ClientDisplayHistoryButton.setFont(font5)

        self.gridLayout_2.addWidget(self.ClientDisplayHistoryButton, 2, 0, 1, 1)

        self.ClientDisplayBooksButton = QPushButton(self.client_home_page)
        self.ClientDisplayBooksButton.setObjectName(u"ClientDisplayBooksButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ClientDisplayBooksButton.sizePolicy().hasHeightForWidth())
        self.ClientDisplayBooksButton.setSizePolicy(sizePolicy4)
        self.ClientDisplayBooksButton.setFont(font5)

        self.gridLayout_2.addWidget(self.ClientDisplayBooksButton, 0, 0, 1, 1)

        self.ClientLogoutButton = QPushButton(self.client_home_page)
        self.ClientLogoutButton.setObjectName(u"ClientLogoutButton")
        self.ClientLogoutButton.setFont(font5)

        self.gridLayout_2.addWidget(self.ClientLogoutButton, 3, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.Stack.addWidget(self.client_home_page)
        self.client_display_books_page = QWidget()
        self.client_display_books_page.setObjectName(u"client_display_books_page")
        self.horizontalLayout_3 = QHBoxLayout(self.client_display_books_page)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.splitter = QSplitter(self.client_display_books_page)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.ListOfBooks = QListWidget(self.splitter)
        self.ListOfBooks.setObjectName(u"ListOfBooks")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ListOfBooks.sizePolicy().hasHeightForWidth())
        self.ListOfBooks.setSizePolicy(sizePolicy5)
        self.splitter.addWidget(self.ListOfBooks)
        self.BookListStack = QStackedWidget(self.splitter)
        self.BookListStack.setObjectName(u"BookListStack")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.BookListStack.sizePolicy().hasHeightForWidth())
        self.BookListStack.setSizePolicy(sizePolicy6)
        self.book_info_page = QWidget()
        self.book_info_page.setObjectName(u"book_info_page")
        self.gridLayout_4 = QGridLayout(self.book_info_page)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.BookGenre = QLabel(self.book_info_page)
        self.BookGenre.setObjectName(u"BookGenre")
        self.BookGenre.setFont(font3)

        self.gridLayout_4.addWidget(self.BookGenre, 2, 0, 1, 1)

        self.BookStatus = QLabel(self.book_info_page)
        self.BookStatus.setObjectName(u"BookStatus")
        self.BookStatus.setFont(font3)

        self.gridLayout_4.addWidget(self.BookStatus, 4, 0, 1, 1)

        self.ReservationButton = QPushButton(self.book_info_page)
        self.ReservationButton.setObjectName(u"ReservationButton")
        self.ReservationButton.setFont(font3)

        self.gridLayout_4.addWidget(self.ReservationButton, 8, 0, 1, 1)

        self.BookTitle = QLabel(self.book_info_page)
        self.BookTitle.setObjectName(u"BookTitle")
        self.BookTitle.setFont(font3)

        self.gridLayout_4.addWidget(self.BookTitle, 0, 0, 1, 1)

        self.BookBorrowButton = QPushButton(self.book_info_page)
        self.BookBorrowButton.setObjectName(u"BookBorrowButton")
        self.BookBorrowButton.setFont(font3)

        self.gridLayout_4.addWidget(self.BookBorrowButton, 7, 0, 1, 1)

        self.BookReservation = QLabel(self.book_info_page)
        self.BookReservation.setObjectName(u"BookReservation")
        self.BookReservation.setFont(font3)

        self.gridLayout_4.addWidget(self.BookReservation, 5, 0, 1, 1)

        self.BookAuthors = QLabel(self.book_info_page)
        self.BookAuthors.setObjectName(u"BookAuthors")
        self.BookAuthors.setFont(font3)

        self.gridLayout_4.addWidget(self.BookAuthors, 1, 0, 1, 1)

        self.BookId = QLabel(self.book_info_page)
        self.BookId.setObjectName(u"BookId")
        self.BookId.setFont(font3)

        self.gridLayout_4.addWidget(self.BookId, 3, 0, 1, 1)

        self.TempLabel = QLabel(self.book_info_page)
        self.TempLabel.setObjectName(u"TempLabel")
        self.TempLabel.setFont(font3)

        self.gridLayout_4.addWidget(self.TempLabel, 6, 0, 1, 1)

        self.BookListStack.addWidget(self.book_info_page)
        self.book_home_page = QWidget()
        self.book_home_page.setObjectName(u"book_home_page")
        self.verticalLayout_5 = QVBoxLayout(self.book_home_page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.BookStack0Label = QLabel(self.book_home_page)
        self.BookStack0Label.setObjectName(u"BookStack0Label")
        font7 = QFont()
        font7.setPointSize(17)
        self.BookStack0Label.setFont(font7)
        self.BookStack0Label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.BookStack0Label)

        self.BookListStack.addWidget(self.book_home_page)
        self.splitter.addWidget(self.BookListStack)

        self.horizontalLayout_3.addWidget(self.splitter)

        self.Stack.addWidget(self.client_display_books_page)
        self.client_display_rentings_page = QWidget()
        self.client_display_rentings_page.setObjectName(u"client_display_rentings_page")
        self.Stack.addWidget(self.client_display_rentings_page)
        self.client_display_history_page = QWidget()
        self.client_display_history_page.setObjectName(u"client_display_history_page")
        self.Stack.addWidget(self.client_display_history_page)
        self.librarian_home_page = QWidget()
        self.librarian_home_page.setObjectName(u"librarian_home_page")
        self.label = QLabel(self.librarian_home_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 30, 59, 15))
        self.Stack.addWidget(self.librarian_home_page)

        self.horizontalLayout.addWidget(self.Stack)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1121, 38))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.Stack.setCurrentIndex(2)
        self.BookListStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LibApp", None))
        self.TitleLabel1.setText(QCoreApplication.translate("MainWindow", u"Welcome to LibApp", None))
        self.TitleLabel2.setText(QCoreApplication.translate("MainWindow", u"Please, enter your login", None))
        self.LoginLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your login here...", None))
        self.SubmitLoginButton.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.InvalidLoginErrorLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.ClientHomeQstLabel.setText(QCoreApplication.translate("MainWindow", u"What would you like to do?", None))
        self.ClientHomeWelcomeLabel.setText(QCoreApplication.translate("MainWindow", u"Welcome to your account.", None))
        self.HelloClientLabel.setText(QCoreApplication.translate("MainWindow", u"Hello!", None))
        self.ClientDisplayRentingsButton.setText(QCoreApplication.translate("MainWindow", u"Display current rentings", None))
        self.ClientDisplayHistoryButton.setText(QCoreApplication.translate("MainWindow", u"Display my renting history", None))
        self.ClientDisplayBooksButton.setText(QCoreApplication.translate("MainWindow", u"Display list of books", None))
        self.ClientLogoutButton.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.BookGenre.setText("")
        self.BookStatus.setText("")
        self.ReservationButton.setText(QCoreApplication.translate("MainWindow", u"Make reservation", None))
        self.BookTitle.setText("")
        self.BookBorrowButton.setText(QCoreApplication.translate("MainWindow", u"Borrow book", None))
        self.BookReservation.setText("")
        self.BookAuthors.setText("")
        self.BookId.setText("")
        self.TempLabel.setText("")
        self.BookStack0Label.setText(QCoreApplication.translate("MainWindow", u"Choose book from list", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

