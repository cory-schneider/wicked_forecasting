from datetime import datetime, date as dt
from dateutil.relativedelta import relativedelta, FR

class ForecastHelper():
    def __init__(self, vip_path, oneportal_path, changelog_path):
        self.vip_file = vip_path
        self.oneportal_file = oneportal_path
        self.changelog_file = changelog_path
        self.today = dt.today()
        self.last_friday = self.today + relativedelta(weekday=FR(-1))

    def __repr__(self):
        return f"Helper Instance('{self.vip_file}', '{self.oneportal_file}', '{self.changelog_file}')"
