2020-03-03T13:37:48:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-03-03T13:37:48:[MAIN  ,0007]buoy 452.020-P-0051
2020-03-03T13:37:48:[MAIN  ,0055]soft pilotage 452.012.300_V2.13-20200303
2020-03-03T13:37:48:[MAIN  ,0011]date 2020-03-03T13:37:48
2020-03-03T13:37:54:[MAIN  ,0006]battery 15295mV,   14518uA
2020-03-03T13:37:57:[MAIN  ,0024]internal pressure 78904Pa
2020-03-03T13:37:58:[PRESS ,0038]P   -109mbar,T+17242mdegC
2020-03-03T13:37:59:[MRMAID,0182]thread started
2020-03-03T13:38:00:[MRMAID,0186]no wake-up
2020-03-03T13:38:01:[MRMAID,0188]acq already stopped
2020-03-03T13:38:01:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-03-03T13:38:02:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-03-03T13:38:02:[TESTMD,0053]Enter in test mode? yes/no
2020-03-03T13:38:02:[TESTMD,0252]0051>
2020-03-03T13:38:07:[TESTMD,0050]"yes"
2020-03-03T13:38:07:[TESTMD,0249]
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
s41dumpa : Get averaged CTD datas
s41dumpr : Get raw CTD datas
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


2020-03-03T13:38:07:[TESTMD,0252]0051>
2020-03-03T13:38:47:[TESTMD,0050]"pint"
2020-03-03T13:38:49:[TESTMD,0029]78857Pa
2020-03-03T13:38:49:[TESTMD,0252]0051>
2020-03-03T13:38:58:[TESTMD,0050]"pext"
2020-03-03T13:39:02:[PRESS ,0038]P   -119mbar,T+17244mdegC
2020-03-03T13:39:02:[TESTMD,0252]0051>
2020-03-03T13:39:13:[TESTMD,0050]"featurehelp"
2020-03-03T13:39:13:[TESTMD,0252]0051>
2020-03-03T13:39:23:[TESTMD,0050]"featureactuiwatch1"
2020-03-03T13:39:23:[TESTMD,0252]0051>
2020-03-03T13:39:36:[TESTMD,0050]"act"
2020-03-03T13:39:36:[SURFIN,0020]filling external bladder
2020-03-03T13:39:44:[PUMP  ,0207]battery 15065mV,   49898uA (warmup), P   -119mbar
2020-03-03T13:39:44:[PUMP  ,0016]pump during 300000ms
2020-03-03T13:39:50:[PUMP  ,0212]battery 12418mV, 1455216uA (steady state), P   -119mbar
2020-03-03T13:39:52:[SURFIN,0019]external bladder full
2020-03-03T13:39:57:[VALVE ,0034]valve opening 30000ms
2020-03-03T13:40:27:[VALVE ,0234]battery 14092mV,  629764uA, P   -119mbar
2020-03-03T13:40:32:[SURFIN,0020]filling external bladder
2020-03-03T13:40:40:[PUMP  ,0207]battery 15102mV,   43188uA (warmup), P   -119mbar
2020-03-03T13:40:41:[PUMP  ,0016]pump during 300000ms
2020-03-03T13:40:48:[PUMP  ,0212]battery 13933mV, 1531344uA (steady state), P   -119mbar
2020-03-03T13:40:50:[SURFIN,0019]external bladder full
2020-03-03T13:40:50:[TESTMD,0045]pump run 8s
2020-03-03T13:40:55:[BYPASS,0035]bypass opening 30000ms
2020-03-03T13:41:00:[BYPASS,0104]battery 14642mV,  329766uA (bypass opening), P   -119mbar
2020-03-03T13:41:35:[BYPASS,0106]battery 14526mV,  411384uA (bypass closing), P   -119mbar
2020-03-03T13:41:40:[SURFIN,0020]filling external bladder
2020-03-03T13:41:48:[PUMP  ,0207]battery 15080mV,   43920uA (warmup), P   -119mbar
2020-03-03T13:41:48:[PUMP  ,0016]pump during 300000ms
2020-03-03T13:42:52:[PUMP  ,0212]battery 13933mV, 1543910uA (steady state), P   -119mbar
2020-03-03T13:42:54:[SURFIN,0019]external bladder full
2020-03-03T13:42:54:[TESTMD,0045]pump run 64s
2020-03-03T13:42:59:[TESTMD,0066]test done
2020-03-03T13:42:59:[TESTMD,0252]0051>
2020-03-03T13:43:11:[TESTMD,0050]"ui"
2020-03-03T13:43:13:[MAIN  ,0006]battery 14850mV,   12200uA
2020-03-03T13:43:13:[TESTMD,0252]0051>
2020-03-03T13:44:19:[TESTMD,0050]"gps"
2020-03-03T13:44:27:[SURF  ,0022]GPS fix...
2020-03-03T13:44:44:<WARN>[GPSFIX,0123]GPRMC ms=490 #1
2020-03-03T13:44:45:<WARN>[GPSFIX,0123]GPRMC ms=990 #1
2020-03-03T13:46:02:[SURF  ,0015]10 PPS detected...
2020-03-03T13:46:04:[MRMAID,0052]Mermaid $GPSACK:+50,+2,+2,+13,+37,-18,-297454;
2020-03-03T13:46:14:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-03-03T13:46:16:[GPSFIX,0179]+4s diff
2020-03-03T13:46:12:[SURF  ,0222]2020-03-03T13:46:12
2020-03-03T13:46:12:[SURF  ,0082]Latitude : N43deg06.487mn, Longitude :E006deg02.284mn
2020-03-03T13:46:12:[SURF  ,0223]fix3D,2satellites
2020-03-03T13:46:12:[SURF  ,0084]GPS fix GPGSA : hdop1.330,vdop2.500
2020-03-03T13:46:27:[TESTMD,0252]0051>
2020-03-03T13:46:46:[TESTMD,0050]"gps"
2020-03-03T13:46:56:[SURF  ,0022]GPS fix...
2020-03-03T13:47:16:[SURF  ,0015]10 PPS detected...
2020-03-03T13:47:17:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,-30;
2020-03-03T13:47:27:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-03-03T13:47:29:[GPSFIX,0179]+0s diff
2020-03-03T13:47:29:[SURF  ,0222]2020-03-03T13:47:29
2020-03-03T13:47:29:[SURF  ,0082]Latitude : N43deg06.484mn, Longitude :E006deg02.283mn
2020-03-03T13:47:29:[SURF  ,0223]fix3D,2satellites
2020-03-03T13:47:29:[SURF  ,0084]GPS fix GPGSA : hdop1.330,vdop2.470
2020-03-03T13:47:44:[TESTMD,0252]0051>
2020-03-03T13:48:06:[TESTMD,0050]"iridium"
2020-03-03T13:48:17:[SURF  ,0025]Iridium...
2020-03-03T13:49:06:[SURF  ,0009]connected in 49s, signal quality 5
2020-03-03T13:50:06:[SURF  ,0218]prompt received, remote cmd end
2020-03-03T13:50:06:[SURF  ,0012]8 cmd(s) received
2020-03-03T13:50:27:[UPLOAD,0248]Upload data files...
2020-03-03T13:51:49:[UPLOAD,0231]"0051/5E465099.BIN" uploaded at 151bytes/s
2020-03-03T13:52:05:[MAIN  ,0013]1 file(s) uploaded
2020-03-03T13:52:40:[SURF  ,0014]disconnected after 263s
2020-03-03T13:52:45:[TESTMD,0252]0051>
