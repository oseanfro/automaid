# automaid

This program converts raw data transmitted by Mermaid instruments to
classify data, correct clock drifts, interpolate float positions and
then generates seismic SAC files, plots seismic events and dives and
generates KML, HTML, and PNG files.

Written by Sebastien Bonnieux.

Slight edits to this and other README.md files by Frederik J Simons

### 1. INSTALLATION

This installation procedure has been tested with macOS. For Linux the
procedure is valid but one could prefer to use a the package manager.
For Windows the installation of Python 2.7 is valid but the
compilation of the wavelet inversion program with "make" could be
problematic.

An easy installation procedure is described here:

* Install [Miniconda](https://conda.io/miniconda.html) or
  [Anaconda](https://www.anaconda.com/download/) (which requires more
  disk space). (You may already have it, you might have to do `module load anaconda`). 
* Restart your terminal to load the new PATH variables.
* Add the conda-forge channel:  
`conda config --add channels conda-forge`
* Create a virtual environment called "pymaid":  
`conda create -n pymaid python=2.7`

* Make sure you are in the `bash` shell!

* Activate the environment:  
`source activate pymaid`
* Install obspy:  
`conda install obspy`
* Install plotly 2.7.0:  
`conda install plotly=2.7.0`
* Quit the virtual environment:  
`source deactivate`

In addition to the Python 2.7 installation it is necessary to compile,
using `make` the wavelet inversion programs located in
`scripts/src/V103/` and `scripts/src/V103EC/`. The compiled binaries
must be in the "bin" directory and must be named `icdf24_v103_test` and
`icdf24_v103ec_test`.

### 2. USAGE

To use the application: 

* Copy files from your Mermaid server into the "server" directory:  
`scp username@host:\{"*.LOG","*.MER","*.vit"\} server`
* Activate the virtual environment:  
`source activate pymaid`
* Run the main.py file in the "scripts" directory:  
`python scripts/main.py`
* Quit the virtual environment:  
`source deactivate`

You will be getting the processed files into the directory `processed`.
You may have to remove some error-prone log files and create some
directories - we will be editing the script for increased versatility
as we go along.

The "main.py" file can be edited to select some options:

* A date range between which to process the data can be chosen with
the `begin` and `end` variables. 
* A "redo" flag can be set to True in order to restart the processing
of data for each launch of the script. This flag force the deletion
of the content of the content of the `processed` directory.
* A `events_plotly` flag allow the user to plot interactive figures
of events in a html page. This kind of plot can be disabled to save
disk space.

