from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.reportgen.forms import ReportGeneratorForm
from datetime import datetime, date as dt
from forecastapp.reportgen.utils import save_csv
import os
import csv

reportgen = Blueprint('reportgen', __name__)

@reportgen.route("/report_generator", methods=['GET', 'POST'])
@login_required
def report_generator():
    form = ReportGeneratorForm()
    if form.validate_on_submit():
        today = dt.today()
        vip_csv = save_csv(form.vip_input.data)
        oneportal_csv = save_csv(form.oneportal_input.data)
        changelog_csv = save_csv(form.changelog_input.data)
        with open(vip_csv, "r", newline = "") as input_file:
            reader = csv.reader(input_file)
            data_ready = []
            for row in reader:
                data_ready.append(row)

        temp_files = [vip_csv, oneportal_csv, changelog_csv]
        for file in temp_files:
            os.remove(file)

        return render_template('testgen.html',
                                testing=data_ready)

    return render_template('report_generator.html', title='Forecast Helper Report Generator',
    form=form, legend='Forecast Helper Report Generator')
