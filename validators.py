from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


def is_contact_valid(data):
    """Validation of contact information from ui"""
    if len(data['firstname']) <= 0:
        return False
    elif len(data['lastname']) <= 0:
        return False
    elif len(data['phone']) <= 0:
        return False
    else:
        return True

def is_email_valid(email):
    """Validation of email information from ui"""
    if len(email) <= 5:
        return True
    elif '@' not in email or '.' not in email:
        return True
    elif email.count('@') > 1 or email.count('.') > 1:
        return True
    elif email[len(email)-1] == '.':
        return True
    else:
        return False

def is_user_valid(data):
    """Validation of user information from ui"""
    if len(data['username']) <= 0:
        return False
    elif len(data['password']) <= 0:
        return False
    elif is_email_valid(data['email']):
        return False
    else:
        return True
