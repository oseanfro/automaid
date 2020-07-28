#buoy default
#buoy store
buoy bypass 20000 120000
buoy near 25000 3
buoy far 15000 4
p2t dt 1000000
p2t dp 500
feature actuiwatch 1
stage del
stage 1500dbar (20dbar) 833mn (833mn)
stage 1500dbar (20dbar) 1620mn (2453mn)
stage surfacing 417mn (2870mn) SBE41
stage params SBE41 samplerate=1
stage params SBE41 binaverageoutput=0
#stage params SBE41 top_bin_interval=1
#stage params SBE41 top_bin_size=1
#stage params SBE41 top_bin_max=5
#stage params SBE41 middle_bin_interval=2
#stage params SBE41 middle_bin_size=2
#stage params SBE41 middle_bin_max=40
#stage params SBE41 bottom_bin_interval=3
#stage params SBE41 bottom_bin_size=3
stage params SBE41 speedcontrol=8
#stage params SBE41 runningpumpbeforeprofile=10
stage store
start

