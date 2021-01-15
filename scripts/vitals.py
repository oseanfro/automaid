import re
from obspy import UTCDateTime
import plotly.graph_objs as graph
import plotly.offline as plotly
import os
import utils
import datetime

class Vitals:
    _state = None
    _dataType = None
    client = None
    buoy = None
    date = None
    longitude = None
    latitude = None
    hdop = None
    vdop = None
    Pint = None
    Pintmin = None
    Pext = None
    Pextrange = None
    divepath = []
    deployed = None
    def __init__(self,client,buoy):
        self._state = "Empty"
        self._dataType = "Vitals"
        self.client = client
        self.buoy = buoy
        self.date = None
        self.hdop = None
        self.longitude = None
        self.latitude = None
        self.pint = None
        self.pext = None
        self.pextrange = None
        self.vbat = None
        self.vbatmin = None
        self.vdop = None
        self.divepath = []
        self.deployed = False
    def split(self,line,mdives,path,filterDate):
        line_buoy = re.match(".* >>> BUOY (\d+) (.*) <<<",line)
        line_coord = re.match(".*: ([NS])(\d+)deg(\d+\.\d+)mn, ([EW])(\d+)deg(\d+\.\d+)mn",line)
        line_dop = re.match(".* hdop (.*), vdop (.*)",line)
        line_bat = re.match(".* Vbat (\d+)mV \(min (\d+)mV\)",line)
        line_Pint = re.match(".* Pint (\d+)Pa",line)
        line_Pext = re.match(".* Pext (-?\d+)mbar \(range (-?\d+)mbar\)",line)
        line_emerg = re.match(".* EMERGENCY .*",line)
        begin = 0
        end = 0
        buffdate = 0

        if self.buoy in filterDate.keys():
            begin = filterDate[self.buoy][0]
            end = filterDate[self.buoy][1]
        else:
            begin = datetime.datetime(1000, 1, 1)
            end = datetime.datetime(3000, 1, 1)

        if line_buoy:
            buffdate = datetime.datetime.strptime(line_buoy.group(2), "%Y-%m-%dT%H:%M:%S")
        if buffdate == 0:
            buffdate = datetime.datetime(1000, 1, 1)
        if begin < buffdate:
            self.deployed = True
        if line_buoy:
            if  self.date is None:
                self.date = utils.totimestamp(datetime.datetime.strptime(line_buoy.group(2), "%Y-%m-%dT%H:%M:%S"))
                for dive in mdives:
                    if (self.date <= dive.end_date.timestamp and self.date >= dive.date.timestamp):
                        divefiles = os.listdir(path + "/" + self.buoy + "/processed/" + dive.directory_name)
                        for divefile in divefiles:
                            divefilepath = "/" + dive.directory_name + "/" + divefile
                            if divefilepath not in self.divepath:
                                self.divepath.append("/" + dive.directory_name + "/" + divefile)

                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_coord:
            if self.latitude is None and self.longitude is None:
                if line_coord.group(1) == "N":
                    sign = 1
                elif line_coord.group(1) == "S":
                    sign = -1
                self.latitude = sign*(float(line_coord.group(2)) + float(line_coord.group(3))/60.)
                if line_coord.group(4) == "E":
                    sign = 1
                elif line_coord.group(4) == "W":
                    sign = -1
                self.longitude = sign*(float(line_coord.group(5)) + float(line_coord.group(6))/60.)
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_dop:
            if self.hdop is None  and self.vdop is None :
                self.hdop = line_dop.group(1)
                self.vdop = line_dop.group(2)
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_bat:
            if self.vbat is None and self.vbatmin is None :
                self.vbat = int(line_bat.group(1))
                self.vbatmin = int(line_bat.group(2))
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_Pint:
            if not self.pint:
                self.pint= int(line_Pint.group(1))
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_Pext:
            if self.pext is None and self.pextrange is None :
                self.pext = int(line_Pext.group(1))
                self.pextrange = int(line_Pext.group(2))
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if not self.buoy is None \
        and not  self.date is None\
        and not  self.latitude is None \
        and not  self.longitude is None \
        and not  self.hdop is None \
        and not  self.vdop is None \
        and not  self.vbat is None \
        and not  self.vbatmin is None \
        and not  self.pint is None \
        and not  self.pext is None \
        and not  self.pextrange is None:
            self._state = "Full"
        #if buffdate < begin:
        #    self._state = "Not_ready"

class Emergency:
    _state = None
    _dataType = None
    client = None
    buoy = None
    date = None
    longitude = None
    latitude = None
    cause = None
    def __init__(self,client,buoy):
        self._state = "Empty"
        self._dataType = "Emergency"
        self.client = client
        self.buoy = buoy
        self.date = None
        self.longitude = None
        self.latitude = None
        self.cause = None

    def split(self,line):
        line_buoy = re.match("(.*): EMERGENCY buoy (\d+) (.*)",line)
        line_coord = re.match(".*: EMERGENCY ([NS])(\d+)deg(\d+\.\d+)mn ([EW])(\d+)deg(\d+\.\d+)mn",line)

        if line_buoy:
            if  self.date is None and self.cause is None:
                self.date = utils.totimestamp(datetime.datetime.strptime(line_buoy.group(1), "%Y%m%d-%Hh%Mmn%S"))
                self.cause = line_buoy.group(3)
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if line_coord:
            if self.latitude is None and self.longitude is None:
                if line_coord.group(1) == "N":
                    sign = 1
                elif line_coord.group(1) == "S":
                    sign = -1
                self.latitude = sign*(float(line_coord.group(2)) + float(line_coord.group(3))/60.)
                if line_coord.group(4) == "E":
                    sign = 1
                elif line_coord.group(4) == "W":
                    sign = -1
                self.longitude = sign*(float(line_coord.group(5)) + float(line_coord.group(6))/60.)
                self._state = "In_progress"
            else:
                self._state = "Interrupted"
        if not self.buoy is None \
        and not  self.date is None\
        and not  self.latitude is None \
        and not  self.longitude is None \
        and not self.cause is None:
            self._state = "Full"

def list_vitals(filepath,client,buoy,mdives,datapath,filterDate):
    listread = list()
    listdive = list()
    for dive in mdives:
        if (dive.get_buoy() == buoy):
            listdive.append(dive)
    vital = Vitals(client,buoy)
    emergency = Emergency(client,buoy)
    with open(filepath, "r") as fs:
        lines = fs.readlines()
        for line in lines:
            vital.split(line,listdive,datapath,filterDate)
            emergency.split(line)
            if vital._state is "Full":
                listread.append(utils.convert2dict(vital))
                vital = Vitals(client,buoy)
            if vital._state is "Interrupted":
                listread.append(utils.convert2dict(vital))
                vital = Vitals(client,buoy)
                vital.split(line,mdives,datapath,filterDate)
            if emergency._state is "Full":
                listread.append(utils.convert2dict(emergency))
                emergency = Emergency(client,buoy)
            if emergency._state is "Interrupted":
                listread.append(utils.convert2dict(emergency))
                emergency = Emergency(client,buoy)
                emergency.split(line)
        if vital._state is "In_progress":
            vital._state = "Interrupted"
            listread.append(utils.convert2dict(vital))
        if emergency._state is "In_progress":
            emergency._state = "Interrupted"
            listread.append(utils.convert2dict(emergency))
    return listread

def sort_vitals(elem):
    match = re.match("([A-Z0-9]{8}).vit",elem)
    return int(match.group(1),16)


def merge_vitals(path,final):
    if os.path.exists(os.path.join(path,final)):
        os.remove(os.path.join(path,final))
    files_to_merges = [m.split('/')[-1] for m in glob.glob(path+"/[A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9][A-Z0-9].vit")]
    if(len(files_to_merges)>0) :
        files_sorted  = sorted(files_to_merges,key=sort_vitals)
        with open(os.path.join(path,final), "a") as final_file:
            for file in files_sorted :
                with open(os.path.join(path,file), "r") as splitted:
                    final_file.write(splitted.read())



#on rentre une list de dictionnaire
#et renvoie une liste plus complete avec des donnee process
def process (list):
    date_origine = None
    for dict in list:
        if not dict['date']:
            dict['buoy_life']= ""
        else:
            if not date_origine:
                date_origine = dict['date']
            dict['buoy_life']= dict['date'] - date_origine
    return list

def sortdictbydate(value):
    return value['date']
def sortdictbyname(value):
    if value['buoy'][-4:].isdigit():
        return value['buoy'][-4:]
    elif value['buoy'][-2:].isdigit():
        return value['buoy'][-2:]

def plot_battery_voltage(vital_file_path, vital_file_name, begin, end):
    # Read file
    with open(vital_file_path + vital_file_name, "r") as f:
        content = f.read()

    # Find battery values
    content = content.replace(' ', '')
    content = content.replace('>','')
    battery_catch = re.findall("(.+):Vbat(\d+)mV\(min(\d+)mV\)", content)

    date = [UTCDateTime(0).strptime(i[0], "%Y%m%d-%Hh%Mmn%S") for i in battery_catch]
    voltage = [float(i[1])/1000. for i in battery_catch]
    minimum_voltage = [float(i[2])/1000. for i in battery_catch]

    voltage = [x for _,x in sorted(zip(date,voltage))]
    minimum_voltage = [x for _,x in sorted(zip(date,minimum_voltage))]
    date = sorted(date)

    if len(date) < 1:
        return

    # Get values between the appropriate date
    i = 0
    while date[i] < begin and i < len(date)-1:
        i += 1
    j = 0
    while date[j] < end and j < len(date)-1:
        j += 1
    date = date[i:j]
    voltage = voltage[i:j]
    minimum_voltage = minimum_voltage[i:j]

    # Add battery values to the graph
    voltage_line = graph.Scatter(x=date,
                                 y=voltage,
                                 name="voltage",
                                 line=dict(color='blue',
                                           width=2),
                                 mode='lines+markers')

    minimum_voltage_line = graph.Scatter(x=date,
                                         y=minimum_voltage,
                                         name="minimum voltage",
                                         line=dict(color='orange',
                                                   width=2),
                                         mode='lines+markers')

    data = [voltage_line, minimum_voltage_line]

    layout = graph.Layout(title="Battery level in \"" + vital_file_name + "\"",
                          xaxis=dict(title='Coordinated Universal Time (UTC)', titlefont=dict(size=18)),
                          yaxis=dict(title='Voltage (Volts)', titlefont=dict(size=18)),
                          hovermode='closest'
                          )

    plotly.plot({'data': data, 'layout': layout},
                filename=os.path.join(os.path.dirname(os.path.dirname(vital_file_path)), "processed/",  "voltage.html"),
                auto_open=False)


def plot_internal_pressure(vital_file_path, vital_file_name, begin, end):
    # Read file
    with open(vital_file_path + vital_file_name, "r") as f:
        content = f.read()

    # Find battery values
    content = content.replace(' ', '')
    content = content.replace('>','')
    internal_pressure_catch = re.findall("(.+):Pint(-?\d+)Pa", content)
    date = [UTCDateTime(0).strptime(i[0], "%Y%m%d-%Hh%Mmn%S") for i in internal_pressure_catch]
    internal_pressure = [float(i[1])/100. for i in internal_pressure_catch]

    internal_pressure_catch = [x for _,x in sorted(zip(date,internal_pressure_catch))]
    internal_pressure = [x for _,x in sorted(zip(date,internal_pressure))]
    date = sorted(date)

    if len(date) < 1:
        return

    # Get values between the appropriate date
    i = 0
    while date[i] < begin and i < len(date)-1:
        i += 1
    j = 0
    while date[j] < end and j < len(date)-1:
        j += 1
    date = date[i:j]
    internal_pressure = internal_pressure[i:j]

    # Add battery values to the graph
    internal_pressure_line = graph.Scatter(x=date,
                                           y=internal_pressure,
                                           name="internal pressure",
                                           line=dict(color='blue',
                                                     width=2),
                                           mode='lines+markers')

    data = [internal_pressure_line]

    layout = graph.Layout(title="Internal pressure in \"" + vital_file_name + "\"",
                          xaxis=dict(title='Coordinated Universal Time (UTC)', titlefont=dict(size=18)),
                          yaxis=dict(title='Internal pressure (millibars)', titlefont=dict(size=18)),
                          hovermode='closest'
                          )

    plotly.plot({'data': data, 'layout': layout},
                filename=os.path.join(os.path.dirname(os.path.dirname(vital_file_path)), "processed/",  "internal_pressure.html"),
                auto_open=False)


def plot_pressure_offset(vital_file_path, vital_file_name, begin, end):
    # Read file
    with open(vital_file_path + vital_file_name, "r") as f:
        content = f.read()

    # Find battery values
    content = content.replace(' ', '')
    content = content.replace('>','')
    pressure_offset_catch = re.findall("(.+):Pext(-?\d+)mbar\(range(-?\d+)mbar\)", content)
    date = [UTCDateTime(0).strptime(i[0], "%Y%m%d-%Hh%Mmn%S") for i in pressure_offset_catch]
    pressure_offset = [int(i[1]) for i in pressure_offset_catch]
    pressure_offset_range = [int(i[2]) for i in pressure_offset_catch]

    pressure_offset = [x for _,x in sorted(zip(date,pressure_offset))]
    pressure_offset_range = [x for _,x in sorted(zip(date,pressure_offset_range))]
    date = sorted(date)

    if len(date) < 1:
        return

    # Filter wrong values
    res = [(x, y, z) for x, y, z in zip(pressure_offset, pressure_offset_range, date) if x != -2147483648]
    pressure_offset = [x[0] for x in res]
    pressure_offset_range = [x[1] for x in res]
    date = [x[2] for x in res]
    if len(date) < 1:
        return

    # Get values between the appropriate date
    i = 0
    while date[i] < begin and i < len(date)-1:
        i += 1
    j = 0
    while date[j] < end and j < len(date)-1:
        j += 1
    date = date[i:j]
    date_rev = date[::-1]
    pressure_offset = pressure_offset[i:j]
    pressure_offset_range = pressure_offset_range[i:j]
    pressure_offset_max = [x + y for x, y in zip(pressure_offset, pressure_offset_range)]
    pressure_offset_min = [x - y for x, y in zip(pressure_offset, pressure_offset_range)]
    pressure_offset_min_rev = pressure_offset_min[::-1]

    # Add battery values to the graph
    pressure_offset_line = graph.Scatter(x=date,
                                         y=pressure_offset,
                                         name="pressure offset",
                                         line=dict(color='blue',
                                                   width=2),
                                         mode='lines+markers')

    pressure_offset_range = graph.Scatter(x=date + date_rev,
                                          y=pressure_offset_max + pressure_offset_min_rev,
                                          fill='toself',
                                          fillcolor='rgba(0,0,256,0.2)',
                                          name="range",
                                          line=dict(color='rgba(0, 0, 0, 0)'),
                                          showlegend=False)

    data = [pressure_offset_line, pressure_offset_range]

    layout = graph.Layout(title="External pressure offset in \"" + vital_file_name + "\"",
                          xaxis=dict(title='Coordinated Universal Time (UTC)', titlefont=dict(size=18)),
                          yaxis=dict(title='Pressure offset (millibars)', titlefont=dict(size=18)),
                          hovermode='closest'
                          )

    plotly.plot({'data': data, 'layout': layout},
                filename=os.path.join(os.path.dirname(os.path.dirname(vital_file_path)), "processed/",  "external_pressure_offset.html"),
                auto_open=False)
