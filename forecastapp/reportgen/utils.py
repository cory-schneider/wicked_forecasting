import math
import os
import csv
import secrets
from flask import current_app
from dateutil.relativedelta import relativedelta, MO

wslr_info = {
    "Great Bay Dist" : [40901, 40915],
    "North Florida Sales" : [70918, 70923],
    "Bernie Little Dist" : [40920, 40919],
    "Southern Crown Partners" : [43975, 43925],
    "Southern Crown Brunswick" : [91094, 21052, 21075],
    "RH Barringer" : [53234, 53296, 33245],
    "Harris Beverage" : [63221, 63236],
    "Carolina Eagle" : [43233, 43272]
    }

pdcn_remap = {
    # Pernicious 6pk tray
    "10164W6" : ["10164Z6"],
    # Pernicious 4pk btl
    "101664S" : ["101664S", "101664Z"],
    # Pernicious 16oz loose
    "101616S" : ["101616Z", "101616S"],
    # Burst 6pk tray
    "10JW46W" : ["10JW46W", "10JW4Z6", "10JW4W7", "10ZH4W7", "10JU2Z4", "10JU4Z6", "10JU4W7", "10JW4W6", "10JV4W6", "10JV4Z6"],
    # Burst 1/6 bbl
    "10JW97X" : ["10JW970", "10JW97X", "10JW97B", "10JU97B", "10JU970", "10JV970"],
    # Burst 1/2 bbl
    "10JW94X" : ["10JW940", "10JW94X", "10JW94G", "10JU94G", "10JU94W", "10JU940", "10JV940"],
    # Appalachia 6pk tray
    "10EM4W6" : ["10EM4W6", "10EM4Z6", "101K4Z6"],
    # Appalachia 16oz loose
    "10EM16S" : ["10EM16Z", "10EM16S"],
    # Coastal Love 6pk can tray
    "10KS6S4" : ["10KS6S4", "10KS6Z4"],
    # Lt Dank 6pk can tray
    "10594W6" : ["10594W6", "10594Z6"],
    # Freak 6pk can tray
    "105I4W6" : ["105I4W6", "105I4Z6"],
    # Freak 4pk btl tray
    "105I64S" : ["105I64Z", "105I64S"],
    # NapCom 6pk can tray
    "102Y4W6" : ["102Y4W6", "102Y4Z6"],
    # NapCom 16oz loose
    "102Y16S" : ["102Y16Z", "102Y16S", "102Y6Z4"],
    # Rick's 6pk tray
    "102Q4S6" : ["102Q4Z6", "102Q4S6"],
    # Smashville 6pk tray
    "108G4S6" : ["108G4S6", "108G4Z6"],
    # Smashville 16oz loose
    "108G16S" : ["108G16S", "108G16Z", "108G6Z4"]
    }

product_names = {
    "Pernicious IPA 4/6/12 oz. can" : "10164W6",
    "Pernicious IPA 24pk 16 oz. can" : "101616S",
    "Pernicious IPA 24pk 12 oz. can" : "10162Z4",
    "Pernicious IPA 6/4/12 oz. btl" : "101664S",
    "Pernicious IPA 1/6 bbl" : "1016970",
    "Pernicious IPA 1/2 bbl" : "1016940",
    "Burst Session Sour 4/6/12 oz. can" : "10JW46W",
    "Burst Session Sour 1/6 bbl" : "10JW97X",
    "Burst Session Sour 1/2 bbl" : "10JW94X",
    "Napoleon Complex 4/6/12 oz. can" : "102Y4W6",
    "Napoleon Complex 1/6 bbl" : "102Y970",
    "Napoleon Complex 1/2 bbl" : "102Y940",
    "Napoleon Complex 24pk 16 oz. can" : "102Y16S",
    "Lieutenant Dank 4/6/12 oz. can" : "10594W6",
    "Lieutenant Dank 2/12/12 oz. can" : "10591Z2",
    "Lieutenant Dank 1/6 bbl" : "1059970",
    "Lieutenant Dank 1/2 bbl" : "1059940",
    "Appalachia Session IPA 4/6/12 oz. can" : "10EM4W6",
    "Appalachia Session IPA 2/12/12 oz. can" : "10EM1Z2",
    "Appalachia Session IPA 24pk 16 oz. can" : "10EM16S",
    "Appalachia Session IPA 1/6 bbl" : "10EM970",
    "Appalachia Session IPA 1/2 bbl" : "10EM940",
    "Rick's Pilsner 4/6/12 oz. can" : "102Q4S6",
    "Rick's Pilsner 1/6 bbl" : "102Q970",
    "Rick's Pilsner 1/2 bbl" : "102Q940",
    "Coastal Love Hazy IPA 4/6/12 oz. can" : "10KS4W6",
    "Coastal Love Hazy IPA 6/4/16 oz. can" : "10KS6S4",
    "Coastal Love Hazy IPA 1/6 bbl" : "10KS970",
    "Coastal Love Hazy IPA 1/2 bbl" : "10KS940",
    "Freak of Nature DIPA 4/6/12 oz. can" : "105I4W6",
    "Freak of Nature DIPA 6/4/12 oz. btl" : "105I64S",
    "Freak of Nature DIPA 1/6 bbl" : "105I970",
    "Freak of Nature DIPA 1/2 bbl" : "105I940",
    "Smashville 4/6/12 oz. can" : "108G4S6",
    "Smashville 24pk 16 oz. can" : "108G16S",
    "Smashville 1/6 bbl" : "108G970",
    "Smashville 1/2 bbl" : "108G940",
    "Elevation Ale 1/6 bbl" : "108F970",
    "Elevation Ale 1/2 bbl" : "108F940",
    }

def pdcn_cleanup(pdcn):
    for x, y in pdcn_remap.items():
        """Cleans up discrepancies between OnePortal ordering
        numbers and VIP inventory numbers."""
        if pdcn in y:
            pdcn = x
    return pdcn

def round_up(n, decimals=1):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier)/ multiplier

def merge_wslr(wslr_id):
    """Identifies which wholesaler warehouses need to be merged
    from preset dictionary called wslr_info. May eventually allow user
    input for this feature, or draw from a csv file instead of
    building into the script itself."""
    for x, y in wslr_info.items():
        if wslr_id not in y:
            continue
        else:
            #row[0] = str(x).upper()
            wslr_id = ', '.join(map(str, y))
            break
    wslr_id = str(wslr_id)
    return wslr_id

def save_csv(form_csv):
    """
    Saves csv file to user's temporary folder and returns the full file path.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_csv.filename)
    csv_fn = random_hex + f_ext
    csv_path = os.path.join(current_app.root_path, 'temp', csv_fn)

    form_csv.save(csv_path)

    return csv_path

def pdcn_plus_product_name(pdcn):
    for x, y in product_names.items():
        if pdcn not in y:
            continue
        else:
            pdcn_verbose = str(x) + " - " + str(y)
            break
    return pdcn_verbose

def unique(wslr_list):
    # insert the list into a set
    list_set = set(wslr_list)
    # convert the set to the list
    unique_list = list(list_set)
    return unique_list

def prev_monday(date):
    prev_monday = date + relativedelta(weekday=MO(-1))
    return prev_monday
