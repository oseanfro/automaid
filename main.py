import os
import shutil
import glob
import datetime
import re
import sys
import traceback

try:
    import kml
    import dives
    import utils
    import sbe41
    import sbe61
    import events
    import decrypt
    import vitals
    import databases
    from arguments import data_directory
    from arguments import events_plotly
    from arguments import generate_csv_file
except:
    import automaid.kml as kml
    import automaid.dives as dives
    import automaid.utils as utils
    import automaid.sbe41 as sbe41
    import automaid.sbe61 as sbe61
    import automaid.events as events
    import automaid.decrypt as decrypt
    import automaid.vitals as vitals
    import automaid.databases as databases
    from automaid.arguments import data_directory
    from automaid.arguments import events_plotly
    from automaid.arguments import generate_csv_file

redo = "True"

# Generate processed files
def generate_processed_files(mfloat, mfloat_path):
    # Build list of all mermaid events recorded by the float
    mevents = events.Events(mfloat_path)
    # Build list of all profiles recorded
    ms41s = sbe41.Profiles(mfloat_path)
    # Build list of all profiles recorded
    ms61s = sbe61.Profiles(mfloat_path)
    # Process data for each dive
    mdives = dives.Dives(mfloat_path, mevents, ms41s,ms61s)

    # Compute files for each dive
    for dive in mdives.get_dives():
        # Create the directory
        if not os.path.exists(dive.export_path):
            os.mkdir(dive.export_path)
        # Generate log
        dive.generate_datetime_log()
        # Generate mermaid environment file
        dive.generate_mermaid_environment_file()
        # Generate profiles params file
        dive.generate_s41_environment_file();
        dive.generate_s61_environment_file();
        # Generate dive plot
        dive.generate_dive_plotly(generate_csv_file)

    # Compute clock drift correction for each event
    for dive in mdives.get_dives():
        dive.correct_events_clock_drift()

    # Compute location of mermaid float for each event (because the station is moving)
    # the algorithm use gps information in the next dive to estimate surface drift
    i = 0
    while i < len(mdives.get_dives()) - 1:
        mdives.get_dives()[i].compute_events_station_location(
            mdives.get_dives()[i + 1])
        i += 1

    # Generate plot and sac files
    for dive in mdives.get_dives():
        if events_plotly:
            dive.generate_events_plotly()
        else :
            dive.generate_events_plot()
        dive.generate_events_sac()
        dive.generate_profile_plotly(generate_csv_file)

    # Plot vital data
    kml.generate(mfloat_path, mfloat, mdives.get_dives())
    vitals.plot_battery_voltage(mfloat_path, mfloat + ".vit")
    vitals.plot_internal_pressure(mfloat_path, mfloat + ".vit")
    vitals.plot_pressure_offset(mfloat_path, mfloat + ".vit")

    return (mdives)


# Move src files into process directory, Generate processed files and clean directory
def process_one_float(mfloat, datapath):
    # For each Mermaid float
    print("")
    print(("> " + mfloat))
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
    # Create processed
    if not os.path.exists(mfloat_path_processed):
        os.mkdir(mfloat_path_processed)

    # Copy appropriate files in the directory and remove files outside of the time range
    files_to_copy = list()
    # All files begin with buoy nb
    files_to_copy += glob.glob(mfloat_path_source + mfloat_nb + "_*")
    # Add .vit and .out files
    files_to_copy += glob.glob(mfloat_path_source + mfloat + "*")
    files_to_copy += glob.glob(mfloat_path_source + "*.vit")
    # Copy files
    for f in files_to_copy:
        shutil.copy(f, mfloat_path_processed)

    files_generated = list()
    # Concatenate VIT files that need it
    files_generated += vitals.merge_vitals(mfloat_path_processed, mfloat + ".vit")
    # Concatenate LOG and BIN files that need it
    files_generated += utils.concatenate_files(mfloat_path_processed)
    # Decrypt all BIN files
    files_generated += decrypt.decrypt_all(mfloat_path_processed)
    # Create generated files folder
    files_generated_path = os.path.join(mfloat_path_processed,"temporary")
    if not os.path.exists(files_generated_path):
        os.mkdir(files_generated_path)
    # Copy files
    for f in files_generated:
        shutil.copy(f, files_generated_path)

    mdives = dives.Dives()
    files_to_delete = list()
    try:
        mdives = generate_processed_files(mfloat, mfloat_path_processed)
    except:
        # Just print(e) is cleaner and more likely what you want,
        # but if you insist on printing message specifically whenever possible...
        traceback.print_exc()
        mdives = None
    else:
        # Clean directories
        files_to_delete += glob.glob(mfloat_path_processed + mfloat_nb + "_*")
        files_to_delete += glob.glob(mfloat_path_processed + "*.vit")

    for f in files_to_delete:
        os.remove(f)

    return mdives

# #############################
#       standalones functions
# #############################

def update_tree(mfloat_serial, src_path, dest_path) :
    # Get float number
    mfloat_nb = re.findall("(\d+)$", mfloat_serial)[0]
    mfloat_path = os.path.join(dest_path, mfloat_serial)
    mfloat_src_path = os.path.join(mfloat_path, "source")

    # Create float directory
    if not os.path.exists(mfloat_path):
        os.mkdir(mfloat_path)
    # Create directory for the source float
    if not os.path.exists(mfloat_src_path):
        os.mkdir(mfloat_src_path)

    # Copy appropriate files in the directory
    extensions = ["[0-9][0-9][0-9]", "LOG", "BIN"]
    files_to_copy = list()
    for extension in extensions:
        files_to_copy += glob.glob(src_path + "/" + mfloat_nb + "*." + extension)
    files_to_copy += glob.glob(src_path + "/" + mfloat_nb + "*.MER")
    files_to_copy += glob.glob(src_path + "/" + mfloat_nb + "*.S41")
    files_to_copy += glob.glob(src_path + "/" + mfloat_nb + "*.S61")

    # Add .vit and .out files
    files_to_copy += glob.glob(src_path + "/" + mfloat_serial + "*")
    files_to_copy += glob.glob(src_path + "/" + mfloat_serial + "*.vit")

    # Copy files
    for f in files_to_copy:
        shutil.copy(f, mfloat_src_path)


# generate as a script (python automaid.py)
def main():
    # Set working directory in "scripts"
    if "scripts" in os.listdir("."):
        os.chdir("scripts")

    outputPath = "../processed"
    dataPath = os.path.join("../", data_directory)

    # Create ouput directory
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    # Update databases
    absFilePath = os.path.abspath(__file__)
    scriptpath, scriptfilename = os.path.split(absFilePath)
    database_path = os.path.join(scriptpath, "databases")
    databases.update(database_path)

    # Floats list
    mfloats = []
    # Search sub folders with Profiler name and initialize tree
    for root, dirs, files in os.walk(dataPath):
        for dir in dirs:
            buoy_dir = re.match('.*([0-9]{3}.[0-9]{3}-[A-z]-([0-9]{4}|[0-9]{2}))', dir)
            if (buoy_dir):
                buoy_serial = buoy_dir.group(1)
                update_tree(buoy_serial,root,outputPath)
                mfloats += [buoy_serial]
        for file in files:
            if os.path.samefile(root,dataPath) :
                buoy_vit = re.match('([0-9]{3}.[0-9]{3}-[A-z]-([0-9]{4}|[0-9]{2}))\.vit', file)
                if (buoy_vit):
                    buoy_serial = buoy_vit.group(1)
                    update_tree(buoy_serial,root,outputPath)
                    mfloats += [buoy_serial]

    # For each Mermaid float make process
    for mfloat in mfloats:
        try:
            process_one_float(mfloat, outputPath)
        except:
            # Just print(e) is cleaner and more likely what you want,
            # but if you insist on printing message specifically whenever possible...
            traceback.print_exc()

if __name__ == "__main__":
    main()
