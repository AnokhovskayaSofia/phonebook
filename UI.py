import sys
from PyQt5.QtGui import QIcon, QBrush, QColor, QRegExpValidator
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QDate, QRegExp
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QDesktopWidget, \
                            QApplication, QLineEdit, QGridLayout, QCheckBox, \
                            QDateEdit, QCommandLinkButton, QVBoxLayout, QTabWidget, \
                            QTableView, QSpacerItem, QSizePolicy, QHBoxLayout, \
                            QLabel


class LoginUI(QWidget):
    """Class for display interface of login screen"""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(open("style.qss", "r").read())

    def initUI(self):
        """Initializes interface of login screen"""
        self.resize(500, 300)
        self.center()
        self.setWindowTitle('Вход')

        self.btnLogin = QPushButton('Вход', self)
        self.btnRegistration = QPushButton('Регистрация', self)
        self.editUsername = QLineEdit(self)
        self.editUsername.setPlaceholderText('Имя пользователя')
        self.editPassword = QLineEdit( self)
        self.editPassword.setPlaceholderText('Пароль')
        self.editPassword.setEchoMode(QLineEdit.Password)
        self.ChRemember = QCheckBox('Запомни меня', self)      
        self.btnSeePassword = QPushButton(QIcon('./icons/close_eye.png'), '' , self)
        self.btnSeePassword.setCheckable(True)
        self.btnForgotPassword = QCommandLinkButton('Забыли пароль?', self)

        layout = QGridLayout()
        layout.addWidget(self.editUsername, 0, 0)
        layout.addWidget(self.editPassword, 1, 0)
        layout.addWidget(self.btnSeePassword, 1, 1)
        layout.addWidget(self.ChRemember, 2, 0)
        layout.addWidget(self.btnLogin, 3, 0)
        layout.addWidget(self.btnRegistration, 4, 0)
        layout.addWidget(self.btnForgotPassword, 5, 0)
        layout.addItem(QSpacerItem(10, 40, QSizePolicy.Policy.Fixed , \
                                   QSizePolicy.Policy.Expanding), 6, 0)

        self.setLayout(layout)
        self.show()
    
    def get_login_user(self):
        """Getter for login data from the interface"""
        data = {
            'username': self.editUsername.text(),
            'password': self.editPassword.text()
        }
        return data

    def set_visibility_password(self):
        """Sets visibitily of password depending on pushbutton"""
        state = self.btnSeePassword.isChecked()

        if state:
            self.editPassword.setEchoMode(QLineEdit.Normal)
            self.btnSeePassword.setIcon(QIcon('./icons/open_eye.png'))
        else:
            self.editPassword.setEchoMode(QLineEdit.Password) 
            self.btnSeePassword.setIcon(QIcon('./icons/close_eye.png'))       
    
    def center(self):
        """Centering the window relative to the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RegistrationUI(QWidget):
    """Class for display interface of registration screen"""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(open("style.qss", "r").read())

    def initUI(self):
        """Initializes interface of registration screen"""
        self.resize(500, 300)
        self.center()

        self.setWindowTitle('Регистрация')
        self.editUsername = QLineEdit(self)
        self.editUsername.setPlaceholderText(' Имя пользователя')
        self.editPassword = QLineEdit(self)
        self.editPassword.setPlaceholderText(' Пароль')
        self.editRepeatPassword = QLineEdit(self)
        self.editRepeatPassword.setPlaceholderText(' Повторите пароль')
        self.editEmail = QLineEdit(self)
        self.editEmail.setPlaceholderText(' Адрес электронной почты')
        self.editEmail.setToolTip('Электронная почта в формате example@example.examle')
        self.editEmail.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+")))
        self.editBirthday = QDateEdit(self)
        self.btnRegistration = QPushButton('Регистрация', self)

        layout = QVBoxLayout()
        layout.addWidget(self.editUsername)
        layout.addWidget(self.editPassword)
        layout.addWidget(self.editRepeatPassword)
        layout.addWidget(self.editEmail)
        layout.addWidget(self.editBirthday)
        layout.addWidget(self.btnRegistration)
        layout.addStretch()

        self.setLayout(layout)
        self.show()
    
    def get_registration_user(self):
        """Getter for registration data from the interface"""
        data = {
            'username': self.editUsername.text(),
            'password': self.editPassword.text(),
            'rep_password': self.editRepeatPassword.text(),
            'email': self.editEmail.text(),
            'date': self.editBirthday.text()
        }
        return data
    
    def center(self):
        """Centering the window relative to the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ForgotPasswordUI(QWidget):
    """Class for display interface of 'Forgot Password' screen"""
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setStyleSheet(open("style.qss", "r").read())

    def initUI(self):
        """Initializes interface of 'Forgot Password' screen"""
        self.resize(500, 300)
        self.center()

        self.setWindowTitle('Восстановление пароля')
        self.editEmail = QLineEdit(self)
        self.editEmail.setPlaceholderText(' Адрес электронной почты')
        self.editEmail.setToolTip('Электронная почта в формате example@example.examle')
        self.btnChangePassword = QPushButton('Восстановить пароль', self)

        self.editEmail.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+")))

        layout = QVBoxLayout()
        layout.addWidget(self.editEmail)
        layout.addWidget(self.btnChangePassword)
        layout.addStretch()

        self.setLayout(layout)
        self.show()
    
    def center(self):
        """Centering the window relative to the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ContactsUI(QWidget):
    """Class for display main screen interface and work with contacts data"""
    def __init__(self):
        super().__init__()

        self.tabs_names = [' АБ ', ' ВГ ', ' ДЕ ', ' ЖЗИЙ ', ' КЛ ', ' МН ', \
                           ' ОП ', ' РС ', ' ТУ ', ' ФХ ', \
                           ' ЦЧШЩ ', ' ЪЫЬЭ ', ' ЮЯ ']
        self.tabs_letters = [' АаБб ', ' ВвГг ', ' ДдЕе ', ' ЖжЗзИиЙй ', ' КкЛл ', ' МмНн ', \
                           ' ОоПп ', ' РрСс ', ' ТтУу ', ' ФфХх ', \
                           ' ЦцЧчШшЩщ ', ' ЪъЫыЬьЭэ ', ' ЮюЯя ']
        self.tabs = []
        self.initUI()
        self.setStyleSheet(open("style.qss", "r").read())

    def closeEvent(self, event):
        """Convinces in closing main window"""
        self.reply = QMessageBox.question(self, "Закрыть программу? ",
            "Вы уверены, что хотите закрыть программу? ",
            QMessageBox.Yes,
            QMessageBox.Cancel)
        if self.reply == QMessageBox.Yes:
            event.accept() 
        else:
            event.ignore()

    def initUI(self):
        """Initializes interface of main screen"""
        self.resize(1000, 900)
        self.center()

        self.setWindowTitle('Книга контактов')

        self.tabBook = QTabWidget(self)
        self.tabBook.setTabPosition(QTabWidget.TabPosition.West)

        layout = QVBoxLayout()
        horizont = QHBoxLayout()

        self.BtnUsername = QPushButton('Добро пожаловать ', self)
        self.BtnUsername.setToolTip('Выйти из учетной записи')
        self.btnCreateUser = QPushButton('Создать новый контакт', self)
        horizont.addStretch()
        horizont.addWidget(self.btnCreateUser)
        horizont.addStretch()
        horizont.addWidget(self.BtnUsername)
        
        self.birthday_tab = QTableView()
        self.birthday_tab.horizontalHeader().hide()
        self.birthday_tab.verticalHeader().hide()
        self.birthday_tab.setColumnHidden(0, True)
        self.tabBook.addTab(self.birthday_tab, QIcon('./icons/birthday-cake.png'), '')

        for name in self.tabs_names:
            tab = QTableView()
            tab.horizontalHeader().hide()
            tab.verticalHeader().hide()
            tab.setColumnHidden(0, True)
            self.tabs.append(tab)
            self.tabBook.addTab(tab, name)


        layout.addLayout(horizont)
        layout.addWidget(self.tabBook)

        self.setLayout(layout)
        self.show()

    def fill_tables(self, data):
        """Shows all contacts on main screen"""
        separated_contacts = self.prepare_contact(data)
        num_letter = 0
        for view in self.tabs:
            view.setModel(self.TableModel(separated_contacts[num_letter]))
            num_letter += 1
        
        birthdays = self.birthday_contacts(data)
        self.birthday_tab.setModel(self.TableModel(birthdays))

    def fill_username(self, username):
        """Fills username on main screen"""
        self.BtnUsername.setText(self.BtnUsername.text() + username)
    
    def center(self):
        """Centering the window relative to the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def prepare_contact(self, data):
        """Divides contacts relay on russian alphabet letters"""
        result = []
        for letters in self.tabs_letters:
            tab = []
            for contact in data:
                if contact[1][0] in letters:
                    tab.append(contact)
            result.append(tab)
        
        return result
    
    def birthday_contacts(self, data):
        """Finds all contacts with birthday on this week"""
        result = []
        today = QDate.currentDate()
        end_of_week = today.addDays(7)
        for contact in data:
            birthday = QDate(today.year(), int(contact[4][5]+contact[4][6]), int(contact[4][8]+contact[4][9]))
            if birthday >= today and birthday <= end_of_week:
                result.append(contact)

        return result

    def check_letter_tab(self, lastname):
        """Finds on what tab new contact will be"""
        if lastname:
            for letters in self.tabs_letters:
                if lastname[0] in letters:
                    return f'Контакт отобразится на вкладке  "{letters}"'
            return f'Для фамилии {lastname} нет вкладки!!!'


    class TableModel(QAbstractTableModel):
            """Table model for contacts"""

            def __init__(self, data):
                super().__init__()
                self.data = data

            def data(self, index, role):
                if role == Qt.ForegroundRole:
                    return QBrush(QColor(169, 183, 198))
                if role == Qt.DisplayRole:
                    if index.column() == 0:
                        return QVariant()
                    return self.data[index.row()][index.column()]

            def rowCount(self, index):
                if not self.data:
                    return 0
                return len(self.data)

            def columnCount(self, index):
                if not self.data:
                    return 0
                return 5

            def headerData(self, col, orientation, role):
                if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                    return QVariant()
                return QVariant()


class ContactFormUI(QWidget):
    """Class for display interface of registration screen"""
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.initUI()
        self.setStyleSheet(open("style.qss", "r").read())

    def initUI(self):
        """Initializes interface of registration screen"""
        self.resize(500, 300)
        self.center()

        self.setWindowTitle(self.status + ' контакта')
        self.editFirstName = QLineEdit(self)
        self.editFirstName.setPlaceholderText(' Имя')
        self.editFirstName.setToolTip('Только буквы кириллицы')
        self.editFirstName.setValidator(QRegExpValidator(QRegExp("[а-яА-Я\-]+")))
        self.editSecondName = QLineEdit(self)
        self.editSecondName.setPlaceholderText(' Фамилия')
        self.editSecondName.setToolTip('Только буквы кириллицы')
        self.editSecondName.setValidator(QRegExpValidator(QRegExp("[а-яА-Я\-]+")))
        self.editPhone = QLineEdit( self)
        self.editPhone.setPlaceholderText(' Телефон')
        self.editPhone.setToolTip('Телефон в формате 87776665544, без пробелов и знаков припинания')
        self.editPhone.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
        self.editBirthday = QDateEdit(self)
        self.editBirthday.setToolTip('Дата рождения день/месяц/год')
        self.btnSubbmit = QPushButton(self.status, self)
        self.btnDelete = QPushButton('Удалить', self)
        self.btnDelete.setHidden(True)


        layout = QVBoxLayout()
        layout.addWidget(self.editFirstName)
        layout.addWidget(self.editSecondName)
        layout.addWidget(self.editPhone)
        layout.addWidget(self.editBirthday)
        layout.addWidget(self.btnSubbmit)

        if self.status == 'Редактировать':
            self.btnDelete.setHidden(False)
            layout.addWidget(self.btnDelete)

        layout.addStretch()

        self.setLayout(layout)
        self.show()

    def set_data_in_form(self, data):
        """Sets all data in contact form"""
        self.editSecondName.setText(data['secondname'])
        self.editFirstName.setText(data['firstname'])
        self.editPhone.setText(data['phone'])
        self.editBirthday.setDate(QDate(int(data['year']), int(data['month']), int(data['day'])))
    
    def get_new_contact_data(self):
        """Returns all data of new contact"""
        data = {
            'firstname': self.editFirstName.text(),
            'lastname': self.editSecondName.text(),
            'phone': self.editPhone.text(),
            'birthday': self.editBirthday.date().toString(Qt.ISODate )
        }
        return data

    def center(self):
        """Centering the window relative to the screen"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())