from datetime import datetime, date as dt
from dateutil.relativedelta import relativedelta, FR
from flask_login import current_user
from forecastapp.reportgen.utils import save_csv
import secrets
import os
from flask import current_app


def temp_folder():
    random_hex = secrets.token_hex(8)
    folder_path = os.path.join(current_app.root_path, 'temp/', random_hex)
    os.mkdir(folder_path)

    return folder_path

class ForecastHelper():
    def __init__(self, form):
        self.file_list = []
        self.temp_report_path = temp_folder()
        self.vip_path = save_csv(form.vip_input.data)
        self.oneportal_path = save_csv(form.oneportal_input.data)
        self.date_list = []
        self.changelog_path = save_csv(form.changelog_input.data)
        self.file_list = [self.vip_path,
                          self.oneportal_path,
                          self.changelog_path]
        self.today = dt.today()
        self.last_friday = datetime.date(datetime(2020, 6, 5))
        # self.last_friday = self.today + relativedelta(weekday=FR(-1))
        self.user = current_user.email
        self.submission_time = datetime.now()
        self.complete = 0
        self.tickets = 0

    def __repr__(self):
        return f"Report ('User: {self.user}', 'Time: {self.submission_time}', \
'Tickets: {self.tickets}', 'Completed: {self.complete}')"
