from flask import (render_template, request, Blueprint, send_file, current_app)
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.reportgen.forms import ReportGeneratorForm
from datetime import datetime, date as dt
from dateutil.relativedelta import relativedelta, FR
from forecastapp.reportgen.utils import save_csv, save_input_report
from forecastapp.reportgen.models import ForecastHelper
from forecastapp.reportgen.vip_etl import vip_clean
from forecastapp.reportgen.oneportal_etl import oneportal_clean
from forecastapp.reportgen.changelog_etl import changelog_clean
import os
import csv
import logging

testing=1

reportgen = Blueprint('reportgen', __name__)

@reportgen.route("/report_generator", methods=['GET', 'POST'])
@login_required
def report_generator():
    form = ReportGeneratorForm()
    if form.validate_on_submit():
        vip_path = save_csv(form.vip_input.data)
        oneportal_path = save_csv(form.oneportal_input.data)
        changelog_path = save_csv(form.changelog_input.data)

        forecast_report = ForecastHelper(vip_path, oneportal_path, changelog_path)
        
        vip_cleaned_list = vip_clean(forecast_report)
        oneportal_cleaned_list = oneportal_clean(forecast_report)
        changelog_cleaned_list, changelog_problems, ticket_count = \
            changelog_clean(forecast_report)

        print(f"THIS IS THE TICKET COUNT {ticket_count}")

        output_fn = os.path.join(current_app.root_path, 'temp', "vip_out.csv")
        save_input_report(oneportal_cleaned_list, output_fn)

        temp_files = [vip_path, oneportal_path, changelog_path]
        for file in temp_files:
            os.remove(file)
# Marks the report creation process as complete.
        forecast_report.complete = 1
        logging.info('User ran a report which completed successfully: ' + str(forecast_report))
        # return send_file(vip_fn,
        #                 mimetype="text/csv",
        #                 attachment_filename='vip_out.csv',
        #                 as_attachment=True)
        return render_template('testgen.html',
                        testing=changelog_problems, output_fn=output_fn)

    return render_template('report_generator.html', title='Forecast Helper Report Generator',
    form=form, legend='Forecast Helper Report Generator')

@reportgen.route('/send_csv') # this is a job for GET, not POST
@login_required
def send_csv():
    output_fn = request.args.get('output_fn', None)
    return send_file(output_fn,
                     mimetype='text/csv',
                     attachment_filename='vip_out.csv',
                     as_attachment=True)
