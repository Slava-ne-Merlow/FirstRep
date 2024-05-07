import smtplib
from email.mime.text import MIMEText
lis = ['Todavia@rambler.ru', 'zhikhareva.a@ostec-group.ru', 'SlavaKushch@yandex.ru']

def send_email(message):
    sender = "slava.kush39@gmail.com"
    password = "iqpk evew sdkm zxml"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Текст на русском 1234 english too"
        for i in lis:

            server.sendmail(sender, i, msg.as_string())


        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    message = input("Type your message: ")
    print(send_email(message=message))


if __name__ == "__main__":
    main()