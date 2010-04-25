from wtforms import Form, BooleanField, TextField, PasswordField, validators

class CreateAccountForm(Form):
    username = TextField('username')
    password = PasswordField('password')
