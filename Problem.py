from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, Form, PasswordField,DateField
from wtforms import validators, ValidationError


class RForm(Form):


    problem = StringField('Problems', [validators.DataRequired('Please enter problem')])

    description = StringField('Description of Problem', [validators.DataRequired('Please type description of incident')])

    location = StringField('Location of Problem', [validators.DataRequired('Please type location of incident')])

    date = StringField('Date of Problem', [validators.DataRequired('Please enter date of incident')])

    comments =  StringField('Comments ', [validators.DataRequired('Please enter comments of incident')])

    name      = StringField('Enter name', [validators.DataRequired('Please enter Name')])

    submit = SubmitField('Submit')


