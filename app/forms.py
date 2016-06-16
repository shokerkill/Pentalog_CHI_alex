from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class LoginForm(Form):
    login_name = StringField('login_name', validators=[DataRequired()])
