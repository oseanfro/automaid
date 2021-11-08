from obspy.core.stream import Stream
from obspy.core.trace import Trace
from obspy.core.trace import Stats
import plotly.graph_objs as graph
import plotly.offline as plotly
import numpy
import glob
import re
import sys
from obspy import UTCDateTime


######################################
# Configuration
######################################

file_path = "tool_invert_raw/"
sampling_file = "tool_invert_raw/2021-05-21_freq"
mode = "Binary"

######################################
# Sampling frequency
######################################
sampling_freq = 40.000000

def invert_raw():
    ######################################
    # Binary
    ######################################
    if mode == "Binary":
        catch_files = []
        files = glob.glob(file_path + "*")
        for file in files :
            catch = re.findall(".*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}_[0-9]{2}_[0-9]{2}\.[0-9]{6}",file)
            if len(catch) > 0 :
                catch_files.append(file)

        ######################################
        # Freq file
        ######################################
        freq_file = glob.glob(file_path + "*_freq")
        if len(freq_file) > 1 :
            print("warning : more than one freq file in folder")
        if len(freq_file) == 0 :
            print(("warning no freq file discovered use :" + str(sampling_freq)))
        else :
            content = "40.000000"
            with open(freq_file[0], "r") as f:
                content = f.read()
            sampling_freq = float(content)
            print(("Sampling used : " + str(sampling_freq)))
        files_nb = len(catch_files)
        file_offset = 1
        for catch_file in catch_files :
            print(catch_file)
            print(("File nb : " + str(file_offset) + "/" + str(files_nb)))
            date = UTCDateTime(re.findall(".*([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}_[0-9]{2}_[0-9]{2}\.[0-9]{6})",catch_file)[0])
            rawdata = numpy.fromfile(catch_file, numpy.int32)
            ######################################
            # Plot plotly file
            ######################################
            # Add acoustic values to the graph
            #data_line = graph.Scattergl(x=[date + i/sampling_freq for i in range(0,len(rawdata))],
            #                          y=rawdata,
            #                          name="counts",
            #                          line=dict(color='blue', width=2),
            #                          mode='lines')

            #plotlydata = [data_line]

            #layout = graph.Layout(title="Plot",
            #                      xaxis=dict(title='Date', titlefont=dict(size=18)),
            #                      yaxis=dict(title='Counts', titlefont=dict(size=18)),
            #                      hovermode='closest'
            #                      )

            #plotly.plot({'data': plotlydata, 'layout': layout},
            #            filename=catch_file + ".html",
            #            auto_open=False)


            ######################################
            # Create SAC file
            ######################################

            # Fill header info
            stats = Stats()
            stats.sampling_rate = sampling_freq
            stats.network = "test"
            stats.station = 0
            stats.starttime = date
            stats.sac = dict()

            # Save data into a Stream object
            trace = Trace()
            trace.stats = stats
            trace.data = rawdata
            stream = Stream(traces=[trace])

            # Save stream object
            stream.write(catch_file + ".sac", format='SAC')
            stream.write(catch_file + ".mseed", format='MSEED')
            stream.write(catch_file + ".wav", format='WAV', framerate=sampling_freq)
            file_offset = file_offset + 1
    else :
        ######################################
        # Text
        ######################################
        #filename = "tool_invert_raw/1553771378.490936"
        #date = UTCDateTime(1553771378.490936)
        # text
        #f = open(filename, 'r')
        #rawdata = numpy.array(f.read().rstrip('\n').split('\n'))
        #f.close()
        # binary
        ######################################
        # Plot plotly file
        ######################################

        # Add acoustic values to the graph
        data_line = graph.Scattergl(x=[date + i/sampling_freq for i in range(0,len(rawdata))],
                                  y=rawdata,
                                  name="counts",
                                  line=dict(color='blue', width=2),
                                  mode='lines')

        plotlydata = [data_line]

        layout = graph.Layout(title="Plot",
                              xaxis=dict(title='Date', titlefont=dict(size=18)),
                              yaxis=dict(title='Counts', titlefont=dict(size=18)),
                              hovermode='closest'
                              )

        plotly.plot({'data': plotlydata, 'layout': layout},
                    filename=filename + ".html",
                    auto_open=False)


        ######################################
        # Create SAC file
        ######################################

        # Fill header info
        stats = Stats()
        stats.sampling_rate = sampling_freq
        stats.network = "test"
        stats.station = 0
        stats.starttime = date
        stats.sac = dict()

        # Save data into a Stream object
        trace = Trace()
        trace.stats = stats
        trace.data = rawdata
        stream = Stream(traces=[trace])

        # Save stream object
        stream.write(filename + ".sac", format='SAC')




if __name__ == "__main__":
    invert_raw()
