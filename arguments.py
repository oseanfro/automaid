# @Author: Frédéric Rocca <fro>
# @Date:   2023-06-09T09:36:17+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: arguments.py
# @Last modified by:   fro
# @Last modified time: 2023-07-07T12:49:58+02:00

import datetime

# Path for input datas
server_directory = "../server"
processed_directory = "../processed"

# Generate CSV with SB61 data
generate_dive_csv_file = False
generate_profil_csv_file = False

# Plot actionners
bypass_ploted = True
valve_ploted = True
pump_ploted = True
mermaid_ploted = True
sbe61_ploted = True

# Argo
generate_ncdf_files = False

# Plot interactive figures in HTML format for acoustic events
events_plotly = True
# Export formats
export_msd = False
export_sac = False
export_wav = True

# Html generation
# if local_html is false user need internet to open html
local_html = False
# if optimize is true we use Scattergl graph (optimized graph when they are a lot of points)
optimize = True
