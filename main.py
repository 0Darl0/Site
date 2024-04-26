from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, LoginForm, Letter, Back_or_Write, Index
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User
from random import randint
from data.letters import Letters

from data.letters import Letters
from forms.user import RegisterForm, LoginForm, Letter, Back_or_Write, SettingForm
# from tg_bot import notification

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

with open('app_key.txt', mode='r') as f_in:
    app.config['SECRET_KEY'] = f_in.read()


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Index()
    le = ''
    if form.validate_on_submit():
        return redirect('/letter')
    db_sess = db_session.create_session()
    try:
        if db_sess.query(User).filter(Letters.who_id == int(str(current_user).split(' ')[0])).first():
            le = db_sess.query(User).filter(Letters.who_id == int(str(current_user).split(' ')[0]))
            print(le)
    except ValueError:
        print(db_sess.query(User).filter(Letters.who_id == int(str(current_user).split(' ')[0])))
    return render_template('index.html', title='Главная', form=form, letter=le)


@app.route('/letter', methods=['GET', 'POST'])
def letter():
    form = Letter()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.who.data).first():
            print(db_sess.query(User).filter(User.email == form.who.data).first().email)
            user = db_sess.query(User).filter(User.id == int(str(current_user).split(' ')[0])).first()
            lett = Letters(
                id=randint(1, 10**10),
                user_id=user.id,
                who_id=db_sess.query(User).filter(User.email == form.who.data).first().id,
                topic=form.theme.data,
                content=form.message.data
            )
            db_sess.add(lett)
            db_sess.commit()
            return redirect('/succes')
        else:
            return render_template('letter.html', title='Письмо', form=form,
                                   message='Проверьте корректность ввода электронной почты')
    return render_template('letter.html', title='Письмо', form=form)


@app.route('/succes', methods=['GET', 'POST'])
def succes():
    form = Back_or_Write()
    if form.validate_on_submit():
        if form.back.data:
            return redirect('/')
        elif form.write.data:
            return redirect('/letter')
    return render_template('succses.html', title='Успешно', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(str(current_user).split(' ')[0])).first()
        if form.surname.data != '':
            if user:
                user.surname = form.surname.data
                db_sess.commit()
        if form.name.data != '':
            if user:
                user.name = form.name.data
                db_sess.commit()
        if form.tg_id.data != '':
            check = (db_sess.query(User).filter(User.tg_nickname == form.tg_id).first)
            print(check.tg_id)
            if user:
                user.tg_nickname = form.tg_id.data
                db_sess.commit()
        db_sess.commit()
        return redirect('/')
    return render_template('settings.html', title='Настройки', form=form)


if __name__ == '__main__':
    main()
