2020-06-12T12:27:07:[MONITR,0197]reboot code 0x0000, src/monitor.c@520
2020-06-12T12:27:07:[MAIN  ,0007]buoy 452.020-P-0051
2020-06-12T12:27:07:[MAIN  ,0055]soft pilotage 452.012.300_V2.20-20200612
2020-06-12T12:27:07:[MAIN  ,0011]date 2020-06-12T12:27:07
2020-06-12T12:27:13:[MAIN  ,0006]battery 15320mV,   14030uA
2020-06-12T12:27:16:[MAIN  ,0024]internal pressure 80535Pa
2020-06-12T12:27:17:[PRESS ,0038]P    -53mbar,T+23103mdegC
2020-06-12T12:27:17:[MRMAID,0182]thread started
2020-06-12T12:27:18:[MRMAID,0186]no wake-up
2020-06-12T12:27:19:[MRMAID,0188]acq already stopped
2020-06-12T12:27:20:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-06-12T12:27:21:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-06-12T12:27:21:[TESTMD,0053]Enter in test mode? yes/no
2020-06-12T12:27:21:[TESTMD,0252]0051>
2020-06-12T12:27:23:[TESTMD,0050]"yes"
2020-06-12T12:27:23:[TESTMD,0249]
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


2020-06-12T12:27:23:[TESTMD,0252]0051>
2020-06-12T12:30:29:[TESTMD,0050]"act"
2020-06-12T12:30:29:[SURFIN,0020]filling external bladder
2020-06-12T12:30:37:[PUMP  ,0016]pump during 300000ms
2020-06-12T12:30:48:[SURFIN,0019]external bladder full
2020-06-12T12:30:53:[VALVE ,0034]valve opening 30000ms
2020-06-12T12:31:28:[SURFIN,0020]filling external bladder
2020-06-12T12:31:36:[PUMP  ,0016]pump during 300000ms
2020-06-12T12:31:49:[SURFIN,0019]external bladder full
2020-06-12T12:31:49:[TESTMD,0045]pump run 11s
2020-06-12T12:31:54:[BYPASS,0035]bypass opening 30000ms
2020-06-12T12:32:39:[SURFIN,0020]filling external bladder
2020-06-12T12:32:48:[PUMP  ,0016]pump during 300000ms
2020-06-12T12:34:13:[SURFIN,0019]external bladder full
2020-06-12T12:34:13:[TESTMD,0045]pump run 84s
2020-06-12T12:34:18:[TESTMD,0066]test done
2020-06-12T12:34:18:[TESTMD,0252]0051>
2020-06-12T12:36:07:[TESTMD,0050]"gps"
2020-06-12T12:36:15:[SURF  ,0022]GPS fix...
2020-06-12T12:36:53:<WARN>[GPSFIX,0123]GPRMC ms=500 #1
2020-06-12T12:37:20:[SURF  ,0015]10 PPS detected...
2020-06-12T12:37:21:[MRMAID,0052]Mermaid $GPSACK:+50,+5,+11,+12,+26,-12,-375396;
2020-06-12T12:37:31:[MRMAID,0052]Mermaid $GPSOFF:3686318;
2020-06-12T12:37:33:[GPSFIX,0179]+0s diff
2020-06-12T12:37:33:[SURF  ,0222]2020-06-12T12:37:33
2020-06-12T12:37:33:[SURF  ,0082]Latitude : N43deg06.480mn, Longitude :E006deg02.287mn
2020-06-12T12:37:33:[SURF  ,0223]fix3D,7satellites
2020-06-12T12:37:33:[SURF  ,0084]GPS fix GPGSA : hdop0.980,vdop1.520
2020-06-12T12:37:48:[TESTMD,0252]0051>
2020-06-12T12:38:02:[TESTMD,0050]"gps"
2020-06-12T12:38:12:[SURF  ,0022]GPS fix...
2020-06-12T12:38:32:[SURF  ,0015]10 PPS detected...
2020-06-12T12:38:33:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-06-12T12:38:43:[MRMAID,0052]Mermaid $GPSOFF:3686318;
2020-06-12T12:38:45:[GPSFIX,0179]-1s diff
2020-06-12T12:38:46:[SURF  ,0222]2020-06-12T12:38:46
2020-06-12T12:38:46:[SURF  ,0082]Latitude : N43deg06.483mn, Longitude :E006deg02.287mn
2020-06-12T12:38:46:[SURF  ,0223]fix3D,7satellites
2020-06-12T12:38:46:[SURF  ,0084]GPS fix GPGSA : hdop0.830,vdop1.150
2020-06-12T12:39:01:[TESTMD,0252]0051>
2020-06-12T12:39:42:[TESTMD,0050]"iridium"
2020-06-12T12:39:53:[SURF  ,0025]Iridium...
2020-06-12T12:40:50:[SURF  ,0009]connected in 57s, signal quality 5
2020-06-12T12:41:09:<WARN>[SURF  ,0058]read error -1
2020-06-12T12:41:19:<WARN>[SURF  ,0071]timeout
2020-06-12T12:41:19:<WARN>[SURF  ,0056]peer mute
2020-06-12T12:41:25:[SURF  ,0014]disconnected after 92s
2020-06-12T12:41:30:[TESTMD,0252]0051>
2020-06-12T12:41:57:[TESTMD,0050]"iridium"
2020-06-12T12:42:09:[SURF  ,0025]Iridium...
2020-06-12T12:42:51:[SURF  ,0009]connected in 42s, signal quality 3
2020-06-12T12:44:08:[SURF  ,0218]prompt received, remote cmd end
2020-06-12T12:44:08:[SURF  ,0012]14 cmd(s) received
2020-06-12T12:44:29:[UPLOAD,0248]Upload data files...
2020-06-12T12:45:00:[UPLOAD,0231]"0051/5ED64D70.MER" uploaded at 103bytes/s
2020-06-12T12:45:13:[UPLOAD,0231]"0051/5EDA1519.BIN" uploaded at 85bytes/s
2020-06-12T12:48:19:[UPLOAD,0231]"0051/5ED62E7F.BIN" uploaded at 129bytes/s
2020-06-12T12:48:45:[UPLOAD,0231]"0051/5EDA15D7.BIN" uploaded at 98bytes/s
2020-06-12T12:49:11:[MAIN  ,0013]4 file(s) uploaded
2020-06-12T12:49:42:[SURF  ,0014]disconnected after 453s
2020-06-12T12:49:47:[TESTMD,0252]0051>
