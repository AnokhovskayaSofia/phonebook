import sys
import mariadb
from DB import DB as database
from UI import LoginUI, RegistrationUI, ForgotPasswordUI, ContactsUI, ContactFormUI
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QCoreApplication, QSettings, QModelIndex
from validators import is_contact_valid, is_user_valid, is_email_valid
from specfunctions import send_password_email


class Login(QMainWindow):
    """Class for login logic"""
    def __init__(self):
        super().__init__()
        self.settings = QSettings( "settings_demo.conf", QSettings.IniFormat )
        self.db = database()
        self.ui = LoginUI()
        self.connecter()
        self.self_login()

    def connecter(self):
        """All connections signal slot for this class"""
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnSeePassword.clicked.connect(self.hide_password)
        self.ui.btnRegistration.clicked.connect(self.registration)
        self.ui.btnForgotPassword.clicked.connect(self.forgot_password)

    def login(self):
        """Logins user in system"""
        data = self.ui.get_login_user()

        if data:
            result = self.db.get_password(data['username'])

            if not result:
                QMessageBox.warning(self, 'Ошибка входа', \
                                    'Пользователя с таким именем не найдено', \
                                    QMessageBox.Ok )
            elif result[0][0] == data['password']:
                self.contacts_window = Contacts(data['username'])
                self.ui.close()
                self.close()
                self.settings.setValue('username', data['username'])
                self.settings.setValue('password', data['password'])
                self.settings.setValue('remember', self.ui.ChRemember.isChecked())
            else:
                QMessageBox.warning(self, 'Ошибка входа', 'Неправильный пароль', \
                                    QMessageBox.Ok)

        else:
            QMessageBox.warning(self, 'Ошибка входа', \
                                    'Неправильно заполненные поля для входа', \
                                    QMessageBox.Ok )
    
    def registration(self):
        """Redirects for registration"""
        self.registration_window = Registration()

    def forgot_password(self):
        """Redirects for password recovery"""
        self.forgot_password_window = ForgotPassword()

    def self_login(self):
        """Auto fills login and password"""
        if self.settings.value('remember', False, type=bool):
            self.ui.editUsername.setText(self.settings.value('username'))
            self.ui.editPassword.setText(self.settings.value('password'))
            self.ui.ChRemember.setChecked(self.settings.value('remember', False, \
                                          type=bool))

    def hide_password(self):
        """Hides password"""
        self.ui.set_visibility_password()


class ForgotPassword(QWidget):
    """Class of password recovery"""
    def __init__(self):
        super().__init__()  
        self.db = database()
        self.ui = ForgotPasswordUI()
        self.connecter()

    def connecter(self):
        """All connections signal slot for this class"""
        self.ui.btnChangePassword.clicked.connect(self.change_password)
    
    def change_password(self):
        """Redirects for login window"""
        data = {
            'email': self.ui.editEmail.text()
        }
        
        if is_email_valid(data['email']):
            user_id = self.db.check_user_email(data['email'])
            if user_id:
                user_data = self.db.get_contact(user_id)
                if send_password_email(data['email'], user_data):
                    QMessageBox.information(self, 'Восстановления пароля', \
                                        'Ваши данные для входа отправлены на почту', \
                                        QMessageBox.Ok )
                else:
                    QMessageBox.warning(self, 'Ошибка восстановления пароля', \
                                        'К сожалению в данный момент восстаносление через почту не работает(', \
                                        QMessageBox.Ok )
                self.login_window = Login()
                self.ui.close()
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка восстановления пароля', \
                                        'Пользователя с такой почтой нет', \
                                        QMessageBox.Ok )
        else:
            QMessageBox.warning(self, 'Ошибка восстановления пароля', \
                                        'Не правильный формат почты', \
                                        QMessageBox.Ok )


class Registration(QWidget):
    """Class for user registration"""
    def __init__(self):
        super().__init__()
        self.db = database()
        self.ui = RegistrationUI()
        self.connecter()
    
    def connecter(self):
        """All connections signal slot for this class"""
        self.ui.btnRegistration.clicked.connect(self.registration)

    def registration(self):
        """Registrats user in system"""
        data = self.ui.get_registration_user()

        if is_user_valid(data):
            if data['password'] == data['rep_password']:
                if self.db.create_user(data):
                    QMessageBox.information(self, 'Регистрации', \
                                        'Пользователь успешно зарегистрирован', \
                                        QMessageBox.Ok )
                    self.ui.close()
                    self.close()
            else:
                QMessageBox.warning(self, 'Ошибка регистрации', \
                                        'Пароли не совпали', \
                                        QMessageBox.Ok )
        else:
            QMessageBox.warning(self, 'Ошибка регистрации', \
                                    'Неправильно заполненные поля для регистрации', \
                                    QMessageBox.Ok)


class Contacts(QWidget):
    """Class to display all contacts and interaction with them"""
    def __init__(self, username):
        super().__init__()

        self.ui = ContactsUI()
        self.ui.fill_username(username)
        self.db = database()
        self.username = username
        self.display_tables()
        
        self.subbmit_data = {}
        self.connecter()

    def connecter(self):
        """All connections signal slot for this class"""
        self.ui.btnCreateUser.clicked.connect(self.add_contact_form)
        self.ui.birthday_tab.activated.connect(self.edit_contact_form)
        self.ui.BtnUsername.clicked.connect(self.login_redirect)
        
        for view in self.ui.tabs:
            view.activated.connect(self.edit_contact_form)

    def display_tables(self):
        """Displays all contacts"""
        result = self.db.get_all_contacts(self.db.get_id_by_username(self.username))
        if result:
            self.ui.fill_tables(result)
        else:
            self.ui.fill_tables([])
            QMessageBox.warning(self, 'Контактов нет',f'Контактов нет', \
                                QMessageBox.Ok )

    def delete_contact(self):
        """Deletes contact"""
        data = {
                'id': self.contact_id,
                'user_id': self.db.get_id_by_username(self.username)
            }

        self.db.delete_contact(data)
        self.ui_edit.close()
        self.display_tables()

    def edit_contact_form(self, index):
        """Edits data of contact in form"""
        self.ui_edit = ContactFormUI('Редактировать')
        self.contact_id = str(index.model().data[index.row()][0])
        data = {
            'secondname': str(index.model().data[index.row()][1]),
            'firstname': str(index.model().data[index.row()][2]),
            'phone': str(index.model().data[index.row()][3]),
            'year': str(index.model().data[index.row()][4][0]) + \
                    str(index.model().data[index.row()][4][1]) + \
                    str(index.model().data[index.row()][4][2]) + \
                    str(index.model().data[index.row()][4][3]),
            'month': str(index.model().data[index.row()][4][5]) + \
                     str(index.model().data[index.row()][4][6]),
            'day': str(index.model().data[index.row()][4][8]) + \
                   str(index.model().data[index.row()][4][9])
        }
        self.ui_edit.btnSubbmit.clicked.connect(self.edit_contact)
        self.ui_edit.btnDelete.clicked.connect(self.delete_contact)
        self.ui_edit.set_data_in_form(data)
    
    def edit_contact(self):
        """Edits contact"""
        self.subbmit_data = self.ui_edit.get_new_contact_data()
        if is_contact_valid(self.subbmit_data):
            self.subbmit_data['user_id'] = self.db.get_id_by_username(self.username)
            self.subbmit_data['id'] = self.contact_id
            if self.db.check_contact_repeats(self.subbmit_data) or self.db.check_contact_phone(self.subbmit_data, self.subbmit_data['user_id']):
                QMessageBox.warning(self, 'Ошибка редактирования контакта',f'Такой пользователь уже есть', \
                                    QMessageBox.Ok )
            else:
                self.db.update_contact(self.subbmit_data)
                self.ui_edit.close()
                QMessageBox.information(self, 'Пользователь изменен', \
                                    self.ui.check_letter_tab(self.subbmit_data['lastname']), \
                                    QMessageBox.Ok )
                self.display_tables()
        else:
            QMessageBox.warning(self, 'Ошибка редактирования контакта',f'Не правильные данные для редактирования', \
                                QMessageBox.Ok )

    def add_contact_form(self):
        """Add data of contact in form"""
        self.ui_add = ContactFormUI('Создать')
        self.ui_add.btnSubbmit.clicked.connect(self.add_contact)
    
    def add_contact(self):
        """Add new contact"""
        self.subbmit_data = self.ui_add.get_new_contact_data()
        if is_contact_valid(self.subbmit_data):
            self.subbmit_data['user_id'] = self.db.get_id_by_username(self.username)
            if self.db.check_contact_repeats(self.subbmit_data) or self.db.check_contact_phone(self.subbmit_data, None):
                QMessageBox.warning(self, 'Ошибка создания контакта',f'Такой пользователь уже есть', \
                                    QMessageBox.Ok )
            else:
                self.db.create_contact(self.subbmit_data)
                self.ui_add.close()
                QMessageBox.information(self, 'Новый пользователь добавлен', \
                                    self.ui.check_letter_tab(self.subbmit_data['lastname']), \
                                    QMessageBox.Ok )
                self.display_tables()
        else:
            QMessageBox.warning(self, 'Ошибка создания контакта',f'Не правильные данные для создания', \
                                QMessageBox.Ok )

    def login_redirect(self):
        self.ui.close()
        if not self.ui.isVisible():
            self.login_window = Login()
        self.close()
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    sys.exit(app.exec_())