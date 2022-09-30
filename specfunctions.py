import smtplib


def send_password_email(email, data):
    """Sends email with username and password"""

    """Закоментированный пример отправки письма"""
    # message = f"Ваш логин и пароль для восстановления: \n LOGIN: {data['username']}" \
    #           f"PASSWORD: {data['password']}"

    # body = "\r\n".join((
    #     "From: %s" % from@gmail.com,
    #     "To: %s" % email,
    #     "Subject: %s" % 'New Password',
    #     "",
    #     message
    # ))

    # server = smtplib.SMTP(host='smtp.gmail.com', port=25)
    # server.login(from@gmail.com, passExample123)
    # server.sendmail(from@gmail.com, [email], body)
    # server.quit()
    # return True
    return False