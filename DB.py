import os
from socket import create_connection
from PyQt5.QtWidgets import QMessageBox, QWidget
import mariadb

class DB:
    """Class for all database connections and data"""
    def __init__(self):
        self.createDB()

    def createConnection(self):
        """Creates connection for DB"""
        try:
            connection = mariadb.connect(
                user='root',
                password='admin',
                host='localhost',
                port=3306,
                database='contactApp'
            )
        except mariadb.Error as e:
            raise Exception(f"Unable to connect to the database: {e}")

        return connection

    def createTable(self, request):
        """Creates table for DB"""

        connection = self.createConnection()
        cursor = connection.cursor() 

        try:
            cursor.execute(request)
        except mariadb.Error as e:
            raise Exception(f"Error creating tables: {e}")

        connection.close()

    def createDB(self):
        """Creates database"""

        try:
            connection = mariadb.connect(
                user='root',
                password='admin',
                host='localhost',
                port=3306
            )
        except mariadb.Error as e:
            raise Exception(f"Unable to connect to the database: {e}")

        cursor = connection.cursor()
        request = f'CREATE DATABASE IF NOT EXISTS contactApp'
        cursor.execute(request)

        # Creating table users for database
        users_table = f"CREATE TABLE IF NOT EXISTS users(" \
                  f"id int unique primary key not null AUTO_INCREMENT," \
                  f"username varchar(50) unique not null," \
                  f"password varchar(50) not null," \
                  f"email varchar(50) unique not null," \
                  f"birthday varchar(10) not null" \
                  f")CHARACTER SET = 'UTF8';"
        self.createTable(users_table)

        # Creating table contacts for database
        contacts_table = f"CREATE TABLE IF NOT EXISTS contacts(" \
                  f"id int unique primary key not null AUTO_INCREMENT," \
                  f"firstname varchar(20) not null," \
                  f"lastname varchar(20) not null," \
                  f"phone varchar(15) unique not null," \
                  f"birthday varchar(10) not null," \
                  f"user_id int not null," \
                  f"CONSTRAINT fk_user_contact" \
                  f"    FOREIGN KEY (user_id) REFERENCES users (id)" \
                  f"    ON DELETE CASCADE " \
                  f"    ON UPDATE RESTRICT " \
                  f")" \
                  f"CHARACTER SET = 'UTF8';"
        self.createTable(contacts_table)

        connection.close()

    def create_user(self, data):
        """Creates user in database"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"insert into users (username, password, email, birthday) values " \
                  f"('{data['username']}', '{data['password']}'," \
                  f"'{data['email']}', '{data['date']}')"
        try:
            cursor.execute(request)
        except mariadb.IntegrityError:
            
            QMessageBox.warning(QWidget(), 'Ошибка регистрации', \
                                        'Такой пользователя уже есть в базе', \
                                        QMessageBox.Ok )
            connection.close()
            return False
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка регистрации',f'Ошибка сервера: {e}', \
                                        QMessageBox.Ok )
            connection.close()
            return False
                
        connection.commit()
        connection.close()
        return True

    def delete_contact(self, data):
        """Deletes contact from database"""
        connection = self.createConnection()
        cursor = connection.cursor()

        if data:
            request = f"delete from contacts where user_id={data['user_id']} and id={data['id']}"
            try:
                cursor.execute(request)
            except mariadb.Error as e:
                raise Exception(f"Error creating tables: {e}")
        else:
            raise Exception(f"Error this data for deleting")

        connection.commit()
        connection.close()
    
    def create_contact(self, data):
        """Creates contact in database"""
        connection = self.createConnection()
        cursor = connection.cursor()

        if data:
            request = f"insert into contacts (firstname, lastname, phone, birthday, user_id) values" \
                      f"( '{data['firstname']}', '{data['lastname']}', '{data['phone']}', '{data['birthday']}', '{data['user_id']}')"
            try:
                cursor.execute(request)
            except mariadb.Error as e:
                raise Exception(f"Error creating tables: {e}")
        else:
            raise Exception(f"Error this data for creating")

        connection.commit()
        connection.close()
    
    def update_contact(self, data):
        """Updates contact in database"""
        connection = self.createConnection()
        cursor = connection.cursor()

        if data:
            request = f"update contacts set firstname = '{data['firstname']}', lastname = '{data['lastname']}', phone = '{data['phone']}', birthday = '{data['birthday']}', user_id = '{data['user_id']}' where id='{data['id']}'"
            try:
                cursor.execute(request)
            except mariadb.Error as e:
                raise Exception(f"Error creating tables: {e}")
        else:
            raise Exception(f"Error this data for creating")

        connection.commit()
        connection.close()

    def get_all_contacts(self, user):
        """Displays all contacts"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f" select id, lastname, firstname, phone, birthday from contacts where user_id = '{user}'" \
                  f" order by contacts.lastname"

        try:
            cursor.execute(request)
            result = cursor.fetchall()
            connection.close()
            return result
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка базы данных', f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
            connection.close()

    def get_id_by_username(self, username):
        """Get user id by username from database"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select id from users where username='{username}'"
        try:
            cursor.execute(request)
            user_id = cursor.fetchall()
            connection.close()
            return user_id[0][0]
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка поиска пользователя', \
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
            connection.close()


    def check_contact_repeats(self, data):
        """Checks is there all similar contact"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select * from contacts where firstname = '{data['firstname']}' and lastname = '{data['lastname']}' and phone = '{data['phone']}' and birthday = '{data['birthday']}' and user_id = '{data['user_id']}'"
        try:
            cursor.execute(request)
            return cursor.fetchall()
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка проверки контакта в базе данных', \
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
            connection.close()

    def check_contact_phone(self, data, user_id):
        """Checks is there all contact with similar phone"""
        connection = self.createConnection()
        cursor = connection.cursor()
        if user_id:
            request = f"select * from contacts where phone = '{data['phone']}' and id != {user_id}"
        else:
            request = f"select * from contacts where phone = '{data['phone']}'"
        try:
            cursor.execute(request)
            return cursor.fetchall()
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка проверки контакта в базе данных', \
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
        connection.close()

    def check_user_repeats(self, data):
        """Checks is there user with similar username"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select * from users where username = '{data['username']}'"
        try:
            cursor.execute(request)
            result = cursor.fetchall()
            connection.close()
            return result
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка проверки пользователя в базе данных', \
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
            connection.close()

    def get_password(self, user):
        """Gets password from database"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select password from users where username='{user}'"
        try:
            cursor.execute(request)
            result = cursor.fetchall()
            connection.close()
            return result
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка получения пароля из базы данных',\
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
            connection.close()
    
    def check_user_email(self, email):
        """Checks if user with such email is in database"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select id from users where email ='{email}'"
        try:
            cursor.execute(request)
            result = cursor.fetchall()
            connection.close()
            return result
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка восстановления пароля',\
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
        connection.close()

    def get_contact(self, user_id):
        """Checks if user with such email is in database"""
        connection = self.createConnection()
        cursor = connection.cursor()
        request = f"select username, password from users where id ='{user_id}'"
        try:
            cursor.execute(request)
            result = cursor.fetchall()
            connection.close()
            return result
        except mariadb.Error as e:
            QMessageBox.warning(QWidget(), 'Ошибка восстановления пароля',\
                                f'Ошибка сервера: {e}', \
                                QMessageBox.Ok )
        connection.close()

