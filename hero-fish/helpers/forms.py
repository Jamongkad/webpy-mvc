from wtforms import Form, BooleanField, TextField, PasswordField, SelectField, validators

class CreateAccountForm(Form):
    username = TextField('username', [validators.Required(message='you need a user name right?')])
    password = PasswordField('password', [validators.Required(message='you need a password right?')])

class ChooseOccup(Form):
    occupation = SelectField('occupation', choices=[('merchant', 'Merchant'), ('mercernary', 'Mercenary'), ('pwet', 'Martie')])
