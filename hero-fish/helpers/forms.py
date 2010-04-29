from wtforms import Form, BooleanField, TextField, PasswordField, validators

class CreateAccountForm(Form):
    username = TextField('username', [validators.Required(message='you need a user name right?')])
    password = PasswordField('password', [validators.Required(message='you need a password right?')])
