from flask import (render_template, request, Blueprint, send_file, current_app)
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.reportgen.forms import ReportGeneratorForm
import datetime
from dateutil.relativedelta import relativedelta, FR
from forecastapp.reportgen.utils import save_csv
from forecastapp.reportgen.models import ForecastHelper
from forecastapp.reportgen.vip_etl import vip_clean
from forecastapp.reportgen.oneportal_etl import oneportal_clean
from forecastapp.reportgen.changelog_etl import changelog_clean
from forecastapp.reportgen.merge_reports import merged_units
from forecastapp.reportgen.email_writer import email_writer
from forecastapp.reportgen.excel_writer import excel_writer
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
# Creating a class instance
        advisor = ForecastHelper(form)
# Data cleaning
        vip_cleaned_list = vip_clean(advisor)
        oneportal_cleaned_list = oneportal_clean(advisor)
        changelog_clean(advisor)
# Report merging
        inventory_and_orders_units = \
            merged_units(vip_cleaned_list, oneportal_cleaned_list, advisor)
        output_fn = excel_writer(inventory_and_orders_units, \
             advisor)
        advisor.output_fn = output_fn
        if form.email_toggle.data == True:
            email_writer(inventory_and_orders_units, advisor)
# Removing temp files
        temp_files = [advisor.vip_path, advisor.oneportal_path, advisor.changelog_path]
        for file in temp_files:
            os.remove(file)
        for i in advisor.file_list:
            print(i)
# Marking the report creation process as complete for logging.
        advisor.complete = 1
        print(f"Ticket Count: {advisor.tickets}")
        logging.info('User ran a report which completed successfully: ' + str(advisor))

        return render_template('return_report.html',
                               output_fn=output_fn,
                               advisor=advisor,
                               legend="Report Generated!")

    return render_template('report_generator.html', title='Forecast Report Generator',
    form=form, legend='Forecast Report Generator')

@reportgen.route('/send_xlsx')
@login_required
def send_xlsx():
    output_fn = request.args.get('output_fn', None)
    today = datetime.date.today()
    attachment_filename = str(today) + "-ForecastWorksheet.xlsx"
    return send_file(output_fn,
                     # mimetype='text/csv',
                     attachment_filename=attachment_filename,
                     as_attachment=True)
