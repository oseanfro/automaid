import os
import shutil
import sys
import decrypt
import glob
import dives
import events
import profile
import re
import utils
import netCDF.init_values as init
from obspy import UTCDateTime
from netCDF4 import Dataset
from netCDF4 import stringtochar
from datetime import datetime,timezone
import numpy as np

import mermaid_to_nc_cfg as cfg
import mermaid_to_mono_profile
import mermaid_to_multi_profile

serverPath = "../server/"
outputPath = "../ARGO/"


def mermaid_to_nc(mfloat,date_begin,date_end) :
    # Set the input and output path
    mfloat_path = outputPath + mfloat + "/"
    mfloat_src_path = mfloat_path + "source/"
    mfloat_processed_path = mfloat_path + "processed/"
    mfloat_input_path = serverPath + mfloat + "/"

    if not os.path.exists(mfloat_input_path):
        print(mfloat_input_path + " doesn't exists")
        return
    # Get float number
    mfloat_nb = re.findall("(\d+)$", mfloat)[0]
    # Create buoy directory
    if not os.path.exists(mfloat_path):
        os.mkdir(mfloat_path)
    # Create source directory
    if not os.path.exists(mfloat_src_path):
        os.mkdir(mfloat_src_path)
    # Clean source directory
    files_to_delete = glob.glob(mfloat_src_path + "*")
    for f in files_to_delete:
        os.remove(f)
    # Create processed directory
    if not os.path.exists(mfloat_processed_path):
        os.mkdir(mfloat_processed_path)

    # Copy appropriate files in the directory and remove files outside of the time range
    files_to_copy = list()
    # All separated files, BIN files for V2, LOG files for V1, MERMAID files, SBE41 files
    files_to_copy += glob.glob(mfloat_input_path + mfloat_nb + "_*[.][0-9][0-9][0-9]")
    files_to_copy += glob.glob(mfloat_input_path + mfloat_nb + "_*[.]BIN")
    files_to_copy += glob.glob(mfloat_input_path + mfloat_nb + "_*[.]LOG")
    files_to_copy += glob.glob(mfloat_input_path + mfloat_nb + "_*[.]MER")
    files_to_copy += glob.glob(mfloat_input_path + mfloat_nb + "_*[.]S41")
    #Filter Date
    files_to_copy = [f for f in files_to_copy if date_begin <= utils.get_date_from_file_name(f) <= date_end]
    # Add .vit and .out files and .cmd files
    files_to_copy += glob.glob(mfloat_input_path + mfloat + "*")

    # Copy files
    for f in files_to_copy:
        shutil.copy(f, mfloat_src_path)

    # Concatenate LOG and BIN files that need it
    utils.concatenate_files(mfloat_src_path)
    # Decrypt all BIN files
    decrypt.decrypt_all(mfloat_src_path)

    # Build list of all mermaid events recorded by the float
    mevents = events.Events(mfloat_src_path)
    # Build list of all profiles recorded
    ms41s = profile.Profiles(mfloat_src_path)
    # Process data for each dive
    mdives = dives.get_dives(mfloat_src_path, mevents, ms41s)
    mfloat_nc_path = mfloat_processed_path + mfloat
    mfloat_nc_profiles_path = mfloat_processed_path + "profiles/"
    if not os.path.exists(mfloat_nc_profiles_path):
        os.mkdir(mfloat_nc_profiles_path)
    mfloat_nc_profiles_path+=mfloat

    mermaid_to_multi_profile.create_nc_multi_prof_c_file_3_1(mfloat_nc_path,mdives,mevents,ms41s)
    mermaid_to_mono_profile.create_nc_mono_prof_c_file_3_1(mfloat_nc_profiles_path,mdives,mevents,ms41s)

if __name__ == "__main__":
    #mermaid_to_nc("452.020-P-0051",datetime(2020, 7, 8),datetime(2020, 10, 30))
    mermaid_to_nc("452.020-P-0051",UTCDateTime(2020, 7, 8),UTCDateTime(2020, 10, 30))
