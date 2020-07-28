2020-02-11T17:41:40:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-02-11T17:41:40:[MAIN  ,0007]buoy 452.020-P-0051
2020-02-11T17:41:40:[MAIN  ,0055]soft pilotage 452.012.300_V2.11-20200211
2020-02-11T17:41:40:[MAIN  ,0011]date 2020-02-11T17:41:40
2020-02-11T17:41:46:[MAIN  ,0006]battery 15302mV,   14152uA
2020-02-11T17:41:48:[MAIN  ,0024]internal pressure 79399Pa
2020-02-11T17:41:50:[PRESS ,0038]P    -29mbar,T+17660mdegC
2020-02-11T17:41:50:[MRMAID,0182]thread started
2020-02-11T17:41:51:[MRMAID,0186]no wake-up
2020-02-11T17:41:52:[MRMAID,0188]acq already stopped
2020-02-11T17:41:53:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-02-11T17:41:53:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-02-11T17:41:54:[TESTMD,0053]Enter in test mode? yes/no
2020-02-11T17:41:54:[TESTMD,0252]0051>
2020-02-11T17:41:55:[TESTMD,0050]"yes"
2020-02-11T17:41:56:[TESTMD,0249]
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


2020-02-11T17:41:56:[TESTMD,0252]0051>
2020-02-11T17:41:58:[TESTMD,0050]"pext"
2020-02-11T17:42:02:[PRESS ,0038]P    -29mbar,T+17659mdegC
2020-02-11T17:42:02:[TESTMD,0252]0051>
2020-02-11T17:42:07:[TESTMD,0050]"pint"
2020-02-11T17:42:09:[TESTMD,0029]79382Pa
2020-02-11T17:42:09:[TESTMD,0252]0051>
2020-02-11T17:45:18:[TESTMD,0050]"act"
2020-02-11T17:45:18:[SURFIN,0020]filling external bladder
2020-02-11T17:45:27:[PUMP  ,0207]pump warmup 15067mV/49166uA
2020-02-11T17:45:27:[PUMP  ,0016]pump during 300000ms
2020-02-11T17:46:03:[PUMP  ,0212]pump stopped, 13487mV/1506768uA
2020-02-11T17:46:03:[PUMP  ,0210]aborted, 26500ticks remain
2020-02-11T17:46:05:[SURFIN,0019]external bladder full
2020-02-11T17:46:10:[VALVE ,0034]valve opening 30000ms
2020-02-11T17:46:40:[VALVE ,0234]closed 14440mV/605608uA
2020-02-11T17:46:45:[SURFIN,0020]filling external bladder
2020-02-11T17:46:54:[PUMP  ,0207]pump warmup 14977mV/49654uA
2020-02-11T17:46:54:[PUMP  ,0016]pump during 300000ms
2020-02-11T17:47:06:[PUMP  ,0212]pump stopped, 14101mV/1510892uA
2020-02-11T17:47:06:[PUMP  ,0210]aborted, 28800ticks remain
2020-02-11T17:47:08:[SURFIN,0019]external bladder full
2020-02-11T17:47:08:[TESTMD,0045]pump run 13s
2020-02-11T17:47:13:[BYPASS,0035]bypass opening 30000ms
2020-02-11T17:47:18:[BYPASS,0104]bypass opening: 14645mV/366854uA
2020-02-11T17:47:53:[BYPASS,0106]bypass closing: 14572mV/401258uA
2020-02-11T17:47:58:[SURFIN,0020]filling external bladder
2020-02-11T17:48:07:[PUMP  ,0207]pump warmup 14967mV/49288uA
2020-02-11T17:48:07:[PUMP  ,0016]pump during 300000ms
2020-02-11T17:49:24:[PUMP  ,0212]pump stopped, 14073mV/1493074uA
2020-02-11T17:49:24:[PUMP  ,0210]aborted, 22600ticks remain
2020-02-11T17:49:26:[SURFIN,0019]external bladder full
2020-02-11T17:49:26:[TESTMD,0045]pump run 78s
2020-02-11T17:49:31:[TESTMD,0066]test done
2020-02-11T17:49:31:[TESTMD,0252]0051>
2020-02-11T17:50:13:[TESTMD,0050]"gps"
2020-02-11T17:50:20:[SURF  ,0022]GPS fix...
2020-02-11T17:50:21:<WARN>[GPSFIX,0123]GPRMC ms=140 #1
2020-02-11T17:50:22:<WARN>[GPSFIX,0122]GPRMC no fix #0
2020-02-11T17:50:49:<WARN>[GPSFIX,0123]GPRMC ms=10 #1
2020-02-11T17:51:09:[SURF  ,0015]10 PPS detected...
2020-02-11T17:51:11:[MRMAID,0052]Mermaid $GPSACK:+50,+1,+10,+17,+40,-14,-561187;
2020-02-11T17:51:21:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-11T17:51:22:[GPSFIX,0179]+1s diff
2020-02-11T17:51:21:[SURF  ,0222]2020-02-11T17:51:21
2020-02-11T17:51:21:[SURF  ,0082]Latitude : N43deg06.483mn, Longitude :E006deg02.286mn
2020-02-11T17:51:21:[SURF  ,0223]fix3D,7satellites
2020-02-11T17:51:21:[SURF  ,0084]GPS fix GPGSA : hdop1.030,vdop1.000
2020-02-11T17:51:36:[TESTMD,0252]0051>
2020-02-11T17:52:01:[TESTMD,0050]"gps"
2020-02-11T17:52:10:[SURF  ,0022]GPS fix...
2020-02-11T17:52:30:[SURF  ,0015]10 PPS detected...
2020-02-11T17:52:31:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,-1,+0;
2020-02-11T17:52:41:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-11T17:52:42:[GPSFIX,0179]-1s diff
2020-02-11T17:52:43:[SURF  ,0222]2020-02-11T17:52:43
2020-02-11T17:52:43:[SURF  ,0082]Latitude : N43deg06.482mn, Longitude :E006deg02.289mn
2020-02-11T17:52:43:[SURF  ,0223]fix3D,7satellites
2020-02-11T17:52:43:[SURF  ,0084]GPS fix GPGSA : hdop1.110,vdop1.050
2020-02-11T17:52:58:[TESTMD,0252]0051>
2020-02-11T17:53:05:[TESTMD,0050]"iridium"
2020-02-11T17:53:17:[SURF  ,0025]Iridium...
2020-02-11T17:53:56:[SURF  ,0009]connected in 39s, signal quality 5
2020-02-11T17:54:26:<WARN>[SURF  ,0071]timeout
2020-02-11T17:54:26:<WARN>[SURF  ,0056]peer mute
2020-02-11T17:54:36:[SURF  ,0014]disconnected after 79s
2020-02-11T17:54:41:[TESTMD,0252]0051>
2020-02-11T17:54:51:[TESTMD,0050]"iridium"
2020-02-11T17:55:02:[SURF  ,0025]Iridium...
2020-02-11T17:56:19:[SURF  ,0009]connected in 77s, signal quality 5
2020-02-11T17:56:46:[BYCMD ,0120]    bypass 10000ms 100000ms (20000ms 60000ms stored)
2020-02-11T17:56:48:[BYCMD ,0125]    near 1500mbar 3mbar/s (15000mbar 3mbar/s stored)
2020-02-11T17:56:49:[BYCMD ,0126]    far 2500mbar 4mbar/s (25000mbar 4mbar/s stored)
2020-02-11T17:56:50:[BYCMD ,0128]    dead 60s (300s stored)
2020-02-11T17:56:52:[P2TCMD,0155]p2t log dp > 50mbar
2020-02-11T17:56:56:[STACMD,0168]stage del 0
2020-02-11T17:56:57:[STACMD,0170]stage store 0
2020-02-11T17:57:07:[SURF  ,0218]prompt received, remote cmd end
2020-02-11T17:57:07:[SURF  ,0012]7 cmd(s) received
2020-02-11T17:57:28:[UPLOAD,0248]Upload data files...
2020-02-11T17:57:48:[UPLOAD,0231]"0051/5E3D3A5D.BIN" uploaded at 104bytes/s
2020-02-11T17:58:08:[MAIN  ,0013]1 file(s) uploaded
2020-02-11T17:58:39:[SURF  ,0014]disconnected after 217s
2020-02-11T17:58:44:[TESTMD,0252]0051>
