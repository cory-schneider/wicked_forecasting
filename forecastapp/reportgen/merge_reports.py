from forecastapp.reportgen import utils
from openpyxl import Workbook
from openpyxl.styles import Color, PatternFill, Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.formula.translate import Translator
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import CellIsRule
import os
from flask import (current_app)

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
