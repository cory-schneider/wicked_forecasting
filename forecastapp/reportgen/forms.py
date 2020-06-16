from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, IntegerField,
                     BooleanField)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class ReportGeneratorForm(FlaskForm):
    vip_input = FileField('VIP .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    oneportal_input = FileField('OnePortal .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    changelog_input = FileField('Changelog .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    email_toggle = BooleanField('Write Email Templates', default="checked")
    submit = SubmitField('Upload File')
