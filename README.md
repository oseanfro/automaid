# automaid

This program converts raw data transmitted by Mermaid instruments to
classify data, correct clock drifts, interpolate float positions and
then generates seismic SAC files, plots seismic events and dives and
generates KML, HTML, and PNG files.

Written by Sebastien Bonnieux. Maintained by Frédéric Rocca.

### 1. INSTALLATION

This installation procedure has been tested with linux.

An easy installation procedure is described here:

* Install [Miniconda](https://conda.io/miniconda.html) or
  [Anaconda](https://www.anaconda.com/download/) (which requires more
  disk space). (You may already have it, you might have to do `module
  load anaconda/5.2.0` to specify the precise version).
* Restart your terminal to load the new PATH variables.
* Add the conda-forge channel:
`conda config --add channels conda-forge`
* Create a virtual environment called "pymaid":
`conda create -n pymaid python=3.10 obspy plotly`

In addition to the Python 3.10 installation it is necessary to compile,
using `make` the wavelet inversion programs located in
`scripts/src/V103/` and `scripts/src/V103EC/`. The compiled binaries
must be in the "bin" directory and must be named `icdf24_v103_test` and
`icdf24_v103ec_test`.

### 2. USAGE

To use the application:

* Copy files from your Mermaid server into the "server" directory:
`scp username@host:\{"*.LOG","*.BIN","*.S61","*.MER","*.vit"\} server`
* Activate the virtual environment:
`conda activate pymaid`
* Run the main.py file in the "scripts" directory:
`python scripts/main.py`
* Quit the virtual environment:
`conda deactivate`

You will be getting the processed files into the directory `processed`.
You may have to remove some error-prone log files and create some
directories - we will be editing the script for increased versatility
as we go along.

The "arguments.py" file can be edited to select some options:

* A "server_directory" parameter to define server directory path relative to automaid or absolute
* A "processed_directory" parameter to define output directory path relative to automaid or absolute
* A "generate_dive_csv_file" flag allow the user to generate "csv" file with timestamped pressure sample
* A "generate_profil_csv_file" flag allow the user to generate "csv" file with SBE61 samples
* Each "*_ploted" flags allow the user to display or not vertical lines when actionners is used or measure is done (in html file)
* Each "export_*" flags allow the user to choose output format for MERMAID data
* A "local_html" flags allow the user to generate html with or not plotly librairie (if this flag is False user must have internet access to display html files)
* A "generate_ncdf_files" flags allow the user to generate NETCDF files according argo user manual

To generate NETCDF files you need to install new python module :

* Activate the virtual environment:
`conda activate pymaid`
* Install NETCDF module:
`conda install -c conda-forge netCDF4`
