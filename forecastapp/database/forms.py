from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from forecastapp.database.models import PdcnPair, WholesalerFamily

class PdcnMergeAdd(FlaskForm):
    pdcnMain = StringField('PDCN Main',
                           validators=[DataRequired(), Length(min=7, max=7)])
    pdcnAlt = StringField('PDCN Alternate',
                           validators=[DataRequired(), Length(min=7, max=7)])
    submit = SubmitField('Merge PDCN')

    def validate_pdcnAlt(self, pdcnAlt):
        alternate = PdcnPair.query.filter_by(pdcnAlt=pdcnAlt.data).first()
        if alternate:
            raise ValidationError('That alternate PDCN already exists in the database.')

class RemovePdcnPair(FlaskForm):
    removeCheck = BooleanField('Remove')
    submit = SubmitField('Remove PDCN Pairs')

class WslrFamAdd(FlaskForm):
    name = StringField('WSLR Family Name',
                           validators=[DataRequired(), Length(min=7, max=25)])
    nums = StringField('WSLR List (separate with space)',
                           validators=[DataRequired(), Length(min=0, max=50)])
    submit = SubmitField('Create WSLR Family')

    def validate_wslrFam(self, nums):
        alternate = WholesalerFamily.query.filter_by(nums=nums.data).first()
        if alternate:
            raise ValidationError('That alternate PDCN already exists in the database.')

class WslrFamRemove(FlaskForm):
    removeCheck = BooleanField('Remove')
    submit = SubmitField('Remove WSLR Fam')
