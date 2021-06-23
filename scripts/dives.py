import glob
import os
import csv
import re
import profile
import plotly.graph_objs as graph
import plotly.offline as plotly
import utils
from obspy import UTCDateTime
import traceback
import gps
import configuration


# Log class to manipulate log files
class Dive:
    log_name = None
    base_path = None
    directory_name = None
    export_path = None
    date = None
    end_date = None
    is_init = None
    is_dive = None
    is_complete_dive = None
    log_content = None
    mmd_name = None
    mmd_environment = None
    profiles = None
    s41_name = None
    s41_environment = None
    s41_start = None
    events = None
    station_name = None
    cycle_nb = None
    soft_version = None
    station_number = None
    gps_list = None
    gps_list_is_complete = None
    surface_leave_loc = None
    surface_reach_loc = None
    great_depth_reach_loc = None
    great_depth_leave_loc = None

    def __init__(self, base_path, log_name, events, profiles):
        self.base_path = base_path
        self.log_name = log_name

        # Get the date from the file name
        self.date = utils.get_date_from_file_name(log_name)

        # Read the content of the LOG
        with open(self.base_path + self.log_name, "r") as f:
            self.log_content = f.read()

        # Get the last date
        ed = re.findall("(\d+):", utils.split_log_lines(self.log_content)[-1])[0]
        self.end_date = UTCDateTime(int(ed))

        # Check if the log correspond to the float initialization
        self.is_init = False
        match = re.search("\[TESTMD,\d{3}\]\"yes\"", self.log_content)
        if "Enter in test mode?" in self.log_content and not match:
            self.is_init = True

        # Check if the log correspond to a dive
        self.is_dive = False
        if "[DIVING," in self.log_content:
            self.is_dive = True

        # Check if the log correspond to a complete dive
        self.is_complete_dive = False
        if self.is_dive:
            catch = utils.find_timestamped_values("\[MAIN *, *\d+\]surface", self.log_content)
            if len(catch) > 0:
                self.is_complete_dive = True

        # Generate the directory name
        self.directory_name = self.date.strftime("%Y%m%d-%Hh%Mm%Ss")
        if self.is_init:
            self.directory_name += "Init"
        elif not self.is_dive:
            self.directory_name += "NoDive"
        elif not self.is_complete_dive:
            self.directory_name += "IcDive"

        self.export_path = os.path.join(os.path.dirname(os.path.dirname(self.base_path)), "processed", self.directory_name) + "/"

        # Get the station name
        if self.is_dive or self.is_init:
            self.station_name = []
            self.soft_version = []
            self.cycle_nb = []
            log_splitted = utils.split_log_lines(self.log_content)
            for line in log_splitted:
                if len(self.station_name) == 0 :
                    self.station_name = re.findall("board (.+)", line)
                    if len(self.station_name) == 0:
                        self.station_name = re.findall("buoy (.+)", line)
                if len(self.soft_version) == 0 :
                    self.soft_version = re.findall("soft \w* ?\d{3}\.\d{3}\.\d{3}[\.]?[_]?[V]?(.+)",line)
                if len(self.cycle_nb) == 0 :
                    self.cycle_nb = re.findall("cycle (\d+)", line)
                if (len(self.station_name) > 0) and (len(self.soft_version) > 0) and (len(self.cycle_nb) > 0):
                    self.station_name = self.station_name[0]
                    self.cycle_nb = self.cycle_nb[0]
                    self.soft_version = self.soft_version[0]
                    self.station_number = self.station_name.split("-")[-1]
                    break


        print(self.station_name)
        print(self.soft_version)
        print(self.cycle_nb)
        # Find the .MER file of the ascent
        catch = re.findall("bytes in (\w+/\w+\.MER)", self.log_content)
        if len(catch) > 0:
            self.mmd_name = catch[-1].replace("/", "_")

        # If the dive contain a Mermaid file
        self.events = list()
        if self.mmd_name:
            try:
                # Read the Mermaid environment associated to the dive
                with open(self.base_path + self.mmd_name, "rb") as f:
                    content = f.read()
            except IOError:
                print(("manque le fichier " + self.mmd_name))
                self.mmd_name = None
                self.events = []
            else:
                header = content.split(b'</PARAMETERS>')[0].decode("utf-8")
                self.mmd_environment = re.findall("<ENVIRONMENT>.+", header, re.DOTALL)[0]
                # Get list of events associated to the dive
                self.events = events.get_events_between(self.date, self.end_date)
                # For each event
                for event in self.events:
                    # 1 Set the environment information
                    event.set_environment(self.mmd_environment)
                    # 2 Find true sampling frequency
                    event.find_measured_sampling_frequency()
                    if event.is_stanford_event() :
                        # 3 Extract stanford data
                        event.extract_stanford_data()
                    else:
                        # 3 Correct events date
                        event.correct_date()
                        # 4 Invert wavelet transform of event
                        event.invert_transform()


        # Find the .S41 file of the ascent
        catch = re.findall("bytes in (\w+/\w+\.S41)", self.log_content)
        if len(catch) > 0:
            self.s41_name = catch[-1].replace("/", "_")
        # If the dive contain a Mermaid file
        self.profiles = list()
        if self.s41_name:
            try:
                # Read the Mermaid environment associated to the dive
                with open(self.base_path + self.s41_name, "r", encoding='latin1') as f:
                    content = f.read()
            except IOError:
                print(("manque le fichier " + self.s41_name))
                self.s41_name = None
            else:
                self.s41_environment = re.findall("<PARAMETERS>.+</PILOTS>", content, re.DOTALL)[0]
                self.profiles = profiles.get_profiles_between(self.date, self.end_date)
                s41_date = utils.find_timestamped_values("\[SBE41 *, *\d+\]Speed start detected", self.log_content)
                if len(s41_date) == len(self.profiles):
                    index = 0
                    for profile in self.profiles :
                        profile.start_date = s41_date[index][1]
                        index = index + 1
        # Find the position of the float
        self.gps_list = gps.get_gps_list(self.log_content, self.mmd_environment, self.mmd_name)
        self.gps_list_is_complete = False
        if self.is_complete_dive:
            # Check that the last GPS fix of the list correspond to the ascent position
            surface_date = utils.find_timestamped_values("\[MAIN *, *\d+\]surface", self.log_content)
            surface_date = UTCDateTime(surface_date[0][1])
            if len(self.gps_list) == 0:
                print(("WARNING: No GPS synchronization at all for \"" \
                    + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            elif len(self.gps_list) > 1 and self.gps_list[-1].date > surface_date:
                self.gps_list_is_complete = True
            elif self.gps_list[-1].date > surface_date:
                print(("WARNING: No GPS synchronization before diving for \"" \
                    + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            else:
                print(("WARNING: No GPS synchronization after surfacing for \"" \
                    + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))

    def generateJSON(self):
        json_object = {}
        json_object["log_name"] = self.log_name
        json_object["base_path"] = self.base_path
        json_object["export_path"] = self.export_path
        json_object["date"] = str(self.date)
        json_object["end_date"] = str(self.end_date)
        json_object["is_init"] = self.is_init
        json_object["is_dive"] = self.is_dive
        json_object["is_complete_dive"] = self.is_complete_dive
        json_object["mmd_name"] = self.mmd_name
        json_object["station_name"] = self.station_name
        json_object["station_number"] = self.station_number
        json_object["gps_list_is_complete"] = self.gps_list_is_complete
        json_object["surface_leave_loc"] = self.surface_leave_loc
        json_object["surface_reach_loc"] = self.surface_reach_loc
        json_object["great_depth_reach_loc"] = self.great_depth_reach_loc
        json_object["great_depth_leave_loc"] = self.great_depth_leave_loc
        return json_object

    def generate_datetime_log(self):
        # Check if file exist
        export_path = self.export_path + self.log_name + ".h"
        export_path_md5 = self.export_path + self.log_name + ".md5"

        md5Current = utils.get_md5_from_string(self.log_content)
        md5Old = ""
        if os.path.exists(export_path_md5) and os.path.exists(export_path):
            with open(export_path_md5, "r") as f:
                md5Old = f.read()
            if md5Current == md5Old:
                print(md5Current)
                return
        if os.path.exists(export_path_md5) :
            os.remove(export_path_md5)
        if os.path.exists(export_path) :
            os.remove(export_path)
        # Generate log with formatted date
        formatted_log = utils.format_log(self.log_content)
        # Write file
        with open(export_path, "w") as f:
            f.write(formatted_log)
        with open(export_path_md5, mode='w') as md5_file:
            md5_file.write(md5Current)

    def generate_mermaid_environment_file(self):
        # Check if there is a Mermaid file
        if self.mmd_name is None:
            return
        # Check if file exist
        export_path = self.export_path + self.log_name + "." + self.mmd_name + ".env"
        export_path_md5 = self.export_path + self.log_name + "." + self.mmd_name + ".md5"

        md5Current = utils.get_md5_from_string(self.mmd_environment)
        md5Old = ""
        if os.path.exists(export_path_md5) and os.path.exists(export_path):
            with open(export_path_md5, "r") as f:
                md5Old = f.read()
            if md5Current == md5Old:
                print(md5Current)
                return
        if os.path.exists(export_path_md5) :
            os.remove(export_path_md5)
        if os.path.exists(export_path) :
            os.remove(export_path)
        # Write file
        with open(export_path, "w") as f:
            f.write(self.mmd_environment)
        with open(export_path_md5, mode='w') as md5_file:
            md5_file.write(md5Current)

    def generate_s41_environment_file(self):
        # Check if there is a Mermaid file
        if self.s41_name is None:
            return
        # Check if file exist
        export_path = self.export_path + self.log_name + "." + self.s41_name + ".params"
        export_path_md5 = self.export_path + self.log_name + "." + self.s41_name + ".md5"

        md5Current = utils.get_md5_from_string(self.s41_environment)
        md5Old = ""
        if os.path.exists(export_path_md5) and os.path.exists(export_path):
            with open(export_path_md5, "r") as f:
                md5Old = f.read()
            if md5Current == md5Old:
                print(md5Current)
                return
        if os.path.exists(export_path_md5) :
            os.remove(export_path_md5)
        if os.path.exists(export_path) :
            os.remove(export_path)
        # Write file
        with open(export_path, "w") as f:
            f.write(self.s41_environment)
        with open(export_path_md5, mode='w') as md5_file:
            md5_file.write(md5Current)

    def generate_dive_plotly(self, csv_file):
        # If the float is not diving don't plot anything
        if not self.is_dive:
            return
        # Check if data are same
        export_path = self.export_path + self.log_name[:-4] + '.html'
        export_path_md5 = self.export_path + self.log_name[:-4] + ".md5"

        md5Current = utils.get_md5_from_string(self.log_content)
        md5Old = ""
        if os.path.exists(export_path_md5) and os.path.exists(export_path):
            with open(export_path_md5, "r") as f:
                md5Old = f.read()
            if md5Current == md5Old:
                print(md5Current)
                return
        if os.path.exists(export_path_md5) :
            os.remove(export_path_md5)
        if os.path.exists(export_path) :
            os.remove(export_path)
        print(export_path)
        # Search pressure values
        pressure = utils.find_timestamped_values(
            "]P\s*(\+?\-?\d+)mbar", self.log_content)
        bypass = utils.find_timestamped_values(
            ":\[BYPASS.+\].*opening.*[0-9]+ms", self.log_content)
        valve = utils.find_timestamped_values(
            ":\[VALVE.+\].*opening.*[0-9]+ms", self.log_content)
        pump = utils.find_timestamped_values(
            ":\[PUMP.+\].*during.*[0-9]+ms", self.log_content)
        mermaid_events = utils.find_timestamped_values(
            "[MRMAID,\d+] *\d+dbar, *-?\d+degC", self.log_content)
        # Return if there is no data to plot
        if len(pressure) < 1:
            return
        # Add pressure values to the graph
        p_val = [-int(p[0]) / 100. for p in pressure]
        p_date = [p[1] for p in pressure]
        depth_line = graph.Scatter(x=p_date,
                                   y=p_val,
                                   name="depth",
                                   line=dict(color='#474747',
                                             width=2),
                                   mode='lines+markers')
        if csv_file:
            p_date_format = [UTCDateTime.strftime(UTCDateTime(date), "%Y%m%dT%H%M%S") for date in p_date]
            csv_path = export_path.replace(".html",".csv")
            rows = list(zip(p_date_format,p_val))
            with open(csv_path, mode='w') as csv_file:
                csv_file = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    csv_file.writerow(row)

        # Add vertical lines
        # Find minimum and maximum for Y axis of vertical lines
        minimum = min(p_val) + 0.05 * min(p_val)
        maximum = 0

        data = [depth_line]
        if configuration.bypass_ploted :
            # Add bypass lines
            bypass = [bp[1] for bp in bypass]
            bypass_line = utils.plotly_vertical_shape(bypass,
                                                      ymin=minimum,
                                                      ymax=maximum,
                                                      name="bypass",
                                                      color="blue")
            data.append(bypass_line)
        if configuration.valve_ploted :
            # Add valve lines
            valve = [vv[1] for vv in valve]
            valve_line = utils.plotly_vertical_shape(valve,
                                                     ymin=minimum,
                                                     ymax=maximum,
                                                     name="valve",
                                                     color="green")
            data.append(valve_line)
        if configuration.pump_ploted :
            # Add pump lines
            pump = [pp[1] for pp in pump]
            pump_line = utils.plotly_vertical_shape(pump,
                                                    ymin=minimum,
                                                    ymax=maximum,
                                                    name="pump",
                                                    color="orange")
            data.append(pump_line)

        if configuration.mermaid_ploted :
            # Add mermaid events lines
            mermaid_events = [pp[1] for pp in mermaid_events]
            mermaid_events_line = utils.plotly_vertical_shape(mermaid_events,
                                                              ymin=minimum,
                                                              ymax=maximum,
                                                              name="MERMAID events",
                                                              color="purple")
            data.append(mermaid_events_line)

        layout = graph.Layout(title=self.directory_name + '/' + self.log_name,
                              xaxis=dict(
                                  title='Coordinated Universal Time (UTC)', titlefont=dict(size=18)),
                              yaxis=dict(title='Depth (meters)',
                                         titlefont=dict(size=18)),
                              hovermode='closest'
                              )

        plotly.plot({'data': data, 'layout': layout},
                    filename=export_path,
                    auto_open=False)

        with open(export_path_md5, mode='w') as md5_file:
            md5_file.write(md5Current)

    def correct_events_clock_drift(self):
        # Return if there is no events
        if len(self.events) == 0:
            return

        # Compute clock drift
        if not self.is_dive:
            # print "WARNING: Events are not part of a dive, don't do clock drift correction for \""\
            #       + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""
            return
        if not self.is_complete_dive:
            print(("WARNING: Events are not part of a complete dive, do not correct clock drift for \""\
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return
        if not self.gps_list_is_complete:
            print(("WARNING: GPS list is incomplete, do not correct clock drift for \""\
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return
        if self.gps_list[-2].clockfreq <= 0:
            print(("WARNING: Error with last gps synchronization before diving, do not correct clock drift for \""\
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return
        if self.gps_list[-1].clockfreq <= 0:
            print(("WARNING: Error with first gps synchronization after ascent, do not correct clock drift for \""\
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return

        # Correct clock drift
        for event in self.events:
            event.correct_clock_drift(self.gps_list[-2], self.gps_list[-1])

    def compute_events_station_location(self, next_dive):
        # Check if the dive is complete
        if not self.is_complete_dive:
            # print "WARNING: The dive is not complete, do not compute event location estimation for \""\
            #       + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""
            return

        # Check if the dive contain enough gps fix
        if len(self.gps_list) <= 1:
            print(("WARNING: The current dive doesn't contain enough GPS fix,""" \
                  + " do not compute event location estimation for \"" \
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return

        # Check if the next dive contain gps fix
        if len(next_dive.gps_list) <= 1:
            print(("WARNING: The next dive doesn't contain enough GPS fix,""" \
                  + " do not compute event location estimation for \"" \
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return

        # Warning GPS list is incomplete, do not compute event location
        if not self.gps_list_is_complete:
            print(("WARNING: GPS list is incomplete, do not compute event location for \""\
                  + str(self.mmd_name) + "\", \"" + str(self.log_name) + "\""))
            return

        # Divide gps in two list
        gps_before_dive = self.gps_list[:-1]
        gps_after_dive = [self.gps_list[-1]] + next_dive.gps_list[:-1]

        # Find location when float leave the surface
        surface_leave_date = utils.find_timestamped_values(
            "\[DIVING, *\d+\] *(\d+)mbar reached", self.log_content)
        surface_leave_date = surface_leave_date[0][1]
        self.surface_leave_loc = gps.linear_interpolation(
            gps_before_dive, surface_leave_date)

        # Find location when float reach the surface
        surface_reach_date = utils.find_timestamped_values(
            "\[SURFIN, *\d+\]filling external bladder", self.log_content)
        surface_reach_date = surface_reach_date[-1][1]
        self.surface_reach_loc = gps.linear_interpolation(
            gps_after_dive, surface_reach_date)

        # Location is determined when the float reach the mixed layer depth
        mixed_layer_depth_m = 50

        # Find pressure values
        pressure = utils.find_timestamped_values(
            "P\s*(\+?\-?\d+)mbar", self.log_content)
        pressure_date = [p[1] for p in pressure]
        pressure_val = [int(p[0]) / 100. for p in pressure]

        # Return if there is the max value doesn't reach the mixed layer depth
        if max(pressure_val) < mixed_layer_depth_m:
            # compute location of events from surface position
            for event in self.events:
                event.compute_station_location(
                    self.surface_leave_loc, self.surface_reach_loc)
            return

        # loop until to reach a depth greater than mixed_layer_depth
        i = 0
        while pressure_val[i] < mixed_layer_depth_m and i < len(pressure_val):
            i += 1
        d2 = pressure_date[i]
        p2 = pressure_val[i]
        if i > 0:
            d1 = pressure_date[i - 1]
            p1 = pressure_val[i - 1]
        else:
            d1 = surface_leave_date
            p1 = 0

        # compute when the float pass under the mixed layer
        reach_great_depth_date = d1 + \
            (mixed_layer_depth_m - p1) * (d2 - d1) / (p2 - p1)

        # loop until to reach a depth higher than mixed_layer_depth bur for in the ascent phase
        i = len(pressure_val) - 1
        while pressure_val[i] < mixed_layer_depth_m and i > 0:
            i -= 1
        d1 = pressure_date[i]
        p1 = pressure_val[i]

        if i < len(pressure_val) - 1:
            d2 = pressure_date[i + 1]
            p2 = pressure_val[i + 1]
        else:
            d2 = surface_reach_date
            p2 = 0

        # compute when the float pass above the mixed layer
        leave_great_depth_date = d1 + \
            (mixed_layer_depth_m - p1) * (d2 - d1) / (p2 - p1)

        # compute location with linear interpolation
        self.great_depth_reach_loc = gps.linear_interpolation(
            gps_before_dive, reach_great_depth_date)
        self.great_depth_leave_loc = gps.linear_interpolation(
            gps_after_dive, leave_great_depth_date)

        # compute location of events
        for event in self.events:
            event.compute_station_location(
                self.great_depth_reach_loc, self.great_depth_leave_loc)

    def generate_events_plotly(self):
        for event in self.events:
            if event.is_stanford_event():
                event.plotly_stanford(self.export_path)
            else :
                event.plotly(self.export_path)

    def generate_profile_plotly(self,csv_file):
        for profile in self.profiles:
            profile.plotly_temperature(self.export_path,csv_file)
            profile.plotly_salinity(self.export_path)

    def generate_events_plot(self):
        for event in self.events:
            if event.is_stanford_event():
                event.plot_stanford(self.export_path)
            else :
                event.plot(self.export_path)

    def generate_events_sac(self):
        for event in self.events:
            if not event.is_stanford_event():
                event.to_sac_and_mseed(self.export_path, self.station_number, force_without_loc=False)

    def get_buoy(self):
        list = self.base_path.split("/")
        return (list[len(list) - 3])


class Dives:
    dives = None
    def __init__(self, path=None, events=None, profiles=None):
        if not path or not events or not profiles:
            return
        log_names = glob.glob(path + "*.LOG")
        if len(log_names) == 0 :
            log_names = glob.glob(path + "*.LOG.h")
        log_names = [x.split("/")[-1] for x in log_names]
        log_names.sort()
        # Create Dive objects
        self.dives = list()
        for log_name in log_names:
            print(log_name)
            try:
                dive = Dive(path, log_name, events, profiles)
            except :
                traceback.print_exc()
                print("wrong format")
            else :
                self.dives.append(dive)
    def get_cycle_nb() :
        cycle_nb = 0
        for dive in self.dives :
            if dive.is_complete_dive :
                cycle_nb = cycle_nb + 1
        return cycle_nb
    def get_position_nb() :
        position_nb = 0
        for dive in self.dives :
            position_nb = position_nb + len(dive.gps_list)
        return position_nb



# Create dives object
def get_dives(path, events, profiles):
    # Get the list of log files
    log_names = glob.glob(path + "*.LOG")
    if len(log_names) == 0 :
        log_names = glob.glob(path + "*.LOG.h")
    log_names = [x.split("/")[-1] for x in log_names]
    log_names.sort()
    # Create Dive objects
    dives = list()
    for log_name in log_names:
        print(log_name)
        try:
            dive = Dive(path, log_name, events, profiles)
        except :
            traceback.print_exc()
            print("wrong format")
        else :
            dives.append(dive)
    return dives


# Concatenate .000 files .LOG files in the path
def concatenate_log_files(path):
    log_files = list()
    extensions = ["000", "001", "002", "003", "004", "005", "LOG"]
    for extension in extensions:
        log_files += glob.glob(path + "*." + extension)
    log_files = [x.split("/")[-1] for x in log_files]
    log_files.sort()

    logstring = ""
    for log_file in log_files:
        # If log extension is a digit, fill the log string
        if log_file[-3:].isdigit():
            with open(path + log_file, "r") as fl:
                # We assume that files are sorted in a correct order
                logstring += fl.read()
            os.remove(path + log_file)
        else:
            if len(logstring) > 0:
                # If log extension is not a digit and the log string is not empty
                # we need to add it at the end of the file
                with open(path + log_file, "r") as fl:
                    logstring += fl.read()
                with open(path + log_file, "w") as fl:
                    fl.write(logstring)
                logstring = ""
