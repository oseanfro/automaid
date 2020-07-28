2020-02-06T10:34:28:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-02-06T10:34:28:[MAIN  ,0007]buoy 452.020-P-0051
2020-02-06T10:34:28:[MAIN  ,0055]soft pilotage 452.012.300_V2.10-20200130
2020-02-06T10:34:28:[MAIN  ,0011]date 2020-02-06T10:34:28
2020-02-06T10:34:34:[MAIN  ,0006]battery 15308mV,   14640uA
2020-02-06T10:34:37:[MAIN  ,0024]internal pressure 79025Pa
2020-02-06T10:34:38:[PRESS ,0038]P    +90mbar,T+17230mdegC
2020-02-06T10:34:39:[MRMAID,0182]thread started
2020-02-06T10:34:40:[MRMAID,0186]no wake-up
2020-02-06T10:34:41:[MRMAID,0188]acq already stopped
2020-02-06T10:34:41:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-02-06T10:34:42:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-02-06T10:34:42:[TESTMD,0053]Enter in test mode? yes/no
2020-02-06T10:34:42:[TESTMD,0252]0051>
2020-02-06T10:34:45:[TESTMD,0050]"yes"
2020-02-06T10:34:45:[TESTMD,0249]
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


2020-02-06T10:34:45:[TESTMD,0252]0051>
2020-02-06T10:35:53:[TESTMD,0050]"pint"
2020-02-06T10:35:56:[TESTMD,0029]79041Pa
2020-02-06T10:35:56:[TESTMD,0252]0051>
2020-02-06T10:36:06:[TESTMD,0050]"pext"
2020-02-06T10:36:11:[PRESS ,0038]P    +90mbar,T+17232mdegC
2020-02-06T10:36:11:[TESTMD,0252]0051>
2020-02-06T10:36:18:[TESTMD,0050]"pext"
2020-02-06T10:36:23:[PRESS ,0038]P    +80mbar,T+17230mdegC
2020-02-06T10:36:23:[TESTMD,0252]0051>
2020-02-06T10:36:26:[TESTMD,0050]"gps"
2020-02-06T10:36:33:[SURF  ,0022]GPS fix...
2020-02-06T10:36:34:<WARN>[GPSFIX,0123]GPRMC ms=610 #1
2020-02-06T10:36:35:<WARN>[GPSFIX,0122]GPRMC no fix #0
2020-02-06T10:36:54:<WARN>[GPSFIX,0121]GPRMC #1
2020-02-06T10:37:20:[SURF  ,0015]10 PPS detected...
2020-02-06T10:37:21:[MRMAID,0052]Mermaid $GPSACK:+50,+1,+5,+10,+33,+15,-177398;
2020-02-06T10:37:31:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-06T10:37:34:[GPSFIX,0179]+0s diff
2020-02-06T10:37:34:[SURF  ,0222]2020-02-06T10:37:34
2020-02-06T10:37:34:[SURF  ,0082]Latitude : N43deg06.487mn, Longitude :E006deg02.283mn
2020-02-06T10:37:34:[SURF  ,0223]fix3D,4satellites
2020-02-06T10:37:34:[SURF  ,0084]GPS fix GPGSA : hdop1.470,vdop2.390
2020-02-06T10:37:49:[TESTMD,0252]0051>
2020-02-06T10:37:50:[TESTMD,0050]"u"
2020-02-06T10:37:50:[TESTMD,0008]command not supported
2020-02-06T10:37:50:[TESTMD,0252]0051>
2020-02-06T10:37:57:[TESTMD,0050]"U"
2020-02-06T10:37:57:[TESTMD,0008]command not supported
2020-02-06T10:37:57:[TESTMD,0252]0051>
2020-02-06T10:38:00:[TESTMD,0050]"gps"
2020-02-06T10:38:10:[SURF  ,0022]GPS fix...
2020-02-06T10:38:31:[SURF  ,0015]10 PPS detected...
2020-02-06T10:38:32:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,-30;
2020-02-06T10:38:42:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-06T10:38:45:[GPSFIX,0179]+0s diff
2020-02-06T10:38:45:[SURF  ,0222]2020-02-06T10:38:45
2020-02-06T10:38:45:[SURF  ,0082]Latitude : N43deg06.484mn, Longitude :E006deg02.288mn
2020-02-06T10:38:45:[SURF  ,0223]fix3D,4satellites
2020-02-06T10:38:45:[SURF  ,0084]GPS fix GPGSA : hdop1.470,vdop2.370
2020-02-06T10:39:00:[TESTMD,0252]0051>
2020-02-06T10:39:05:[TESTMD,0050]"ui"
2020-02-06T10:39:07:[MAIN  ,0006]battery 15276mV,   12688uA
2020-02-06T10:39:07:[TESTMD,0252]0051>
2020-02-06T10:39:14:[TESTMD,0050]"act"
2020-02-06T10:39:14:[SURFIN,0020]filling external bladder
2020-02-06T10:39:22:[PUMP  ,0207]pump warmup 15120mV/49898uA
2020-02-06T10:39:22:[PUMP  ,0016]pump during 300000ms
2020-02-06T10:39:30:[PUMP  ,0212]pump stopped, 13583mV/1419888uA
2020-02-06T10:39:31:[PUMP  ,0210]aborted, 29200ticks remain
2020-02-06T10:39:33:[SURFIN,0019]external bladder full
2020-02-06T10:39:38:[VALVE ,0034]valve opening 30000ms
2020-02-06T10:40:08:[VALVE ,0234]closed 14415mV/605120uA
2020-02-06T10:40:13:[SURFIN,0020]filling external bladder
2020-02-06T10:40:21:[PUMP  ,0207]pump warmup 15065mV/49776uA
2020-02-06T10:40:21:[PUMP  ,0016]pump during 300000ms
2020-02-06T10:40:30:[PUMP  ,0212]pump stopped, 13982mV/1466715uA
2020-02-06T10:40:30:[PUMP  ,0210]aborted, 29100ticks remain
2020-02-06T10:40:32:[SURFIN,0019]external bladder full
2020-02-06T10:40:32:[TESTMD,0045]pump run 9s
2020-02-06T10:40:37:[BYPASS,0035]bypass opening 30000ms
2020-02-06T10:40:42:[BYPASS,0104]bypass opening: 14658mV/370880uA
2020-02-06T10:41:17:[BYPASS,0106]bypass closing: 14573mV/401502uA
2020-02-06T10:41:22:[SURFIN,0020]filling external bladder
2020-02-06T10:41:31:[PUMP  ,0207]pump warmup 15032mV/49654uA
2020-02-06T10:41:31:[PUMP  ,0016]pump during 300000ms
2020-02-06T10:42:48:[PUMP  ,0212]pump stopped, 13970mV/1464662uA
2020-02-06T10:42:48:[PUMP  ,0210]aborted, 22600ticks remain
2020-02-06T10:42:50:[SURFIN,0019]external bladder full
2020-02-06T10:42:50:[TESTMD,0045]pump run 78s
2020-02-06T10:42:55:[TESTMD,0066]test done
2020-02-06T10:42:55:[TESTMD,0252]0051>
2020-02-06T10:43:09:[TESTMD,0050]"iridium"
2020-02-06T10:43:19:[SURF  ,0025]Iridium...
2020-02-06T10:45:46:[SURF  ,0009]connected in 146s, signal quality 3
2020-02-06T10:46:12:[BYCMD ,0120]    bypass 10000ms 100000ms (20000ms 60000ms stored)
2020-02-06T10:46:14:[BYCMD ,0125]    near 1500mbar 3mbar/s (15000mbar 3mbar/s stored)
2020-02-06T10:46:17:[BYCMD ,0126]    far 2500mbar 4mbar/s (25000mbar 4mbar/s stored)
2020-02-06T10:46:19:[BYCMD ,0128]    dead 60s (300s stored)
2020-02-06T10:46:21:[MRMAID,0052]Mermaid $TRIG:10,1;
2020-02-06T10:46:24:[MRMAID,0052]Mermaid $DTRIG:1,1;
2020-02-06T10:46:27:[MRMAID,0052]Mermaid $SCALES:2;
2020-02-06T10:46:29:[P2TCMD,0155]p2t log dp > 50mbar
2020-02-06T10:46:31:[STACMD,0168]stage del 0
2020-02-06T10:46:34:[STACMD,0170]stage store 0
2020-02-06T10:46:44:[SURF  ,0218]prompt received, remote cmd end
2020-02-06T10:46:44:[SURF  ,0012]10 cmd(s) received
2020-02-06T10:47:06:[UPLOAD,0248]Upload data files...
2020-02-06T10:47:18:[UPLOAD,0231]"0051/5E3AD277.BIN" uploaded at 81bytes/s
2020-02-06T10:47:30:[UPLOAD,0231]"0051/5E3AD865.BIN" uploaded at 98bytes/s
2020-02-06T10:47:46:[UPLOAD,0231]"0051/5E3AE219.BIN" uploaded at 109bytes/s
2020-02-06T10:48:03:[MAIN  ,0013]3 file(s) uploaded
2020-02-06T10:48:36:[SURF  ,0014]disconnected after 316s
2020-02-06T10:48:41:[TESTMD,0252]0051>
