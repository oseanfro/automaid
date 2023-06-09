import datetime

# Path for input datas
server_directory = "../server"
processed_directory = "../processed"

# Generate CSV with SB61 data
generate_dive_csv_file = True
generate_profil_csv_file = True

# Plot actionners
bypass_ploted = True
valve_ploted = True
pump_ploted = True
mermaid_ploted = True
sbe61_ploted = True

# Plot interactive figures in HTML format for acoustic events
events_plotly = False
# Export formats
export_msd = False
export_sac = False
export_wav = False

# Html generation
# if local_html is false user need internet to open html
local_html = True
# if optimize is true we use Scattergl graph (optimized graph when they are a lot of points)
optimize = True
