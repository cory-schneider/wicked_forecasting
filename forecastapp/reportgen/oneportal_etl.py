from forecastapp.reportgen import utils

def oneportal_pdcn(y):
    """Merges order quantities for PDCN/order date in cases where warehouses
    share/transfer inventory"""
    combined_data = []
    for row in y:
        for x in combined_data:
            if row[1] == x[1] and row[2] == x[2] and row[4] == x[4]:
                row[3] += x[3]
                combined_data.remove(x)
        combined_data.append(row)
    combined_data = sorted(combined_data)
    return combined_data

def nearest(dates, truck):
    return min([i for i in dates[1:] if i < truck], key=lambda x: abs(x - truck))

def oneportal_clean():
    oneportal_cleaned = []
    with open(oneportal_input, 'r', newline = "") as input_file:
        reader = csv.reader(input_file, delimiter = ",")
        next(reader)

        for row in reader:
            wholesaler = str(row[4])
            try:
                wholesaler_id = int(row[3])
            except:
                wholesaler_id = int(''.join([i for i in row[3] if i.isdigit()]))
            wholesaler_id = utils.merge_wslr(wholesaler_id)
            pdcn = str(row[1])
            pdcn = utils.pdcn_cleanup(pdcn)
            order_qty = int(row[8])
            date1 = dateutil.parser.parse(row[9]).strftime("%Y/%m/%d")
            date_split = date1.split("/")
            y = int(date_split[0])
            m = int(date_split[1])
            d = int(date_split[2])
            delivery_date = datetime.date(datetime(y, m, d))
            delivery_date = delivery_date - dt.timedelta(days=delivery_date.weekday())
            wslr_contact = str(row[7])

            oneportal_cleaned.append([
                wholesaler,
                wholesaler_id,
                pdcn,
                order_qty,
                delivery_date,
                wslr_contact])

    oneportal_cleaned = oneportal_pdcn(oneportal_cleaned)

# Create a dictionary of email addresses for each wslr
    email_dict = defaultdict(list)
    for row in oneportal_cleaned:
        wslr_id = row[1]
        email = row[-1]
        if email not in email_dict[wslr_id]:
            email_dict[wslr_id].append(email)

    # email_set = set(email_dict)
    # unique_emails = list(email_set)
    # print(unique_emails)

    bi_header = ["WSLR Name",
                    "WSLR ID",
                    "Product - PDCN",
                    "Order Qty.",
                    "Delivery Date",
                    "WSLR Contact"
                    ]
    oneportal_cleaned.insert(0, bi_header)

    output_filename = "/forecasting/oneportal_output" + str(today) + ".csv"

    with open(output_filename, 'w', newline = '') as output:
        writer = csv.writer(output)
        for i in oneportal_cleaned:
            writer.writerow(i)

    return oneportal_cleaned, email_dict
