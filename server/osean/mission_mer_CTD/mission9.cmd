#buoy default
#buoy bypass 20000 120000
#buoy near 15000 3
#buoy far 25000 4
#buoy mmtime 43200
#buoy dead 300
#buoy delay 900 7200
p2t dt 1000000
p2t dp 500
buoy store
feature actuiwatch 1
mermaid TRIG:3,1
stage del
stage 1500dbar (50dbar) 833mn (833mn)
stage 1500dbar (50dbar) 5200mn (6033mn) MERMAID
stage 2000dbar (50dbar) 278mn (6311mn)
stage surfacing 536mn (6847mn) SBE41
#stage params SBE41 samplerate=1
#stage params SBE41 binaverageoutput=0
#stage params SBE41 top_bin_interval=1
#stage params SBE41 top_bin_size=1
#stage params SBE41 top_bin_max=5
#stage params SBE41 middle_bin_interval=2
#stage params SBE41 middle_bin_size=2
#stage params SBE41 middle_bin_max=40
#stage params SBE41 bottom_bin_interval=3
#stage params SBE41 bottom_bin_size=3
#stage params SBE41 speedcontrol=8
#stage params SBE41 runningpumpbeforeprofile=10
stage store
#start

