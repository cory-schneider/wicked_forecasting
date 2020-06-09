from forecastapp.reportgen import utils

def email_writer(report_doh, date_list):

    end_date = date_list[-1]

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
    for i in report_doh[2:]:
        wslr_id_num = str(i[2])
        wslr_list.append(wslr_id_num)
    wslr_list = unique(wslr_list)
    wslr_list_names_too = []
    for i in wslr_list:
        new_wslr = []
        new_wslr.append(i)
        for r in report_doh[2:]:
            if i == str(r[2]):
                wslr_name = str(r[1])
                new_wslr.append(wslr_name)
                break
        wslr_list_names_too.append(new_wslr)

    # Runs through days on hand report to write emails for each wholesaler in list
    today_date = str(dt.date.today())
    for w in wslr_list_names_too:
        email = []
        email.append(f"Greetings {w[1]} team,")
        email.append("")
        email.append(opener)
        email.append("")
        item_list = []
        for r in report_doh:
            if str(r[2]) == w[0]:
                new_item = r[3] + " - "
                item_list.append(new_item)
        email.append("Tickets Requested:")
        for d in date_list[2:5]:
            email.append(str(d) + ":")
            for i in item_list:
                email.append(i)
            email.append("")
        email.append("")
        email.append("Orders Requested:")
        for d in date_list[5:]:
            email.append(str(d) + ":")
            for i in item_list:
                email.append(i)
            email.append("")
        email.append(closer)
        wslr_stripped = w[1].replace(" ", "").lower() + w[0].replace(", ", "")
        output_filename = "/forecasting/emails/" + today_date + wslr_stripped + ".txt"

        with open(output_filename, 'w+') as file:
            for i in email:
                file.write("%s\n" % i)
