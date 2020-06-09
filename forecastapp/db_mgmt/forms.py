from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from forecastapp.models import MergedPdcn

class PdcnMergeAdd(FlaskForm):
    pdcnMain = StringField('PDCN Main',
                           validators=[DataRequired(), Length(min=7, max=7)])
    pdcnAlt = StringField('PDCN Alternate',
                           validators=[DataRequired(), Length(min=7, max=7)])
    submit = SubmitField('Merge PDCN')

    def validate_pdcnAlt(self, pdcnAlt):
        alternate = MergedPdcn.query.filter_by(pdcnAlt=pdcnAlt.data).first()
        if alternate:
            raise ValidationError('That alternate PDCN already exists in the database.')
