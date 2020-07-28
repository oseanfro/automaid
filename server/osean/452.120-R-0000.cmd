#buoy default
#buoy store
buoy bypass 20000 120000
buoy near 25000 3
buoy far 15000 4
buoy mmtime 43200
mermaid TRIG:3,1
mermaid KEEP_SIZE:0.010,0.100,4000
mermaid KEEP_ALL:0.100,1.300
mermaid STALTAFLT:B0=1/1,A0=1/1
mermaid WEIGHT:0.0,0.93206,0.64848,0.00095,0.16048,0.27136
mermaid ASCEND_THRESH:0.100,1.300,20,8192
p2t dt 1000000
p2t dp 500
feature actuiwatch 1
stage del
stage 50dbar (5dbar) 30mn (30mn)
stage 50dbar (5dbar) 30mn (60mn) MERMAID
stage surfacing 60mn (180mn) SBE41
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
#start

