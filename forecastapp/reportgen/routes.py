from flask import render_template, request, Blueprint
from forecastapp.reportgen.forms import ReportGeneratorForm

reportgen = Blueprint('reportgen', __name__)

@reportgen.route("/report_generator")
def report_generator():
    form = ReportGeneratorForm()
    return render_template('report_generator.html', title='Forecast Helper Report Generator',
    form=form, legend='Forecast Helper Report Generator')
