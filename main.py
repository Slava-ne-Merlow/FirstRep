from flask import Flask, render_template, redirect, request, abort
from sqlalchemy.orm import Session
from data import db_session
from data.orders import Orders
from data.users import User
from data.formarders import Forwarders
from forms.user import RegisterForm, LoginForm
from forms.order import OrderForm
from forms.mailing import MailForm
from forms.forwarder import ForwarderForm
from getMesseges import answers_by_subject
import smtplib
from email.mime.text import MIMEText
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import base64
import email
import imaplib
import quopri
from email.header import decode_header


#osteccorporation@gmail.com
# pnor qdfq ncdc egnu
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    db_sess: Session = db_session.create_session()()

    if current_user.is_authenticated and current_user.user_type == 'Мэнеджер':
        news = db_sess.query(Orders).filter(Orders.user == current_user)
    else:
        news = db_sess.query(Orders)
    return render_template("index.html", news=news)

@app.route('/orders',  methods=['GET', 'POST'])
@login_required
def add_order():
    form = OrderForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()()
        if db_sess.query(Orders).filter(Orders.invoice_numbers == form.invoice_numbers.data).first():
            return render_template('orders.html', title='Добавление заказа',
                                   form=form,
                                   message="Заказ с таким номером уже есть")
        order = Orders()
        order.start_address = form.start_address.data
        order.end_address = form.end_address.data
        order.quantity = form.quantity.data
        order.dimensions = form.dimensions.data
        order.invoice_numbers = form.invoice_numbers.data
        order.weight = form.weight.data
        order.content = form.content.data
        current_user.orders.append(order)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('orders.html', title='Добавление заказа',
                           form=form)



@app.route('/register', methods=['GET', 'POST'])
def reqister():

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.user_type.data == 'Админ' and form.code.data != 'BedniBarn777':
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверный код доступа")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.user_type = form.user_type.data


        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/orders/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_orders(order_id):
    form = OrderForm()
    if request.method == "GET":
        db_sess = db_session.create_session()()
        news = db_sess.query(Orders).filter(Orders.id == order_id,
                                          Orders.user == current_user
                                          ).first()
        if news:


            form.invoice_numbers.data = news.invoice_numbers
            form.content.data = news.content
            form.start_address.data = news.start_address
            form.end_address.data = news.end_address
            form.weight.data = news.weight
            form.quantity.data = news.quantity
            form.dimensions.data = news.dimensions

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()()
        news = db_sess.query(Orders).filter(Orders.id == order_id,
                                          Orders.user == current_user
                                          ).first()
        if news:

            news.invoice_numbers = form.invoice_numbers.data
            news.content = form.content.data
            news.start_address = form.start_address.data
            news.end_address = form.end_address.data
            news.weight = form.weight.data
            news.quantityd = form.quantity.data
            news.dimensions = form.dimensions.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('orders.html',
                           title='Редактирование заказа',
                           form=form
                           )

@app.route('/orders_delete/<int:order_id>', methods=['GET', 'POST'])
@login_required
def orders_delete(order_id):
    db_sess = db_session.create_session()()
    news = db_sess.query(Orders).filter(Orders.id == order_id,
                                      Orders.user == current_user
                                      ).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/answer_print/<int:order_id>', methods=['GET', 'POST'])
@login_required
def answer_print(order_id):
    db_sess = db_session.create_session()()
    order: Orders = db_sess.query(Orders).filter(Orders.id == order_id
                                      ).first()
    file_rus = open('templates/Messege template russ.txt').readline().replace('theme_', order.invoice_numbers).strip()
    file_eng = open('templates/Messege template eng.txt').readline().replace('theme_', order.invoice_numbers).strip()
    incoming = answers_by_subject(file_rus,  'INBOX')
    incoming.extend(answers_by_subject(file_eng, 'INBOX'))
    sented = answers_by_subject(file_rus,  'OUTBOX')
    sented.extend(answers_by_subject(file_eng, 'OUTBOX'))
    dudes = set()
    for i in incoming:
        dudes.add(i["From"])

    perepiski = {}
    for _ in dudes:
        perepiski[_] = []


    for i in dudes:
        for j in incoming:
            if i == j["From"]:
                perepiski[i].append(j)

        for m in sented:
            if i == m["To"]:
                perepiski[i].append(m)


    for y in perepiski.keys():
        perepiski[y] = sorted(perepiski[y], key=lambda x: x['Date'])
    return render_template('answers_view.html',
                           title='Редактирование заказа',
                           news=perepiski)

@app.route('/forwarders_view')
@login_required
def forwarders_view():
    db_sess = db_session.create_session()()
    forwarders = db_sess.query(Forwarders)
    dic = {}
    f_set = set()
    for i in forwarders:
        f_set.add(i.company)
    for i in f_set:
        dic[i] = []
    for i in forwarders:
        dic[i.company].append(i)

    return render_template('forwarders_view.html',
                           title='Редактирование заказа',
                           dic=dic, str=str)

@app.route('/forwarders',  methods=['GET', 'POST'])
@login_required
def add_forwarder():
    form = ForwarderForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()()
        if db_sess.query(Forwarders).filter(Forwarders.email == form.email.data).first():
            return render_template('forwarders.html', title='Добавление новости',
                                   form=form,
                                   message="Перевозчик с таким адресом уже есть")
        forwarder = Forwarders()

        forwarder.name = form.name.data
        forwarder.company = form.company.data
        forwarder.email = form.email.data

        db_sess.add(forwarder)
        db_sess.commit()
        return redirect('/forwarders_view')
    return render_template('forwarders.html', title='Добавление новости',
                           form=form)


@app.route('/mailing/<int:order_id>/<lang>', methods=['GET', 'POST'])
@login_required
def mailing(order_id, lang):
    db_sess = db_session.create_session()()
    forwarders = db_sess.query(Forwarders)
    available_theme = True
    form = MailForm()
    form.choices.query = forwarders
    if request.method == "GET":
        db_sess = db_session.create_session()()
        order = db_sess.query(Orders).filter(Orders.id == order_id,
                                          Orders.user == current_user
                                          ).first()
        if order:
            with open(f'templates/Messege template {lang}.txt', 'r') as template:

                theme, text = template.read().split('\n\n')
                form.mail_theme.data = theme.replace('theme_', order.invoice_numbers)
                text = text.replace('start_address', order.start_address)
                text = text.replace('end_address', order.end_address)
                text = text.replace('weight_', str(order.weight))
                text = text.replace('dimensions_', str(order.dimensions))
                text = text.replace('quantity_', str(order.quantity))
                text = text.replace('content_', order.content)
                form.mail_text.data = text



    if form.validate_on_submit():
        db_sess = db_session.create_session()()
        news = db_sess.query(Orders).filter(Orders.id == order_id,
                                          Orders.user == current_user
                                          ).first()
        if news:
            mails: list = form.choices.data
            mails.append(current_user)


            sender = "osteccorporation@gmail.com"
            password = "pnor qdfq ncdc egnu"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)

            msg = MIMEText(form.mail_text.data)
            msg["Subject"] = form.mail_theme.data
            mails: list = form.choices.data

            for i in mails:
                server.sendmail(sender, i.email, msg.as_string())
            db_sess.commit()
            return redirect('/')


    return render_template('mailing.html',
                           title='Редактирование заказа',
                           form=form, lang=lang, available_theme=available_theme, order_id=order_id)


@app.route('/mailing2/<message_id>/<folder>', methods=['GET', 'POST'])
@login_required
def mailing2(message_id, folder):
    folder = folder.replace('slash', '/')
    form = MailForm()
    form.choices.query = []
    available_theme = False
    if request.method == "GET":
        FROM_EMAIL = "osteccorporation@gmail.com"
        FROM_PWD = "pnor qdfq ncdc egnu"
        SMTP_SERVER = "imap.gmail.com"

        imap = imaplib.IMAP4_SSL(SMTP_SERVER)

        imap.login(FROM_EMAIL, FROM_PWD)

        imap.select(folder)

        typ, data = imap.search(None, 'ALL')

        data = data[0].split()

        ind = data[list(map(str, data)).index(message_id)]
        status, msg = imap.fetch(ind, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])

        mail = msg['From'].split()[-1].replace('<', '').replace('>', '')
        subj = quopri.decodestring(decode_header(msg["Subject"])[0][0]).decode('UTF-8')


        form.mail_theme.data = subj
        # form.mail_theme.render_kw = {'disabled': 'disabled'}

    if request.method == "POST":
        print('xpmzm')
        sender = "osteccorporation@gmail.com"
        password = "pnor qdfq ncdc egnu"
        SMTP_SERVER = "imap.gmail.com"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        msg = MIMEText(form.mail_text.data)
        msg["Subject"] = form.mail_theme.data
        msg['In-Reply-To'] = message_id
        msg['References'] = message_id

        imap = imaplib.IMAP4_SSL(SMTP_SERVER)
        imap.login(sender, password)
        imap.select(folder)
        typ, data = imap.search(None, 'ALL')
        data = data[0].split()
        ind = data[list(map(str, data)).index(message_id)]
        status, msg2 = imap.fetch(ind, '(RFC822)')
        msg2 = email.message_from_bytes(msg2[0][1])
        if folder == 'INBOX':
            mail = msg2['From']
        elif folder == '[Gmail]/&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-':
            if not msg2['Received']:
                a = msg2['To']
                if a.find('<') != -1:
                    mail = a[a.find('<') + 1:a.find('>') ]
                else:
                    mail = a
            else:
                a = str(msg2['Received']).split('\r\n')[2]
                if a.find('<') != -1:
                    mail =a[a.find('<') + 1:a.find('>') ]
                else:
                    mail = a
        print(mail)
        server.sendmail(sender, mail, msg.as_string())


        return redirect('/')
    print(request.method == "POST")
    print(form.validate_on_submit())
    return render_template('mailing.html',
                           title='Редактирование заказа',
                           form=form, available_theme=available_theme)

def main():
    db_session.global_init("db/blogs.db")
    # db_sess: Session = db_session.create_session()()
    app.run(port=8000)


if __name__ == '__main__':
    main()
