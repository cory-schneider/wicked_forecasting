from forecastapp.reportgen import utils


def unique(wslr_list):
    # insert the list into a set
    list_set = set(wslr_list)
    # convert the set to the list
    unique_list = list(list_set)
    return unique_list

def pdcn_plus_product_name(doh_report):
    for row in doh_report:
        pdcn = row[3]
        for x, y in utils.product_names.items():
            if pdcn not in y:
                continue
            else:
                row[3] = str(x) + " - " + str(y)
                break
    return doh_report

def merged_units(vip_cleaned_list, oneportal_cleaned_list, \
                 changelog_cleaned_list, date_list):
    units_report = []

    vip_header = vip_cleaned_list[0]
    merged_header = vip_header
    for i in date_list[1:]:
        merged_header.append(i)

# Write a row for each wholesaler inventory item. Merged report will exclude
# PDCNs which are forecasted but don't have sales history/aren't in VIP report.
# Writes WSLR, WSLR ID, PDCN, ROS, Current inventory.
    for vip_row in vip_cleaned_list[1:]:
        new_row = []
        for i in vip_row:
            new_row.append(i)

# Write a zero for each order date initially, to be replaced if there's an
# order in One Portal.
        for i in range(len(date_list)-1):
            new_row.append(0)
        units_report.append(new_row)

# Indexing within the One Portal report. This is to account for changes in
# output format. Likely unnecessary and is a trade-off because changing
# verbiage will break the program, too.
    bi_header = oneportal_cleaned_list[0]
    oneportal_delivery_index = bi_header.index("Delivery Date")
    oneportal_qty_index = bi_header.index("Order Qty.")
    oneportal_wslr_index = bi_header.index("WSLR ID")
    oneportal_pdcn_index = bi_header.index("Product - PDCN")

# Indexing within the new merged report
    merged_wslr_index = merged_header.index("WSLR ID")
    merged_pdcn_index = merged_header.index("Product - PDCN")

# Inserting order quantity data under the correct date.
# Tracking efficiency by counting the loops. Working on this...
    count = 0
    for r in units_report:
        for oneportal_row in oneportal_cleaned_list:
            count += 1
            if oneportal_row[oneportal_wslr_index] == r[merged_wslr_index] and \
                oneportal_row[oneportal_pdcn_index] == r[merged_pdcn_index]:
                delivery_date = oneportal_row[oneportal_delivery_index]
                qty = oneportal_row[oneportal_qty_index]
                date_index = merged_header.index(delivery_date)
# The += below accounts for inventory date being also a truck date, adds
# the inventory qty and order qty together for calculation purposes
                r[date_index] += qty

    print(f"{count} loops in the report build loop")

    vip_wslr_id_index = vip_header.index("WSLR ID")
    vip_pdcn_index = vip_header.index("Product - PDCN")
# Making Adjustments to the report based on changelog_cleaned_list
    for ticket in changelog_cleaned_list:
        ticket_wslr_id = ticket[1]
        ticket_pdcn = ticket[2]
        adjustment_amount = ticket[3]
        ticket_date = ticket[4]
        for row in units_report:
            wslr_id = row[vip_wslr_id_index]
            pdcn = row[vip_pdcn_index]
            if wslr_id == ticket_wslr_id and pdcn == ticket_pdcn:
                row[merged_header.index(ticket_date)] += adjustment_amount
                if row[merged_header.index(ticket_date)] < 0:
                    row[merged_header.index(ticket_date)] = 0


    units_report.insert(0, merged_header)

    return units_report

def doh_calc_excel_formulas(report_units, forecast_report):
    date_list = forecast_report.date_list
    today = forecast_report.today
    days_between_orders = []
    for i in range(len(date_list) - 1):
        this_day = date_list[i]
        next_day = date_list[i + 1]
        delta = (next_day - this_day).days
        days_between_orders.append(delta)

    doh_report = []
    header = report_units.pop(0)
    ros_index = header.index("DAILY ROS (60 day period)")

# Starting row in the spreadsheet for WSLR/ITEM combos.
    row_count = 3

    for row in report_units:
        ooc_flag = False
        new_row = []
# Appends WSLR, WSLR ID, PDCN, ROS, initial inventory to the new row
        for data in row[0:5]:
            new_row.append(data)
        weekly_ros = "=$E3 * 7"
        new_row.append(weekly_ros)
# Future Feature: dictionary of preferred DOH Targets
        new_row.append(21)
##################
# Calculates DOH for initial inventory. No suggestions made.
        ros = row[ros_index]
# Addresses ROS of zero issues.
        if ros == 0:
            ooc_flag = True
        init_inventory = row[5]
        new_row.append(init_inventory)
# Calculates DOH for initial inventory in excel
        new_row.append("=H3/E3")
# Calculates Units to Target for init inventory in excel
        new_row.append("=($G3-I3)*$E3")
        current_week_order = row[6]
        new_row.append(current_week_order)
# Enters formulas for DOH and Units to Tgt for current week order in excel
        new_row.append("=IF((I3+(K3/$E3))-(K$1-H$1)>0,(I3+(K3/$E3))-(K$1-H$1),0)")
        new_row.append("=($G3-L3)*$E3")
# Performs data entry and enters formulas for first week of suggestions
        first_suggest_week_order = row[7]
        # Actual order
        new_row.append(first_suggest_week_order)
        # Suggested order
        new_row.append(first_suggest_week_order)
        new_row.append("=IF((L3+(O3/$E3))-(N$1-K$1)>0,(L3+(O3/$E3))-(N$1-K$1),0)")
        new_row.append("=($G3-P3)*$E3")
# Performs data entry and enters formulas for second week of suggestions
        second_suggest_week_order = row[8]
        # Actual order
        new_row.append(second_suggest_week_order)
        # Suggested order
        new_row.append(second_suggest_week_order)
        new_row.append("=IF((P3+(S3/$E3))-(R$1-N$1)>0,(P3+(S3/$E3))-(R$1-N$1),0)")
        new_row.append("=($G3-T3)*$E3")
# Performs data entry and enters formulas for remaining
        for order in row[9:]:
            # Actual order
            new_row.append(order)
            # Suggested order
            new_row.append(order)
            new_row.append("")
            new_row.append("")

        doh_report.append(new_row)

    doh_report = pdcn_plus_product_name(doh_report)

    header_labels = []
    for i in header[0:5]:
        header_labels.append(i)
    header_labels.append("WEEKLY ROS")
    header_labels.append("DOH Target")
    header_labels.append("Inventory (Units)")
    header_labels.append("DOH")
    header_labels.append("Units to Target")
    header_labels.append("Actual Order (Units)")
    header_labels.append("Rolling DOH")
    header_labels.append("Units to Target")
    for i in date_list[2:]:
        header_labels.append("Actual Order (Units)")
        header_labels.append("WWB Sugg. Order (Units)")
        header_labels.append("Rolling DOH")
        header_labels.append("Units to Target")
    # header_labels.append(str(date_list[0]) + " Inventory")
    # header_labels.append(str(date_list[0]) + " DOH")
    # header_labels.append(str(date_list[0]) + " DOH Gap")
    # for i in date_list[1:]:
    #     header_labels.append(str(i) + " Order Units")
    #     header_labels.append(str(i) + " Rolling DOH")
    #     header_labels.append(str(i) + " DOH Gap")

    header_dates = []
    for i in range(7):
        header_dates.append("")
    for i in date_list[:2]:
        header_dates.append(i)
        header_dates.append("")
        header_dates.append("")
    for i in date_list[2:]:
        header_dates.append(i)
        header_dates.append("")
        header_dates.append("")
        header_dates.append("")

    doh_report.insert(0, header_labels)
    doh_report.insert(0, header_dates)

    return doh_report
