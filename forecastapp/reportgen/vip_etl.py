from datetime import datetime, date, timedelta
import datetime as dt
import numpy as np
import math
import csv
import sys
import dateutil.parser
import os
from flask import (flash)
from collections import defaultdict
from forecastapp.reportgen import utils

# In order to use the nearest function on the OnePortal report, I'll have to
# get the date list earlier than I am now, which is in the reportUnits portion.
# Then run nearest on

def merge_data_vip(cleaned):
    merged_data = []
    for row in cleaned:
        for x in merged_data:
            if row[2] == x[2] and row[3] == x[3]:
                row[4] += x[4]
                row[5] += x[5]
                merged_data.remove(x)
        merged_data.append(row)

    merged_data = sorted(merged_data)

    return merged_data

def vip_clean(vip_input):
    vip_cleaned = []
    with open(vip_input, "r", newline = "") as input_file:
        reader = csv.reader(input_file)
        next(reader)

        for row in reader:
# Likely I should change this try except to something more specific to the
# issue, which is the function finding an empty row at the bottom of some
# inventory reports and returning an index out of range error.
            try:
                state = str(row[0])
                wholesaler = "".join([i for i in str(row[1]) if i.isalpha() or i == " "])
                try:
                    wholesaler_id = int(row[2])
                except:
                    wholesaler_id = int(''.join([i for i in row[2] if i.isdigit()]))
                wholesaler_id = utils.merge_wslr(wholesaler_id)
                pdcn = utils.pdcn_cleanup(str(row[4]))
                inventory_units = round(float(row[5]), 1)
                if inventory_units < 0:
                    inventory_units = 0
                daily_ros = utils.round_up(float(row[6]))
            except:
                break

            vip_cleaned.append([
                    state,
                    wholesaler,
                    wholesaler_id,
                    pdcn,
                    daily_ros,
                    inventory_units])

    vip_cleaned = sorted(vip_cleaned)
    vip_merged = merge_data_vip(vip_cleaned)

    vip_header = [
            "WSLR State",
            "WSLR Name",
            "WSLR ID",
            "Product - PDCN",
            "DAILY ROS (60 day period)",
            datetime.date(datetime(2020, 5, 29))]
    vip_merged.insert(0, vip_header)

    output_filename = "/forecasting/vip_output" + str(today) + ".csv"

    with open(output_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for i in vip_merged:
            writer.writerow(i)

    return vip_merged
