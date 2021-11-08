import os
import shutil
import sys
import glob
import test
import re
import utils
from obspy import UTCDateTime
from tkinter import *
from functools import partial
import datetime

class Input:
    root = None
    index = None
    framelist = None
    outputlist = None
    year = None
    month = None
    day = None
    label = None
    button = None
    mfloats = None
    def __init__(self,mfloats):
        self.root = Tk()
        self.framelist = []
        self.outputlist = []
        self.index = 0
        self.date_begin = []
        self.date_end = []
        self.label = Label(self.root, text='Choose the buoy  ')
        self.mfloats = mfloats
        self.button = Button(self.root, text='Launch', command=partial(launch_process,self))

    def add_list(self):
        for mfloat in self.mfloats:
            fra = Frame(self.root)
            output = BooleanVar(self.root, '0');
            date_begin = StringVar(self.root, '19800101')
            date_end = StringVar(self.root, '21000101')
            self.outputlist.append(output);
            self.date_begin.append(date_begin);
            self.date_end.append(date_end);

            Checkbutton(fra, variable=self.outputlist[self.index]).grid(row=0, column=0)
            Label(fra, text=mfloat).grid(row=0, column=1)
            Label(fra, text="Start(format:%YYYY%MM%DD) : ").grid(row=0, column=2)
            Entry(fra, textvariable=self.date_begin[self.index]).grid(row=0, column=3)
            Label(fra, text="End(format:%YYYY%MM%DD) : ").grid(row=0, column=4)
            Entry(fra, textvariable=self.date_end[self.index]).grid(row=0, column=5)

            self.framelist.append(fra)
            self.framelist[self.index].grid(row=self.index, column=0)
            self.index = self.index +1

        self.button.grid(row=self.index, column=0)
        self.index = self.index +1
        self.label.grid(row=self.index, column=0)

    def start(self):
        self.root.mainloop()

def launch_process(inputs):
    choices = []
    dates_begin = []
    dates_end = []
    index = 0
    for input in inputs.outputlist:
        if input.get() == True:
            choices.append(inputs.mfloats[index])
            dates_begin.append(inputs.date_begin[index])
            dates_end.append(inputs.date_end[index])
        index = index +1


    index = 0
    for choice in choices:
        with open(choices[index], 'w') as f:
            # We redirect the 'sys.stdout' command towards the descriptor file
            sys.stdout = f
            date_begin = dates_begin[index].get()
            date_end = dates_end[index].get()
            b_year = int(date_begin[0:4])
            b_mont = int(date_begin[5:6])
            b_day = int(date_begin[7:8])
            e_year = int(date_end[0:4])
            e_mont = int(date_end[5:6])
            e_day = int(date_end[7:8])

            test.dive(choices[index],datetime.datetime(b_year, b_mont, b_day),datetime.datetime(e_year, e_mont, e_day))
        index = index +1
    #label.config(text="script finished !!")


def main():
    # Set working directory in "scripts"
    if "scripts" in os.listdir("."):
        os.chdir("scripts")

    # Create processed directory if it doesn't exist
    if not os.path.exists("../processed/"):
        os.mkdir("../processed/")

    # Search Mermaid floats
    mfloats = [p.split("/")[-1][:] for p in glob.glob("../processed/*")]
    #listbox = Listbox(root, listvariable=choices, selectmode="multiple")
    input = Input(mfloats)
    input.add_list()
    input.start()

if __name__ == "__main__":
 main()
