2020-02-05T15:41:13:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-02-05T15:41:13:[MAIN  ,0007]buoy 452.020-P-0051
2020-02-05T15:41:13:[MAIN  ,0055]soft pilotage 452.012.300_V2.10-20200130
2020-02-05T15:41:13:[MAIN  ,0011]date 2020-02-05T15:41:13
2020-02-05T15:41:19:[MAIN  ,0006]battery 15327mV,   14640uA
2020-02-05T15:41:22:[MAIN  ,0024]internal pressure 79797Pa
2020-02-05T15:41:23:[PRESS ,0038]P    +80mbar,T+20116mdegC
2020-02-05T15:41:24:[MRMAID,0182]thread started
2020-02-05T15:41:25:[MRMAID,0186]no wake-up
2020-02-05T15:41:26:[MRMAID,0188]acq already stopped
2020-02-05T15:41:26:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-02-05T15:41:27:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-02-05T15:41:27:[TESTMD,0053]Enter in test mode? yes/no
2020-02-05T15:41:27:[TESTMD,0252]0051>
2020-02-05T15:41:29:[TESTMD,0050]"yes"
2020-02-05T15:41:29:[TESTMD,0249]
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


2020-02-05T15:41:29:[TESTMD,0252]0051>
2020-02-05T15:41:34:[TESTMD,0050]"act"
2020-02-05T15:41:34:[SURFIN,0020]filling external bladder
2020-02-05T15:41:42:[PUMP  ,0207]pump warmup 15117mV/53070uA
2020-02-05T15:41:42:[PUMP  ,0016]pump during 300000ms
2020-02-05T15:41:47:[PUMP  ,0212]pump stopped, 13010mV/1470222uA
2020-02-05T15:41:47:[PUMP  ,0210]aborted, 29500ticks remain
2020-02-05T15:41:49:[SURFIN,0019]external bladder full
2020-02-05T15:41:54:[VALVE ,0034]valve opening 30000ms
2020-02-05T15:42:24:[VALVE ,0234]closed 14333mV/600118uA
2020-02-05T15:42:29:[SURFIN,0020]filling external bladder
2020-02-05T15:42:37:[PUMP  ,0207]pump warmup 15095mV/52948uA
2020-02-05T15:42:37:[PUMP  ,0016]pump during 300000ms
2020-02-05T15:42:44:[PUMP  ,0212]pump stopped, 13873mV/1500795uA
2020-02-05T15:42:44:[PUMP  ,0210]aborted, 29400ticks remain
2020-02-05T15:42:46:[SURFIN,0019]external bladder full
2020-02-05T15:42:46:[TESTMD,0045]pump run 7s
2020-02-05T15:42:51:[BYPASS,0035]bypass opening 30000ms
2020-02-05T15:42:56:[BYPASS,0104]bypass opening: 14641mV/360754uA
2020-02-05T15:43:31:[BYPASS,0106]bypass closing: 14587mV/396866uA
2020-02-05T15:43:36:[SURFIN,0020]filling external bladder
2020-02-05T15:43:44:[PUMP  ,0207]pump warmup 15096mV/49776uA
2020-02-05T15:43:44:[PUMP  ,0016]pump during 300000ms
2020-02-05T15:45:07:[PUMP  ,0212]pump stopped, 13968mV/1462897uA
2020-02-05T15:45:07:[PUMP  ,0210]aborted, 22100ticks remain
2020-02-05T15:45:09:[SURFIN,0019]external bladder full
2020-02-05T15:45:09:[TESTMD,0045]pump run 83s
2020-02-05T15:45:14:[TESTMD,0066]test done
2020-02-05T15:45:14:[TESTMD,0252]0051>
2020-02-05T15:45:23:[TESTMD,0050]"gps"
2020-02-05T15:45:31:[SURF  ,0022]GPS fix...
2020-02-05T15:45:32:<WARN>[GPSFIX,0122]GPRMC no fix #0
2020-02-05T15:45:57:<WARN>[GPSFIX,0123]GPRMC ms=500 #1
2020-02-05T15:46:19:[SURF  ,0015]10 PPS detected...
2020-02-05T15:46:21:[MRMAID,0052]Mermaid $GPSACK:+50,+1,+4,+15,+40,-27,-478637;
2020-02-05T15:46:31:[MRMAID,0052]Mermaid $GPSOFF:3686319;
2020-02-05T15:46:32:[GPSFIX,0179]-1s diff
2020-02-05T15:46:33:[SURF  ,0222]2020-02-05T15:46:33
2020-02-05T15:46:33:[SURF  ,0082]Latitude : N43deg06.487mn, Longitude :E006deg02.286mn
2020-02-05T15:46:33:[SURF  ,0223]fix3D,6satellites
2020-02-05T15:46:33:[SURF  ,0084]GPS fix GPGSA : hdop0.840,vdop1.250
2020-02-05T15:46:48:[TESTMD,0252]0051>
2020-02-05T15:46:50:[TESTMD,0050]"gps"
2020-02-05T15:46:59:[SURF  ,0022]GPS fix...
2020-02-05T15:47:20:[SURF  ,0015]10 PPS detected...
2020-02-05T15:47:21:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-02-05T15:47:31:[MRMAID,0052]Mermaid $GPSOFF:3686319;
2020-02-05T15:47:33:[GPSFIX,0179]-1s diff
2020-02-05T15:47:34:[SURF  ,0222]2020-02-05T15:47:34
2020-02-05T15:47:34:[SURF  ,0082]Latitude : N43deg06.485mn, Longitude :E006deg02.286mn
2020-02-05T15:47:34:[SURF  ,0223]fix3D,6satellites
2020-02-05T15:47:34:[SURF  ,0084]GPS fix GPGSA : hdop0.850,vdop1.250
2020-02-05T15:47:49:[TESTMD,0252]0051>
2020-02-05T15:47:53:[TESTMD,0050]"iridium"
2020-02-05T15:48:04:[SURF  ,0025]Iridium...
