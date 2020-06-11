from datetime import datetime, date as dt
from dateutil.relativedelta import relativedelta, FR
from flask_login import current_user

class ForecastHelper():
    def __init__(self, vip_path, oneportal_path, changelog_path):
        self.vip_file = vip_path
        self.oneportal_file = oneportal_path
        self.changelog_file = changelog_path
        self.today = dt.today()
        self.last_friday = self.today + relativedelta(weekday=FR(-1))
        self.user = current_user.email
        self.submission_time = datetime.now()
        self.complete = 0

    def __repr__(self):
        return f"Report Instance('{self.user}', '{self.submission_time}' \
'{self.complete}')"
