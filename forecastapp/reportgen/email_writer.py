from forecastapp.reportgen import utils
import datetime as dt
import os
from flask import (current_app)

def email_writer(report_units, advisor):

    end_date = advisor.date_list[-1]

    opener = f"I’ve attached our weekly order tracker highlighting our \
suggested tickets and orders through shipping week of {end_date}. The \
attachment details projected days on hand by week based on your orders, \
and our suggested adjustments have been highlighted in red for cuts and \
green for adds for your convenience. \
These suggestions are made to bring your on-hand inventory closer \
to the ideal amount providing our targeted days on hand."

    closer = "Please let me know if you have any questions regarding these \
suggestions. Also, I’d appreciate hearing back if you approve of and will \
place tickets or orders based on these suggestions. \n \n\
Thanks for your business!"

    wslr_list = []
    # Creates list of unique wholesalers
    for i in report_units[2:]:
        wslr_id_num = str(i[2])
        wslr_list.append(wslr_id_num)
    wslr_list = utils.unique(wslr_list)

    wslr_id_and_name = []
    for i in wslr_list:
        new_wslr = []
        new_wslr.append(i)
        for r in report_units[2:]:
            wslr_id_num = str(r[2])
            if i == wslr_id_num:
                wslr_name = str(r[1])
                new_wslr.append(wslr_name)
                break
        wslr_id_and_name.append(new_wslr)

# Runs through days on hand report to write emails for each wholesaler in list
    today_date = str(dt.date.today())
    for w in wslr_id_and_name:
        email = []
        email.append(f"Greetings {w[1]} team,")
        email.append("")
        email.append(opener)
        email.append("")
        item_list = []
        for r in report_units:
            if str(r[2]) == w[0]:
                name_and_pdcn = utils.pdcn_plus_product_name(r[3])
                new_item = name_and_pdcn + " - "
                item_list.append(new_item)
        email.append("Tickets Requested:")
        for d in advisor.date_list[2:5]:
            email.append(str(d) + ":")
            for i in item_list:
                email.append(i)
            email.append("")
        email.append("")
        email.append("Orders Requested:")
        for d in advisor.date_list[5:]:
            email.append(str(d) + ":")
            for i in item_list:
                email.append(i)
            email.append("")
        email.append(closer)

        wslr_stripped = w[1].replace(" ", "").lower() + w[0].replace(", ", "")

        output_filename = str(today_date + wslr_stripped + ".txt")
        dest_path = advisor.temp_report_path + "/" + output_filename

        with open(dest_path, 'w+') as file:
            for i in email:
                file.write("%s\n" % i)
