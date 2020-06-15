from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from forecastapp.db_mgmt.models import MergedPdcn

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

class RemovePdcnPair(FlaskForm):
    removeCheck = BooleanField('Remove')
    submit = SubmitField('Remove PDCN Pairs')

# https://wtforms.readthedocs.io/en/latest/specific_problems/
# Dynamic Form Composition -- uh actually maybe not
# https://stackoverflow.com/questions/31859903/get-the-value-of-a-checkbox-in-flask
