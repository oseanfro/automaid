from obspy.core.stream import Stream
from obspy.core.trace import Trace
from obspy.core.trace import Stats
import plotly.graph_objs as graph
import plotly.offline as plotly
import numpy
from obspy import UTCDateTime


def invert_raw():

    ######################################
    # Binary
    ######################################

    #filename = "tool_invert_raw/2019-03-19T10_09_00.349517"
    #date = UTCDateTime("2019-03-19T10:09:00.349517")

    #filename = "tool_invert_raw/2019-03-19T12_26_56.134613"
    #date = UTCDateTime("2019-03-19T12:26:56.134613")

    #filename = "tool_invert_raw/2019-03-19T14_23_20.733093"
    #date = UTCDateTime("2019-03-19T14:23:20.733093")

    # binary
    #rawdata = numpy.fromfile(filename, numpy.int32)


    ######################################
    # Text
    ######################################

    filename = "tool_invert_raw/1553771378.490936"
    date = UTCDateTime(1553771378.490936)
    # text
    f = open(filename, 'r')
    rawdata = numpy.array(f.read().rstrip('\n').split('\n'))
    f.close()


    ######################################
    # Sampling frequency
    ######################################
    # 40.
    fs = 40.014332


    ######################################
    # Plot plotly file
    ######################################

    # Add acoustic values to the graph
    data_line = graph.Scatter(x=[date + i/fs for i in range(0,len(rawdata))],
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
    stats.sampling_rate = fs
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


