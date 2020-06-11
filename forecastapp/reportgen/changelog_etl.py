from datetime import date, datetime
from forecastapp.reportgen import utils
import csv

def date_reformat_changelog(date):
    date_split = date.split("/")
    y = int(date_split[2])
    m = int(date_split[0])
    d = int(date_split[1])
    new_date = datetime.date(datetime(y, m, d))

    return new_date

def nearest(dates, truck):
    return min([i for i in dates[1:] if i < truck], key=lambda x: abs(x - truck))

def changelog_adjustments(changelog_list, date_list):
    ticket_counter = 0
    changelog_samedate = []
    changelog_diffdate = []

# split the change log list into changes that affect a single date and those that
# shift order date
    for ticket in changelog_list:
        chg_log_orig_date = ticket[0]
        chg_log_new_date = ticket[4]
# First if statement ensures no old tickets make it into changelog lists.
        if chg_log_new_date >= date_list[1]:
            ticket_counter += 1
            if chg_log_orig_date == chg_log_new_date:
                changelog_samedate.append(ticket)
            else:
                changelog_diffdate.append(ticket)

# The following for loops "round down" the ship weeks in cases where a date
# other than Monday was errantly typed into the change log
    for ticket in changelog_samedate:
        orig_ship_week = ticket[0]
        new_ship_week = ticket[4]
        if orig_ship_week not in date_list:
            ticket[0] = nearest(date_list, orig_ship_week)
        if new_ship_week not in date_list:
            ticket[4] = nearest(date_list, new_ship_week)

    return changelog_samedate, changelog_diffdate, ticket_counter

def changelog_clean(forecast_report):
    changelog_list = []
    date_list = forecast_report.date_list

    with open(forecast_report.changelog_path, 'r', newline = "") as input_file:
        changelog_reader = csv.reader(input_file, delimiter = ",")
        for row in changelog_reader:
            orig_week = date_reformat_changelog(row[1])
            try:
                wslr_id = int(row[2])
            except:
                wslr_id = int(''.join([i for i in row[2] if i.isdigit()]))
            wslr_id = utils.merge_wslr(wslr_id)
            pdcn = str(row[3]).upper()
            pdcn = utils.pdcn_cleanup(pdcn)
            orig_qty = int(row[4])
            new_qty = int(row[5])
            order_adjustment = new_qty - orig_qty
            new_week = date_reformat_changelog(row[6])
            changelog_list.append([
                    orig_week,
                    wslr_id,
                    pdcn,
                    order_adjustment,
                    new_week])
    changelog_samedate, changelog_diffdate, ticket_counter = \
        changelog_adjustments(changelog_list, date_list)

    return changelog_samedate, changelog_diffdate, ticket_counter
