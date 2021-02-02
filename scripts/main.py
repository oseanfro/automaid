import os
import shutil
import glob
import datetime
import dives
import profile
import events
import decrypt
import vitals
import databases
import kml
import re
import utils
import sys

from configuration import dataPath
from configuration import events_plotly
from configuration import filterDate
from configuration import generate_csv_file

redo = "True"

# main process
def process(mfloat_path, mfloat, begin, end):
    # Concatenate LOG and BIN files that need it
    utils.concatenate_files(mfloat_path)
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
    while i < len(mdives) - 1:
        mdives[i].compute_events_station_location(mdives[i + 1])
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

    return (mdives)

# generate as a function
def generate(mfloat, datapath, filterdate):
    # For each Mermaid float
    print ""
    print "> " + mfloat
    # Get float number
    mfloat_nb = re.findall("(\d+)$", mfloat)[0]
    # Set the path for the float
    mfloat_path_source = datapath + "/" + mfloat + "/source/"
    mfloat_path_processed = datapath + "/" + mfloat + "/processed/"
    # Create data directory
    if not os.path.exists(datapath):
        os.mkdir(datapath)
    # Create float directory
    if not os.path.exists(datapath + "/" + mfloat):
        os.mkdir(datapath + "/" + mfloat)
    # Create directory for the source float
    if not os.path.exists(mfloat_path_source):
        os.mkdir(mfloat_path_source)
    # Remove old processed
    if os.path.exists(mfloat_path_processed):
        shutil.rmtree(mfloat_path_processed)
    # Create processed directory
    os.mkdir(mfloat_path_processed)
    # Copy appropriate files in the directory and remove files outside of the time range
    files_to_copy = list()
    # All separated files, BIN files for V2, LOG files for V1, MERMAID files, SBE41 files
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*[.][0-9][0-9][0-9]")
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*[.]BIN")
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*[.]LOG")
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*[.]MER")
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*[.]S41")

    if mfloat in filterDate.keys():
        begin = filterDate[mfloat][0]
        end = filterDate[mfloat][1]
        files_to_copy = [f for f in files_to_copy if begin <= utils.get_date_from_file_name(f) <= end]
    else:
        # keep all files
        begin = datetime.datetime(1000, 1, 1)
        end = datetime.datetime(3000, 1, 1)

    # Add .vit and .out files
    files_to_copy += glob.glob(mfloat_path_source + mfloat + "*")

    # Copy files
    for f in files_to_copy:
        shutil.copy(f, mfloat_path_processed)

    mdives =[]
    files_to_delete = list()

    try:
        mdives = process(mfloat_path_processed, mfloat, begin, end)
    except:
        mdives = []
        print "Error on process"
    else:
        # Clean directories
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*[.][0-9][0-9][0-9]")
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*[.]BIN")
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*[.]LOG")
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*[.]MER")
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*[.]S41")
        files_to_delete += glob.glob(mfloat_path_processed + mfloat + "*")

    for f in files_to_delete:
        os.remove(f)

    return mdives

# generate as a script (python automaid.py)
def main():
    # Set working directory in "scripts"
    if "scripts" in os.listdir("."):
        os.chdir("scripts")

    outputPath = "../processed"
    # Create ouput directory
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    # Update databases
    print "****************"
    print "Update databases"
    print "****************"
    absFilePath = os.path.abspath(__file__)
    scriptpath, scriptfilename = os.path.split(absFilePath)
    database_path = os.path.join(scriptpath,"databases")
    databases.update(database_path)

    # Search Profiler by folder name
    buoys_dir_paths=[os.path.join("../",dataPath)]
    for root, dirs, files in os.walk(os.path.join("../",dataPath)):
        for dir in dirs:
            buoy_dir = re.match('.*([0-9]{3}.[0-9]{3}-[A-z]-([0-9]{4}|[0-9]{2}))', dir)
            if (buoy_dir):
                vitals.merge_vitals(os.path.join(root,dir),str(buoy_dir.group(1))+".vit");
                buoys_dir_paths.append(os.path.join(root,dir))

    print buoys_dir_paths
    # Search Profiler floats at root directory
    for buoy_dir in buoys_dir_paths :
        mfloats = [p.split("/")[-1][:-4] for p in glob.glob(buoy_dir + "/[0-9][0-9][0-9].[0-9][0-9][0-9]-*.vit")]
        # For each Mermaid float
        for mfloat in mfloats:
            print ""
            print "> " + mfloat

            # Get float number
            mfloat_nb = re.findall("(\d+)$", mfloat)[0]
            mfloat_path = os.path.join(outputPath,mfloat)
            mfloat_src_path = os.path.join(mfloat_path,"source")

            # Create float directory
            if not os.path.exists(mfloat_path):
                os.mkdir(mfloat_path)
            # Create directory for the source float
            if not os.path.exists(mfloat_src_path):
                os.mkdir(mfloat_src_path)

            # Copy appropriate files in the directory and remove files outside of the time range
            extensions = ["000", "001", "002", "003", "004", "005", "LOG", "BIN"]
            files_to_copy = list()
            for extension in extensions:
                    files_to_copy += glob.glob( buoy_dir + "/" + mfloat_nb + "*." + extension)
            files_to_copy += glob.glob(buoy_dir + "/" + mfloat_nb + "*.MER")
            files_to_copy += glob.glob(buoy_dir + "/" + mfloat_nb + "*.S41")
            if mfloat in filterDate.keys():
                begin = filterDate[mfloat][0]
                end = filterDate[mfloat][1]
                files_to_copy = [f for f in files_to_copy if begin <= utils.get_date_from_file_name(f) <= end]
            else:
                # keep all files
                begin = datetime.datetime(1000, 1, 1)
                end = datetime.datetime(3000, 1, 1)

            # Add .vit and .out files
            files_to_copy += glob.glob(buoy_dir + "/" + mfloat + "*")
            # Copy files
            for f in files_to_copy:
                shutil.copy(f, mfloat_src_path)

            try:
                generate(mfloat,outputPath,filterDate);
            except:
                print "error on process"


if __name__ == "__main__":
    main()
