2020-01-14T13:56:43:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-01-14T13:56:43:[MAIN  ,0007]buoy 452.020-P-0051
2020-01-14T13:56:43:[MAIN  ,0055]soft pilotage 452.012.300_V2.9-20200113
2020-01-14T13:56:43:[MAIN  ,0011]date 2020-01-14T13:56:43
2020-01-14T13:56:49:[MAIN  ,0006]battery 15371mV,   11346uA
2020-01-14T13:56:52:[MAIN  ,0024]internal pressure 79639Pa
2020-01-14T13:56:53:[PRESS ,0038]P    -41mbar,T+14781mdegC
2020-01-14T13:56:54:[MRMAID,0182]thread started
2020-01-14T13:56:55:[MRMAID,0186]no wake-up
2020-01-14T13:56:56:[MRMAID,0188]acq already stopped
2020-01-14T13:56:56:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-01-14T13:56:57:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-01-14T13:56:57:[TESTMD,0053]Enter in test mode? yes/no
2020-01-14T13:56:57:[TESTMD,0252]0051>
2020-01-14T13:57:05:[TESTMD,0050]"yes"
2020-01-14T13:57:05:[TESTMD,0249]
Command list
pext    : Get external pressure
pint    : Get internal vacuum
ui      : Get voltage/current
act     : Test actuators
fillb   : Pump until filling the bladder
bpopen  : Open bypass
bpclose : Close bypass
date    : Get date
gps     : GPS synchronization
iridium : Iridium transfer
mstart  : Start mermaid acq
mstop   : Stop mermaid acq
mdata   : Get mermaid datas
ls      : List files
cat     : Print content of a file
rm      : Remove a file
h       : Print command list
q       : Quit

Advanced
pumps X : pompe Xs (lent)
pumpf X : pompe Xs (rapide)
evh     : ouvre l'electrovalve 30s
bypass  : ouvre le bypass 30s
dvmine  : deverminage de la carte
nominal : mode nominal pour mesure de conso
cychydr : test du circuit hydraulique
mkdir   : creer un repertoire
mv      : deplacer un fichier
ps      : liste les processus

Set params
stage   : Stage settings
buoy    : Buoy settings
p2t     : Pressure sensor settings
log     : Verb cfg
mermaid : Mermaid cfg
upload  : On/Off Irid transfer
sys  : system param settings


2020-01-14T13:57:05:[TESTMD,0252]0051>
2020-01-14T13:57:16:[TESTMD,0050]"iridium"
2020-01-14T13:57:24:[SURF  ,0025]Iridium...
2020-01-14T14:00:07:[SURF  ,0009]connected in 163s, signal quality 3
2020-01-14T14:00:36:[BYCMD ,0120]    bypass 10000ms 100000ms (20000ms 60000ms stored)
2020-01-14T14:00:38:[BYCMD ,0125]    near 1500mbar 3mbar/s (15000mbar 3mbar/s stored)
2020-01-14T14:00:40:[BYCMD ,0126]    far 2500mbar 4mbar/s (25000mbar 4mbar/s stored)
2020-01-14T14:00:42:[BYCMD ,0128]    dead 60s (300s stored)
2020-01-14T14:00:45:[MRMAID,0052]Mermaid $TRIG:10,1;
2020-01-14T14:00:47:[MRMAID,0052]Mermaid $DTRIG:1,1;
2020-01-14T14:00:50:[MRMAID,0052]Mermaid $SCALES:2;
2020-01-14T14:00:53:[P2TCMD,0155]p2t log dp > 50mbar
2020-01-14T14:00:55:[STACMD,0168]stage del 0
2020-01-14T14:00:57:[STACMD,0170]stage store 0
2020-01-14T14:01:07:[SURF  ,0218]prompt received, remote cmd end
2020-01-14T14:01:07:[SURF  ,0012]10 cmd(s) received
2020-01-14T14:01:30:[UPLOAD,0248]Upload data files...
2020-01-14T14:03:26:[ZIO   ,0240]"NO CARRIER" received, aborting
2020-01-14T14:03:47:[SURF  ,0014]disconnected after 383s
2020-01-14T14:03:52:[TESTMD,0252]0051>
2020-01-14T14:04:31:[TESTMD,0050]"q"
2020-01-14T14:04:31:[MAIN  ,0018]end of test mode
2020-01-14T14:04:31:[MAIN  ,0048]reboot MERMAID board
2020-01-14T14:04:33:[MAIN  ,0047]reboot float
2020-01-14T14:04:33:[MONITR,0198]rebooting with code 0x0000, data "src/monitor.c@516002"
