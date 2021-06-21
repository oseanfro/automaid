import os
import glob
import re
import subprocess
import numpy
from obspy import UTCDateTime
from obspy.core.stream import Stream
from obspy.core.trace import Trace
from obspy.core.trace import Stats
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print "no display found. Using non-interactive Agg backend"
    mpl.use('agg',warn=False, force=True)
import matplotlib.pyplot as plt
import plotly.graph_objs as graph
import plotly.offline as plotly
import utils
import gps


class Events:
    events = None

    def __init__(self, base_path=None):
        # Initialize event list (if list is declared above, then elements of the previous instance are kept in memory)
        self.events = list()
        # Read all Mermaid files and find events associated to the dive
        mer_files = glob.glob(base_path + "*.MER")
        for mer_file in mer_files:
            file_name = mer_file.split("/")[-1]
            with open(mer_file, "r") as f:
                content = f.read()
            events = content.split("</PARAMETERS>")[-1].split("<EVENT>")[1:]
            for event in events:
                # Divide header and binary
                header = event.split("<DATA>\x0A\x0D")[0]
                binary = event.split("<DATA>\x0A\x0D")[1].split("\x0A\x0D\x09</DATA>")[0]
                self.events.append(Event(file_name, header, binary))

    def get_events_between(self, begin, end):
        catched_events = list()
        for event in self.events:
            if begin < event.date < end:
                catched_events.append(event)
        return catched_events


class Event:
    file_name = None
    environment = None
    header = None
    binary = None
    data = None
    dataMax = None
    dataMin = None
    date = None
    measured_fs = None   # Measured sampling frequency
    decimated_fs = None  # Sampling frequency of the received data
    trig = None
    depth = None
    temperature = None
    criterion = None
    snr = None
    requested = None
    station_loc = None
    drift_correction = None
    stanford_rounds = None
    stanford_duration = None
    stanford_period = None
    stanford_win_len = None
    stanford_win_type = None
    stanford_overlap = None
    stanford_db_offset = None

    def __init__(self, file_name, header, binary):
        self.file_name = file_name
        self.header = header
        self.binary = binary

        if len(re.findall(" ROUNDS=(-?\d+)", self.header)) > 0 :
            self.stanford_rounds = re.findall(" ROUNDS=(-?\d+)", self.header)[0]
            date = re.findall(" DATE=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})", header, re.DOTALL)
            self.date = UTCDateTime.strptime(date[0], "%Y-%m-%dT%H:%M:%S.%f")
            self.requested = False
            #if len(re.findall("FNAME=(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d{6})", self.header)) > 0 :
                #self.requested = True
        else :
            if len(re.findall(" STAGES=(-?\d+)", self.header)) > 0 :
                self.scales = re.findall(" STAGES=(-?\d+)", self.header)[0]
            catch_trig = re.findall(" TRIG=(\d+)", self.header)
            if len(catch_trig) > 0:
                # Event detected with STA/LTA algorithm
                self.requested = False
                self.trig = int(catch_trig[0])
                date = re.findall(" DATE=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})", header, re.DOTALL)
                try:
                    self.date = UTCDateTime.strptime(date[0], "%Y-%m-%dT%H:%M:%S.%f")
                except IndexError as e:
                    date = re.findall(" DATE=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", header, re.DOTALL)
                    self.date = UTCDateTime.strptime(date[0], "%Y-%m-%dT%H:%M:%S")
                self.depth = int(re.findall(" PRESSURE=(-?\d+)", self.header)[0])
                self.temperature = int(re.findall(" TEMPERATURE=(-?\d+)", self.header)[0])
                self.criterion = float(re.findall(" CRITERION=(\d+\.\d+)", self.header)[0])
                self.snr = float(re.findall(" SNR=(\d+\.\d+)", self.header)[0])
            else:
                # Event requested by user
                self.requested = True
                date = re.findall(" DATE=(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", header, re.DOTALL)
                self.date = UTCDateTime.strptime(date[0], "%Y-%m-%dT%H:%M:%S")

    def set_environment(self, environment):
        self.environment = environment
        duration = re.findall("DURATION_h=(\d+)", self.environment)
        if len(duration) > 0 :
            self.stanford_duration = duration[0]
        else :
            self.stanford_duration = ""
        period = re.findall("PROCESS_PERIOD_h=(\d+)", self.environment)
        if len(duration) > 0 :
            self.stanford_period = period[0]
        else :
            self.stanford_period = ""
        win_len = re.findall("WINDOW_LEN=(\d+)", self.environment)
        if len(duration) > 0 :
            self.stanford_win_len = win_len[0]
        else :
            self.stanford_win_len = ""
        win_type = re.findall("WINDOW_TYPE=(\w+)", self.environment)
        if len(duration) > 0 :
            self.stanford_win_type = win_type[0]
        else :
            self.stanford_win_type = ""
        overlap = re.findall("OVERLAP_PERCENT=(\d+)", self.environment)
        if len(duration) > 0 :
            self.stanford_overlap = overlap[0]
        else :
            self.stanford_overlap = ""
        db_offset = re.findall("dB_OFFSET=(\d+)", self.environment)
        if len(duration) > 0 :
            self.stanford_db_offset = db_offset[0]
        else :
            self.stanford_db_offset = ""
    def is_stanford_event(self):
        if self.stanford_rounds :
            return True
        else :
            return False
    def find_measured_sampling_frequency(self):
        # Get the frequency recorded in the .MER environment header
        fs_catch = re.findall("TRUE_SAMPLE_FREQ FS_Hz=(\d+\.\d+)", self.environment)
        if (fs_catch):
            self.measured_fs = float(fs_catch[0])
        else:
            self.measured_fs = 40
        print "MEASURE_FS="+str(self.measured_fs)

        # Divide frequency by number of scales
        if not self.is_stanford_event() :
            int_scl = int(self.scales)
            if int_scl >= 0:
                self.decimated_fs = self.measured_fs / (2. ** (6 - int_scl))
            else:
                self.decimated_fs = self.measured_fs
        else:
            self.decimated_fs = self.measured_fs
        # Else: This is raw data sampled at 40Hz

    def correct_date(self):
        # Calculate the date of the first sample
        if not self.is_stanford_event() :
            if self.requested:
                # For a requested event
                sample_offset = re.findall("SMP_OFFSET=(\d+)", self.header)
                rec_file_date = re.findall("FNAME=(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d{6})", self.header)
                if len(rec_file_date) <= 0 :
                    rec_file_date = re.findall("FNAME=(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2})", self.header)
                    rec_file_date = UTCDateTime.strptime(rec_file_date[0], "%Y-%m-%dT%H_%M_%S")
                else:
                    rec_file_date = UTCDateTime.strptime(rec_file_date[0], "%Y-%m-%dT%H_%M_%S.%f")
                sample_offset = float(sample_offset[0])
                self.date = rec_file_date + sample_offset/self.measured_fs
            else:
                # For a detected event
                # The recorded date is the STA/LTA trigger date, subtract the time before the trigger.
                self.date = self.date - float(self.trig) / self.decimated_fs

    def correct_clock_drift(self, gps_descent, gps_ascent):
        # Correct the clock drift of the Mermaid board with GPS measurement
        pct = (self.date - gps_descent.date) / (gps_ascent.date - gps_descent.date)
        self.drift_correction = gps_ascent.clockdrift * pct
        # Apply correction
        self.date = self.date + self.drift_correction

    def compute_station_location(self, drift_begin_gps, drift_end_gps):
        self.station_loc = gps.linear_interpolation([drift_begin_gps, drift_end_gps], self.date)

    def extract_stanford_data(self):
        self.data = numpy.frombuffer(self.binary, numpy.int8)

    def invert_transform(self):
        # If scales == -1 this is a raw signal, just convert binary data to numpy array of int32
        if self.scales == "-1":
            self.data = numpy.frombuffer(self.binary, numpy.int32)
            self.dataMax = numpy.amax(self.data)
            self.dataMin = numpy.amin(self.data)
            return
        # Get additional information to invert wavelet
        normalized = re.findall(" NORMALIZED=(\d+)", self.environment)[0]
        edge_correction = re.findall(" EDGES_CORRECTION=(\d+)", self.environment)[0]
        # Write cdf24 data
        automaid_dir = os.path.dirname(__file__)
        wtcoeffsname = os.path.join(automaid_dir, 'bin/wtcoeffs')
        icdf24_v103ec_test = os.path.join(automaid_dir, 'bin/icdf24_v103ec_test')
        icdf24_v103_test = os.path.join(automaid_dir, 'bin/icdf24_v103_test')
        icdf24_data = os.path.join(automaid_dir, "bin/wtcoeffs.icdf24_" + self.scales)
        with open(wtcoeffsname, 'w') as f:
            f.write(self.binary)
        # Do icd24
        if edge_correction == "1":
            print "icdf24_v103ec_test"
            subprocess.check_output([icdf24_v103ec_test,
                                     self.scales,
                                     normalized,
                                     wtcoeffsname])
        else:
            print "icdf24_v103_test"
            subprocess.check_output([icdf24_v103_test,
                                    self.scales,
                                    normalized,
                                    wtcoeffsname])
        # Read icd24 data
        self.data = numpy.fromfile(icdf24_data, numpy.int32)
        self.dataMax = numpy.amax(self.data)
        self.dataMin = numpy.amin(self.data)

    def get_export_file_name(self):
        export_file_name = UTCDateTime.strftime(UTCDateTime(self.date), "%Y%m%dT%H%M%S") + "." + self.file_name
        if self.is_stanford_event() :
            export_file_name = export_file_name + ".STD"
        else :
            if not self.trig:
                export_file_name = export_file_name + ".REQ"
            else:
                export_file_name = export_file_name + ".DET"
            if self.scales == "-1":
                export_file_name = export_file_name + ".RAW"
            else:
                export_file_name = export_file_name + ".WLT" + self.scales
        return export_file_name

    def statistics(self):
        return [UTCDateTime.strftime(UTCDateTime(self.date), "%Y%m%dT%H%M%S"),self.dataMax, self.dataMin]

    def __get_figure_title(self):
        title = "" + self.date.isoformat() \
                + "     Fs = " + str(self.decimated_fs) + "Hz\n" \
                + "     Depth: " + str(self.depth) + " m\n" \
                + "     Temperature: " + str(self.temperature) + " degC\n" \
                + "     Criterion = " + str(self.criterion) \
                + "     SNR = " + str(self.snr)
        return title
    def __get_figure_title_stanford_html(self):
        title = "" + self.date.isoformat() \
                + "<br> Fs = " + str(self.decimated_fs) + "Hz" \
                + "     DURATION = " + str(self.stanford_duration) + "h" \
                + "     PROCESS_PERIOD = " + str(self.stanford_period) + "h" \
                + "     WINDOW_LEN = " + str(self.stanford_win_len) \
                + "<br> WINDOW_TYPE = " + str(self.stanford_win_type) \
                + "     OVERLAP_PERCENT = " + str(self.stanford_overlap) \
                + "     dB_OFFSET = " + str(self.stanford_db_offset) + "db"
        return title
    def __get_figure_title_stanford(self):
        title = "" + self.date.isoformat() \
                + "\n Fs = " + str(self.decimated_fs) + "Hz" \
                + "     DURATION = " + str(self.stanford_duration) + "h" \
                + "     PROCESS_PERIOD = " + str(self.stanford_period) + "h" \
                + "     WINDOW_LEN = " + str(self.stanford_win_len) \
                + "\n WINDOW_TYPE = " + str(self.stanford_win_type) \
                + "     OVERLAP_PERCENT = " + str(self.stanford_overlap) \
                + "     dB_OFFSET = " + str(self.stanford_db_offset) + "db"
        return title

    def plotly(self, export_path):
        # Check if file exist
        export_path = export_path + self.get_export_file_name() + ".html"
        if os.path.exists(export_path):
            return
        # Add acoustic values to the graph
        data_line = graph.Scatter(x=utils.get_date_array(self.date, len(self.data), 1./self.decimated_fs),
                                  y=self.data,
                                  name="counts",
                                  line=dict(color='blue',
                                            width=2),
                                  mode='lines')

        data = [data_line]

        layout = graph.Layout(title=self.__get_figure_title(),
                              xaxis=dict(title='Coordinated Universal Time (UTC)', titlefont=dict(size=18)),
                              yaxis=dict(title='Counts', titlefont=dict(size=18)),
                              hovermode='closest'
                              )

        plotly.plot({'data': data, 'layout': layout},
                    filename=export_path,
                    auto_open=False)
    def plotly_stanford(self, export_path):
        # Check if file exist
        export_path = export_path + self.get_export_file_name() + ".html"
        print export_path
        if os.path.exists(export_path):
            return
        win_sz = re.findall("WINDOW_LEN=(\d+)", self.environment, re.DOTALL)
        dt = numpy.dtype([('perc50', numpy.int8)])
        x_split = numpy.array_split(self.data,2)
        x0=x_split[0]
        x1=x_split[1]
        freq_max=(float)((x0.size*40)/int(win_sz[0]))
        freq = numpy.arange(0.,freq_max,freq_max/x0.size)
        # Add acoustic values to the graph
        x0_line = graph.Scatter(x=freq,
                                  y=x0,
                                  name="Percentil 50",
                                  line=dict(color='blue',
                                            width=2),
                                  mode='lines')
        x1_line = graph.Scatter(x=freq,
                                  y=x1,
                                  name="Percentil 95",
                                  line=dict(color='red',
                                            width=2),
                                  mode='lines')

        data = [x0_line,x1_line]

        layout = graph.Layout(title=self.__get_figure_title_stanford_html(),
                              xaxis=dict(title='Freq (Hz)', titlefont=dict(size=18), type='log'),
                              yaxis=dict(title='dBfs^2/Hz', titlefont=dict(size=18)),
                              hovermode='closest'
                              )

        plotly.plot({'data': data, 'layout': layout},
                    filename=export_path,
                    auto_open=False)

    def plot(self, export_path):
        # Check if file exist
        export_path = export_path + self.get_export_file_name() + ".png"
        if os.path.exists(export_path):
            return
        # Plot frequency image
        plt.figure(figsize=(9, 4))
        plt.title(self.__get_figure_title(), fontsize=12)
        plt.plot(utils.get_time_array(len(self.data), 1./self.decimated_fs),
                 self.data,
                 color='b')
        plt.xlabel("Time (s)", fontsize=12)
        plt.ylabel("Counts", fontsize=12)
        plt.tight_layout()
        plt.grid()
        plt.savefig(export_path)
        plt.clf()
        plt.close()

    def plot_stanford(self, export_path):
        # Check if file exist
        export_path = export_path + self.get_export_file_name() + ".png"
        print export_path
        if os.path.exists(export_path):
            return
        win_sz = re.findall("WINDOW_LEN=(\d+)", self.environment, re.DOTALL)
        dt = numpy.dtype([('perc50', numpy.int8)])
        x_split = numpy.array_split(self.data,2)
        x0=x_split[0]
        x1=x_split[1]
        freq_max=(float)((x0.size*40)/int(win_sz[0]))
        freq = numpy.arange(0.,freq_max,(freq_max/x0.size))
        # Plot frequency image
        plt.figure(figsize=(9, 4))
        plt.title(self.__get_figure_title_stanford(), fontsize=12)
        plt.plot(freq,x0,color='b')
        plt.plot(freq,x1,color='r')
        plt.xlabel("Freq (Hz)", fontsize=12)
        plt.ylabel("dBfs^2/Hz", fontsize=12)
        plt.xscale("log")
        plt.tight_layout()
        plt.grid()
        plt.savefig(export_path)
        plt.clf()
        plt.close()

    def to_sac_and_mseed(self, export_path, station_number, force_without_loc):
        # Check if file exist
        export_path_sac = export_path + self.get_export_file_name() + ".sac"
        export_path_msd = export_path + self.get_export_file_name() + ".mseed"
        export_path_wav = export_path + self.get_export_file_name() + ".wav"
        if os.path.exists(export_path_sac) and os.path.exists(export_path_msd):
            return

        # Check if the station location have been calculated
        if self.station_loc is None and not force_without_loc:
            print self.get_export_file_name() + ": Skip sac/mseed generation, wait the next ascent to compute location"
            return

        # Fill header info
        stats = Stats()
        stats.sampling_rate = self.decimated_fs
        stats.network = "MH"
        stats.station = station_number
        stats.starttime = self.date

        stats.sac = dict()
        if not force_without_loc:
            stats.sac["stla"] = self.station_loc.latitude
            stats.sac["stlo"] = self.station_loc.longitude
        stats.sac["stdp"] = self.depth
        stats.sac["user0"] = self.snr
        stats.sac["user1"] = self.criterion
        stats.sac["iztype"] = 9  # 9 == IB in sac format

        # Save data into a Stream object
        trace = Trace()
        trace.stats = stats
        trace.data = self.data
        stream = Stream(traces=[trace])

        # Save stream object
        stream.write(export_path_sac, format='SAC')
        stream.write(export_path_msd, format='MSEED')
        #stream.write(export_path_wav, format='WAV', framerate=self.decimated_fs)
