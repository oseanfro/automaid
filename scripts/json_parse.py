import os
import shutil
import sys
import glob
import json
from . import dives
from . import events

def main():
    # Set working directory in "scripts"
    if "scripts" in os.listdir("."):
        os.chdir("scripts")

    # Set the path for the float
    datapath = "../server/"
    object_json_array = list()
    # Search Mermaid floats
    mfloats = [p.split("/")[-1][:-4] for p in glob.glob(datapath)]

    for mfloat in mfloats:
        # Build list of all mermaid events recorded by the float
        mevents = events.Events(datapath)
        # Process data for each dive
        mdives = dives.get_dives(datapath, mevents)
        # Compute files for each dive
        for dive in mdives:
            object_json_array.append(dive.generateJSON())

    #listbox = Listbox(root, listvariable=choices, selectmode="multiple")
    print(json.dumps(object_json_array, indent=4))
if __name__ == "__main__":
 main()
