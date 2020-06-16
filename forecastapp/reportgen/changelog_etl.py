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

def changelog_clean(advisor):
    changelog = []

    with open(advisor.changelog_path, 'r', newline = "") as input_file:
        changelog_reader = csv.reader(input_file, delimiter = ",")

        for row in changelog_reader:
            try:
                orig_week = date_reformat_changelog(row[1])
                new_week = date_reformat_changelog(row[6])
            except:
                row.append("Date malformed or missing.")
                advisor.malformed_tickets.append(row)
                continue
# Skip old tickets
            if new_week < advisor.date_list[1]:
                continue
# Add malformed tickets to a list for review
            if orig_week != new_week:
                row.append("Dates don't match.")
                advisor.malformed_tickets.append(row)
            else:
# Begin forming the changelog
                orig_week = utils.prev_monday(orig_week)
                new_week = utils.prev_monday(new_week)
# Strips non-digit characters from wslr_id, which has popped up for some reason.
                wslr_id = int(''.join([i for i in row[2] if i.isdigit()]))
                wslr_id = utils.merge_wslr(wslr_id)
                pdcn = str(row[3]).upper()
                pdcn = utils.pdcn_cleanup(pdcn)
                orig_qty = int(row[4])
                new_qty = int(row[5])
                order_adjustment = new_qty - orig_qty
                advisor.tickets += 1

                changelog.append([
                        orig_week,
                        wslr_id,
                        pdcn,
                        order_adjustment,
                        new_week])

    return changelog

# Deprecated
# def nearest(dates, truck):
#     return min([i for i in dates[1:] if i < truck], key=lambda x: abs(x - truck))
