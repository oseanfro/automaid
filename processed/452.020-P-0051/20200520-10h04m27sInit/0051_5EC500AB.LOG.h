2020-05-20T10:04:27:[MONITR,0197]reboot code 0x0000, src/monitor.c@520
2020-05-20T10:04:27:[MAIN  ,0007]buoy 452.020-P-0051
2020-05-20T10:04:27:[MAIN  ,0055]soft pilotage 452.012.300_V2.18-20200518
2020-05-20T10:04:27:[MAIN  ,0011]date 2020-05-20T10:04:27
2020-05-20T10:04:33:[MAIN  ,0006]battery 15228mV,   14396uA
2020-05-20T10:04:36:[MAIN  ,0024]internal pressure 81490Pa
2020-05-20T10:04:37:[PRESS ,0038]P   -125mbar,T+24251mdegC
2020-05-20T10:04:37:[MRMAID,0182]thread started
2020-05-20T10:04:39:[MRMAID,0186]no wake-up
2020-05-20T10:04:40:[MRMAID,0188]acq already stopped
2020-05-20T10:04:40:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-05-20T10:04:41:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-05-20T10:04:41:[TESTMD,0053]Enter in test mode? yes/no
2020-05-20T10:04:41:[TESTMD,0252]0051>
2020-05-20T10:04:46:[TESTMD,0050]"yes"
2020-05-20T10:04:46:[TESTMD,0249]
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
mchecksd  : Start mermaid acq
mdump  : Send data REQUEST command with date and duration
s41dumpa : Get averaged CTD datas
s41dumpr : Get raw CTD datas
ls      : List files
cp      : Copy file or directory content on the desktop
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


2020-05-20T10:04:46:[TESTMD,0252]0051>
2020-05-20T10:05:21:[TESTMD,0050]"pint"
2020-05-20T10:05:23:[TESTMD,0029]81528Pa
2020-05-20T10:05:23:[TESTMD,0252]0051>
2020-05-20T10:05:32:[TESTMD,0050]"ui"
2020-05-20T10:05:35:[MAIN  ,0006]battery 15230mV,   15128uA
2020-05-20T10:05:36:[TESTMD,0252]0051>
2020-05-20T10:06:02:[TESTMD,0050]"act"
2020-05-20T10:06:02:[SURFIN,0020]filling external bladder
2020-05-20T10:06:05:[SURFIN,0019]external bladder full
2020-05-20T10:06:10:[VALVE ,0034]valve opening 30000ms
2020-05-20T10:06:45:[SURFIN,0020]filling external bladder
2020-05-20T10:06:53:[PUMP  ,0016]pump during 300000ms
2020-05-20T10:07:02:[SURFIN,0019]external bladder full
2020-05-20T10:07:02:[TESTMD,0045]pump run 7s
2020-05-20T10:07:07:[BYPASS,0035]bypass opening 30000ms
2020-05-20T10:07:52:[SURFIN,0020]filling external bladder
2020-05-20T10:08:00:[PUMP  ,0016]pump during 300000ms
2020-05-20T10:09:17:[SURFIN,0019]external bladder full
2020-05-20T10:09:17:[TESTMD,0045]pump run 75s
2020-05-20T10:09:22:[TESTMD,0066]test done
2020-05-20T10:09:22:[TESTMD,0252]0051>
2020-05-20T10:09:53:[TESTMD,0050]"gps"
2020-05-20T10:10:00:[SURF  ,0022]GPS fix...
2020-05-20T10:10:26:<WARN>[GPSFIX,0123]GPRMC ms=10 #1
2020-05-20T10:10:50:[SURF  ,0015]10 PPS detected...
2020-05-20T10:10:52:[MRMAID,0052]Mermaid $GPSACK:+50,+4,+19,+10,+3,+17,-343078;
2020-05-20T10:11:02:[MRMAID,0052]Mermaid $GPSOFF:3686317;
2020-05-20T10:11:04:[GPSFIX,0179]-1s diff
2020-05-20T10:11:05:[SURF  ,0222]2020-05-20T10:11:05
2020-05-20T10:11:05:[SURF  ,0082]Latitude : N43deg41.954mn, Longitude :E007deg18.523mn
2020-05-20T10:11:05:[SURF  ,0223]fix3D,6satellites
2020-05-20T10:11:05:[SURF  ,0084]GPS fix GPGSA : hdop1.000,vdop1.540
2020-05-20T10:11:20:[TESTMD,0252]0051>
2020-05-20T10:11:26:[TESTMD,0050]"gps"
2020-05-20T10:11:37:[SURF  ,0022]GPS fix...
2020-05-20T10:11:57:[SURF  ,0015]10 PPS detected...
2020-05-20T10:11:58:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-05-20T10:12:08:[MRMAID,0052]Mermaid $GPSOFF:3686317;
2020-05-20T10:12:10:[GPSFIX,0179]+0s diff
2020-05-20T10:12:10:[SURF  ,0222]2020-05-20T10:12:10
2020-05-20T10:12:10:[SURF  ,0082]Latitude : N43deg41.954mn, Longitude :E007deg18.524mn
2020-05-20T10:12:10:[SURF  ,0223]fix3D,6satellites
2020-05-20T10:12:10:[SURF  ,0084]GPS fix GPGSA : hdop0.870,vdop1.170
2020-05-20T10:12:25:[TESTMD,0252]0051>
2020-05-20T10:12:34:[TESTMD,0050]"iridium"
2020-05-20T10:12:46:[SURF  ,0025]Iridium...
2020-05-20T10:13:28:[SURF  ,0009]connected in 42s, signal quality 5
2020-05-20T10:14:28:[SURF  ,0218]prompt received, remote cmd end
2020-05-20T10:14:28:[SURF  ,0012]12 cmd(s) received
2020-05-20T10:14:48:[UPLOAD,0248]Upload data files...
2020-05-20T10:15:28:<ERR>[UPLOAD,0131]opening upload
2020-05-20T10:15:28:<ERR>[UPLOAD,0132]opening upload "0051"
2020-05-20T10:15:47:[SURF  ,0014]disconnected after 181s
2020-05-20T10:15:52:[TESTMD,0252]0051>
2020-05-20T10:17:47:[TESTMD,0050]"cp0051"
2020-05-20T10:17:53:[TESTMD,0252]0051>
