from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class ReportGeneratorForm(FlaskForm):
    vip_input = FileField('VIP .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    oneportal_input = FileField('OnePortal .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    changelog_input = FileField('Changelog .csv file:',
                validators=[FileAllowed(['csv'], '.csv only!'), FileRequired()])
    # doh_target = IntegerField('DOH Target:',
    #                     validators=[DataRequired()],
    #                     default='25')
    submit = SubmitField('Upload File')
