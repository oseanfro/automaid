import datetime

# Plot interactive figures in HTML format for acoustic events
# WARNING: Plotly files takes a lot of memory so commented by default
events_plotly = True

# Path for input datas
dataPath = "server"

# Generate CSV with RAW data
generate_csv_file = False

# Set a time range of analysis for a specific float
filterDate = {
    "452.112-N-0000": (datetime.datetime(2100, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.112-N-01": (datetime.datetime(2018, 12, 27), datetime.datetime(2100, 1, 1)),
    "452.112-N-02": (datetime.datetime(2018, 12, 28), datetime.datetime(2100, 1, 1)),
    "452.112-N-03": (datetime.datetime(2100, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.112-N-04": (datetime.datetime(2019, 1, 3), datetime.datetime(2100, 1, 1)),
    "452.112-N-05": (datetime.datetime(2019, 1, 4), datetime.datetime(2100, 1, 1)),
    "452.020-P-06": (datetime.datetime(2018, 6, 26), datetime.datetime(2100, 1, 1)),
    "452.020-P-07": (datetime.datetime(2018, 6, 27), datetime.datetime(2100, 1, 1)),
    "452.020-P-08": (datetime.datetime(2018, 8, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-09": (datetime.datetime(2018, 8, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-10": (datetime.datetime(2018, 8, 7), datetime.datetime(2100, 1, 1)),
    "452.020-P-11": (datetime.datetime(2018, 8, 9), datetime.datetime(2100, 1, 1)),
    "452.020-P-12": (datetime.datetime(2018, 8, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-13": (datetime.datetime(2018, 8, 31), datetime.datetime(2100, 1, 1)),
    "452.210-P-14": (datetime.datetime(2020, 2, 5), datetime.datetime(2100, 1, 1)),
    "452.210-P-0014": (datetime.datetime(2020, 2, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-16": (datetime.datetime(2018, 9, 3), datetime.datetime(2100, 1, 1)),
    "452.020-P-17": (datetime.datetime(2018, 9, 4), datetime.datetime(2100, 1, 1)),
    "452.020-P-18": (datetime.datetime(2018, 9, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-19": (datetime.datetime(2018, 9, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-20": (datetime.datetime(2018, 9, 8), datetime.datetime(2100, 1, 1)),
    "452.020-P-21": (datetime.datetime(2018, 9, 9), datetime.datetime(2100, 1, 1)),
    "452.020-P-22": (datetime.datetime(2018, 9, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-23": (datetime.datetime(2018, 9, 12), datetime.datetime(2100, 1, 1)),
    "452.020-P-24": (datetime.datetime(2018, 9, 13), datetime.datetime(2100, 1, 1)),
    "452.020-P-25": (datetime.datetime(2018, 9, 14), datetime.datetime(2100, 1, 1)),
    "452.020-P-0026": (datetime.datetime(2019, 10, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-0027": (datetime.datetime(2019, 9, 26), datetime.datetime(2100, 1, 1)),
    "452.020-P-0028": (datetime.datetime(2019, 8, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-0029": (datetime.datetime(2019, 8, 8), datetime.datetime(2100, 1, 1)),
    "452.020-P-0030": (datetime.datetime(2100, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.020-P-0031": (datetime.datetime(2019, 8, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-0032": (datetime.datetime(2019, 8, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-0033": (datetime.datetime(2019, 8, 11), datetime.datetime(2100, 1, 1)),
    "452.020-P-0034": (datetime.datetime(2019, 8, 13), datetime.datetime(2100, 1, 1)),
    "452.020-P-0035": (datetime.datetime(2019, 8, 14), datetime.datetime(2100, 1, 1)),
    "452.020-P-0036": (datetime.datetime(2019, 8, 15), datetime.datetime(2100, 1, 1)),
    "452.020-P-0037": (datetime.datetime(2019, 8, 18), datetime.datetime(2100, 1, 1)),
    "452.020-P-0038": (datetime.datetime(2019, 8, 18), datetime.datetime(2100, 1, 1)),
    "452.020-P-0039": (datetime.datetime(2019, 8, 18), datetime.datetime(2100, 1, 1)),
    "452.020-P-0040": (datetime.datetime(2019, 8, 19), datetime.datetime(2100, 1, 1)),
    "452.020-P-0041": (datetime.datetime(2019, 8, 20), datetime.datetime(2100, 1, 1)),
    "452.020-P-0042": (datetime.datetime(2019, 8, 21), datetime.datetime(2100, 1, 1)),
    "452.020-P-0043": (datetime.datetime(2019, 8, 21), datetime.datetime(2100, 1, 1)),
    "452.020-P-0044": (datetime.datetime(2019, 8, 22), datetime.datetime(2100, 1, 1)),
    "452.020-P-0045": (datetime.datetime(2019, 8, 22), datetime.datetime(2100, 1, 1)),
    "452.020-P-0046": (datetime.datetime(2019, 8, 23), datetime.datetime(2100, 1, 1)),
    "452.020-P-0047": (datetime.datetime(2019, 8, 23), datetime.datetime(2100, 1, 1)),
    "452.020-P-0048": (datetime.datetime(2019, 8, 27), datetime.datetime(2100, 1, 1)),
    "452.020-P-0049": (datetime.datetime(2019, 8, 25), datetime.datetime(2100, 1, 1)),
    "452.020-P-0050": (datetime.datetime(2019, 8, 12), datetime.datetime(2100, 1, 1)),
    "452.020-P-0051": (datetime.datetime(2020, 2, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-0052": (datetime.datetime(2019, 8, 17), datetime.datetime(2100, 1, 1)),
    "452.020-P-0053": (datetime.datetime(2019, 8, 19), datetime.datetime(2100, 1, 1)),
    "452.020-P-0054": (datetime.datetime(2019, 8, 21), datetime.datetime(2100, 1, 1)),
    "452.020-P-0057": (datetime.datetime(2100, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.020-P-0060": (datetime.datetime(2100, 1, 1), datetime.datetime(2100, 1, 1))
}
