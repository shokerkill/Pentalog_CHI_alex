from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import LoginForm
from .models import User, Advice
import json, requests

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = form.login_name.data
        user = User.query.filter(User.nickname == user).first()
        if user:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        flash('No such user in system')
    return render_template('login.html', form=form)

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/advice/<advice_type>')
@login_required
def advice(advice_type):
    advice_url = 'http://fucking-great-advice.ru/api/'
    if advice_type == 'censored':
       advice_type = 'random/censored'
    resp = requests.get(url=advice_url+advice_type, params={})
    data = json.loads(resp.text)
    if not isinstance(data, list):
        data = [data]
    return render_template('advice.html', advices=data, read=False)

@app.route('/store_advice', methods=['GET', 'POST'])
@login_required
def advice_store():
    advice = Advice.query.filter(Advice.foreign_id == int(request.args['foreign_id[]'])).first()
    if advice:
        advice.victims.add(current_user)
    else:
        advice = Advice(text=request.args['advice[]'], foreign_id=int(request.args['foreign_id[]']), victims=[current_user])
    db.session.add(advice)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/self_advices')
@login_required
def self_advices():
    advices = current_user.advices
    return render_template('advice.html', advices=advices, read=True)
