import os
import shutil
import glob
import datetime
import dives
import events
import vitals
import profile
import decrypt
import kml
import re
import utils
#import decrypt

# Set a time range of analysis for a specific float
filterDate = {
    "452.112-N-01": (datetime.datetime(2018, 12, 27), datetime.datetime(2100, 1, 1)),
    "452.112-N-02": (datetime.datetime(2018, 12, 28), datetime.datetime(2100, 1, 1)),
    "452.112-N-03": (datetime.datetime(2018, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.112-N-04": (datetime.datetime(2019, 1, 3), datetime.datetime(2100, 1, 1)),
    "452.112-N-05": (datetime.datetime(2019, 1, 3), datetime.datetime(2100, 1, 1)),
    "452.020-P-06": (datetime.datetime(2018, 6, 26), datetime.datetime(2100, 1, 1)),
    "452.020-P-07": (datetime.datetime(2018, 6, 27), datetime.datetime(2100, 1, 1)),
    "452.020-P-08": (datetime.datetime(2018, 8, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-09": (datetime.datetime(2018, 8, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-10": (datetime.datetime(2018, 8, 7), datetime.datetime(2100, 1, 1)),
    "452.020-P-11": (datetime.datetime(2018, 8, 9), datetime.datetime(2100, 1, 1)),
    "452.020-P-12": (datetime.datetime(2018, 8, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-13": (datetime.datetime(2018, 8, 31), datetime.datetime(2100, 1, 1)),
    "452.020-P-16": (datetime.datetime(2018, 9, 3), datetime.datetime(2100, 1, 1)),
    "452.020-P-17": (datetime.datetime(2018, 9, 4), datetime.datetime(2100, 1, 1)),
    "452.020-P-18": (datetime.datetime(2018, 9, 5), datetime.datetime(2100, 1, 1)),
    "452.020-P-19": (datetime.datetime(2018, 9, 6), datetime.datetime(2100, 1, 1)),
    "452.020-P-20": (datetime.datetime(2018, 9, 8), datetime.datetime(2100, 1, 1)),
    "452.020-P-21": (datetime.datetime(2018, 9, 9), datetime.datetime(2100, 1, 1)),
    "452.020-P-22": (datetime.datetime(2018, 9, 10), datetime.datetime(2100, 1, 1)),
    "452.020-P-23": (datetime.datetime(2018, 9, 12), datetime.datetime(2100, 1, 1)),
    "452.020-P-24": (datetime.datetime(2018, 9, 13), datetime.datetime(2100, 1, 1)),
    "452.020-P-0051": (datetime.datetime(2020, 1, 1), datetime.datetime(2100, 1, 1)),
    "452.020-P-25": (datetime.datetime(2018, 9, 14), datetime.datetime(2100, 1, 1))
}

# Boolean set to true in order to delete every processed data and redo everything
redo = False

# Generate CSV with RAW data
generate_csv_file = False

# Plot interactive figures in HTML format for acoustic events
# WARNING: Plotly files takes a lot of memory so commented by default
events_plotly = False

# Path for input datas
dataPath = "server"


def main():
    # Set working directory in "scripts"
    if "scripts" in os.listdir("."):
        os.chdir("scripts")

    # Create processed directory if it doesn't exist
    if not os.path.exists("../processed/"):
        os.mkdir("../processed/")

    # Search Mermaid floats
    mfloats = [p.split("/")[-1][:-4] for p in glob.glob("../" + dataPath + "/*.vit")]

    # For each Mermaid float
    for mfloat in mfloats:
        print ""
        print "> " + mfloat

        # Set the path for the float
        mfloat_path = "../processed/" + mfloat + "/"

        # Get float number
        mfloat_nb = re.findall("(\d+)$", mfloat)[0]

        # Delete the directory if the redo flag is true
        if redo and os.path.exists(mfloat_path):
            shutil.rmtree(mfloat_path)

        # Create directory for the float
        if not os.path.exists(mfloat_path):
            os.mkdir(mfloat_path)

        # Remove existing files in the processed directory (if the script have been interrupted the time before)
        for f in glob.glob(mfloat_path + "*.*"):
            os.remove(f)

        # Copy appropriate files in the directory and remove files outside of the time range
        extensions = ["000", "001", "002", "003", "004", "005", "LOG", "BIN"]
        files_to_copy = list()
        for extension in extensions:
                files_to_copy += glob.glob("../" + dataPath + "/" + mfloat_nb + "*." + extension)
        files_to_copy += glob.glob("../" + dataPath + "/" + mfloat_nb + "*.MER")
        files_to_copy += glob.glob("../" + dataPath + "/" + mfloat_nb + "*.S41")
        if mfloat in filterDate.keys():
            begin = filterDate[mfloat][0]
            end = filterDate[mfloat][1]
            files_to_copy = [f for f in files_to_copy if begin <= utils.get_date_from_file_name(f) <= end]
        else:
            # keep all files
            begin = datetime.datetime(1000, 1, 1)
            end = datetime.datetime(3000, 1, 1)

        # Add .vit and .out files
        files_to_copy += glob.glob("../" + dataPath + "/" + mfloat + "*")

        # Copy files
        for f in files_to_copy:
            shutil.copy(f, mfloat_path)

        # Decrypt all BIN files
        decrypt.decrypt_all(mfloat_path)

        # Build list of all mermaid events recorded by the float
        mevents = events.Events(mfloat_path)

        # Build list of all profiles recorded
        ms41s = profile.Profiles(mfloat_path)

        # Process data for each dive
        mdives = dives.get_dives(mfloat_path, mevents, ms41s)

        # Compute files for each dive
        for dive in mdives:
            # Create the directory
            if not os.path.exists(dive.export_path):
                os.mkdir(dive.export_path)
            # Generate log
            dive.generate_datetime_log()
            # Generate mermaid environment file
            dive.generate_mermaid_environment_file()
            # Generate S41 params file
            dive.generate_s41_environment_file()
            # Generate dive plot
            dive.generate_dive_plotly(generate_csv_file)

        # Compute clock drift correction for each event
        for dive in mdives:
            dive.correct_events_clock_drift()

        # Compute location of mermaid float for each event (because the station is moving)
        # the algorithm use gps information in the next dive to estimate surface drift
        i = 0
        while i < len(mdives)-1:
            mdives[i].compute_events_station_location(mdives[i+1])
            i += 1

        # Generate plot and sac files
        for dive in mdives:
            dive.generate_events_plot()
            if events_plotly:
                dive.generate_events_plotly()
            dive.generate_events_sac()
            dive.generate_profile_plotly(generate_csv_file)

        # Plot vital data
        kml.generate(mfloat_path, mfloat, mdives)
        vitals.plot_battery_voltage(mfloat_path, mfloat + ".vit", begin, end)
        vitals.plot_internal_pressure(mfloat_path, mfloat + ".vit", begin, end)
        vitals.plot_pressure_offset(mfloat_path, mfloat + ".vit", begin, end)

        # Clean directories
        for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.LOG"):
            os.remove(f)
        for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.BIN"):
            os.remove(f)
        for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.MER"):
            os.remove(f)
        for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.S41"):
            os.remove(f)

        # for dive in mdives[:-1]: # on ne regarde pas la derniere plongee qui n'a pas ete interpolee
        #    if dive.is_complete_dive: # on ne regarde que les vraies plongees (pas les tests faits a terre)
        #        print dive.log_name
        #        for gps in dive.gps_list[0:-1]: # point GPS avant de descendre
        #            print gps.date
        #        print dive.surface_leave_loc.date
        #        print dive.great_depth_reach_loc.date
        #        print dive.great_depth_leave_loc.date
        #        print dive.gps_list[-1].date # point GPS en arrivant en surface


if __name__ == "__main__":
    main()
