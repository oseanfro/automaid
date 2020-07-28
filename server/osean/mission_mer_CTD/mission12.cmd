#buoy default
buoy bypass 20000 120000
buoy near 15000 3
buoy far 25000 4
buoy mmtime 43200
buoy dead 300
buoy delay 900 7200
p2t dt 1000000
p2t dp 500
#buoy store
feature actuiwatch 1
mermaid TRIG:3,1
stage del
stage 1500dbar (50dbar) 833mn (833mn)
stage 1500dbar (50dbar) 5360mn (6193mn) MERMAID
stage 2000dbar (10dbar) 310mn (6503mn)
stage surfacing 536mn (7039mn) SBE41
stage params SBE41 samplerate=0
#stage params SBE41 binaverageoutput=0
#stage params SBE41 top_bin_interval=10
#stage params SBE41 top_bin_size=10
#stage params SBE41 top_bin_max=100
#stage params SBE41 middle_bin_interval=50
#stage params SBE41 middle_bin_size=50
#stage params SBE41 middle_bin_max=1000
#stage params SBE41 bottom_bin_interval=100
#stage params SBE41 bottom_bin_size=100
stage params SBE41 speedcontrol=8
#stage params SBE41 runningpumpbeforeprofile=10
stage store
#start

