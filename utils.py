# -*-coding:Utf-8 -*
import re
import glob
from obspy import UTCDateTime
import plotly.graph_objs as graph
from datetime import datetime, timedelta
import hashlib


#
# Log files utilities
#

# Concatenate .000 files .LOG and .BIN files in the path
def concatenate_files(path):
    #LOG FILES
    log_files_path = glob.glob(path + "*.LOG")
    log_files_path_filtered = list()
    bin_files_path = glob.glob(path + "*.BIN")

    for log_file_path in log_files_path:
        ok_file = True
        for bin_file_path in bin_files_path:
            if bin_file_path[:-4] == log_file_path[:-4]:
                ok_file = False
                break
        if ok_file :
            log_files_path_filtered.append(log_file_path)



    for log_file_path in log_files_path_filtered:
        logstring = ""
        files_to_merge = glob.glob(log_file_path[:-4] +".[0-9][0-9][0-9]")
        files_to_merge += log_files_path
        files_to_merge.sort()
        if len(files_to_merge) > 1:
            for file_to_merge in files_to_merge :
                if file_to_merge[-3:].isdigit():
                    with open(file_to_merge, "r") as fl:
                        # We assume that files are sorted in a correct order
                        logstring += fl.read()
                else :
                    if len(logstring) > 0:
                        # If log extension is not a digit and the log string is not empty
                        # we need to add it at the end of the file
                        with open(file_to_merge, "r") as fl:
                            logstring += fl.read()
                        with open(file_to_merge, "w") as fl:
                            fl.write(logstring)
                        logstring = ""
    #BIN FILES
    for bin_file_path in bin_files_path:
        bin = b''
        files_to_merge = list(glob.glob(bin_file_path[:-4] +".[0-9][0-9][0-9]"))
        files_to_merge.append(bin_file_path)
        files_to_merge.sort()
        if len(files_to_merge) > 1:
            for file_to_merge in files_to_merge :
                if file_to_merge[-3:].isdigit():
                    with open(file_to_merge, "rb") as fl:
                        # We assume that files are sorted in a correct order
                        bin += fl.read()
                else :
                    if len(bin) > 0:
                        # If log extension is not a digit and the log string is not empty
                        # we need to add it at the end of the file
                        with open(file_to_merge, "rb") as fl:
                            bin += fl.read()
                        with open(file_to_merge, "wb") as fl:
                            fl.write(bin)
                        bin = b''


# Split logs in several lines
def split_log_lines(content):
    splitted = []
    splitted = re.split(r'[\r\n][\n]?',content);
    if splitted[-1] == "":
        splitted = splitted[:-1]
    return splitted


def find_timestamped_value(regexp, line):
    v = 0
    d = UTCDateTime(0)
    value_catch = re.findall(regexp, line)
    if len(value_catch) > 0:
        timestamp_catch = re.findall("(\d+):", line)
        if len(timestamp_catch) > 0 :
            v = value_catch[0]
            d = UTCDateTime(int(timestamp_catch[0]))
            return [v, d]
    return []

# Search timestamps for a specific keyword
def find_timestamped_values(regexp, content):
    timestamped_values = list()
    lines = split_log_lines(content)
    last_value = 0
    for line in lines:
        value_catch = re.findall(regexp, line)
        timestamp_catch = re.findall("(\d+):", line)
        if len(value_catch) > 0:
            if(len(timestamp_catch) > 10):
                timestamp_catch = timestamp_catch[len(timestamp_catch)-10:]
            v = value_catch[0]
            try:
                d = UTCDateTime(int(timestamp_catch[0]))
                last_value = int(timestamp_catch[0])
            except:
                d = UTCDateTime(last_value)
            timestamped_values.append([v, d])
    return timestamped_values

def find_timestampedUTC_values(regexp, content):
    timestamped_values = list()
    last_value = 0
    v = 0
    d = UTCDateTime()
    lines = split_log_lines(content)
    for line in lines:
        value_catch = re.findall(regexp, line)
        timestamp_catch = re.findall("(\S+):\\[", line)
        if len(value_catch) > 0:
            v = value_catch[0]
            try:
                d = UTCDateTime(str(timestamp_catch[0]), iso8601=True)
                last_value = timestamp_catch[0]
            except:
                d = UTCDateTime(last_value)
            timestamped_values.append([v, d])
    return timestamped_values

# Format log files
def format_log(log):
    datetime_log = ""
    lines = split_log_lines(log)
    last_value = 0
    for line in lines:
        catch = re.findall("(\d+):", line)
        if len(catch) > 0:
            timestamp = catch[0]
            if(len(timestamp) > 10):
                print(("error value : " + timestamp))
                timestamp = timestamp[len(timestamp)-10:]
            value = int(timestamp)
            try:
                isodate = UTCDateTime(value).isoformat()
                last_value = value
            except:
                isodate = UTCDateTime(last_value).isoformat()
            datetime_log += line.replace(timestamp, isodate) + "\r\n"
        else :
            datetime_log += line + "\r\n"
    formatted_log = "".join(datetime_log)
    return formatted_log


# verify log format
def verify_format_log(log):
    error_log = False
    correct_log = ""
    lines = split_log_lines(log)
    for line in lines:
        catch = re.findall("(\d+):[(\w+ *),(\d+)].*", line)
        if len(catch) > 0:
            print((catch[0][0]))
            if len(catch[0][0]) > 10 :
                error_log = True
                continue
            print((catch[0]))
            if len(catch[0] < 3) :
                error_log = True
                continue
            correct_log += line + "\r\n"
        else :
            correct_log += line + "\r\n"
    if error_log:
        return correct_log
    return ""


# Get date from a .LOG or a .MER file name
def get_date_from_file_name(filename):
    hexdate = re.findall("(.+\d+_)?([A-Z0-9]+)\.(BIN|LOG|MER|S41|[0-9]{3})", filename)[0][1]
    timestamp = int(hexdate, 16)
    return UTCDateTime(timestamp)


def get_md5_from_bytes(bytes):
    result = hashlib.md5(bytes)
    return result.hexdigest()
def get_md5_from_string(string):
    result = hashlib.md5(string.encode())
    return result.hexdigest()


#
# Plot utilities
#

# Plot vertical lines with plotly
def plotly_vertical_shape(position, ymin=0, ymax=1, name='name', color='blue'):
    xval = list()
    yval = list()
    for ps in position:
        xval.append(ps)
        xval.append(ps)
        xval.append(None)
        yval.append(ymin)
        yval.append(ymax)
        yval.append(None)

    lines = graph.Scatter(x=xval,
                          y=yval,
                          name=name,
                          line=dict(color=color,
                                    width=1.5),
                          hoverinfo='x',
                          mode='lines'
                          )
    return lines


# Get an array of date objects
def get_date_array(date, length, period):
    date_list = list()
    i = 0
    while i < length:
        date_list.append(date + i * period)
        i += 1
    return date_list


# Get an array of time values
def get_time_array(length, period):
    # Compute time
    time_list = list()
    i = 0.0
    while i < length:
        time_list.append(i * period)
        i += 1.
    return time_list


# Convert raw data amplitude to pascal
def counts2pascal(data):
    factor = 0.178 / 1000. * 10. ** (23. / 20.) * 2. ** 24. / 5. * 2. ** 4.
    return data / factor

def convert2dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """

  #  Populate the dictionary with object meta datalong
  obj_dict = {
  }

  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)
  return obj_dict


def totimestamp(dt, epoch = datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

def toJuld(utcdatetime, reference = UTCDateTime("1950-01-01T00:00:00")):
    if isinstance(utcdatetime,UTCDateTime):
        # Calculates the time difference in seconds between two UTCDateTime objects.
        # The time difference is given as float data type and may also contain a negative number.
        diff = utcdatetime - reference
        return diff/86400.0

    else :
        print("Wrong parameter need UTCDATETIME instance")
        print(type(utcdatetime))
        return
