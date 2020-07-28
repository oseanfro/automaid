2020-01-13T16:19:32:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-01-13T16:19:32:[MAIN  ,0007]buoy 452.020-P-0051
2020-01-13T16:19:32:[MAIN  ,0055]soft pilotage 452.012.300_V2.9-20200113
2020-01-13T16:19:33:[MAIN  ,0011]date 2020-01-13T16:19:33
2020-01-13T16:19:39:[MAIN  ,0006]battery 15385mV,   10858uA
2020-01-13T16:19:41:[MAIN  ,0024]internal pressure 80007Pa
2020-01-13T16:19:43:[PRESS ,0038]P-65535965mbar,T+20762mdegC
2020-01-13T16:19:43:[MRMAID,0182]thread started
2020-01-13T16:19:44:[MRMAID,0186]no wake-up
2020-01-13T16:19:45:[MRMAID,0188]acq already stopped
2020-01-13T16:19:45:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-01-13T16:19:46:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-01-13T16:19:46:[TESTMD,0053]Enter in test mode? yes/no
2020-01-13T16:19:46:[TESTMD,0252]0051>
2020-01-13T16:19:51:[TESTMD,0050]"yes"
2020-01-13T16:19:52:[TESTMD,0249]
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


2020-01-13T16:19:52:[TESTMD,0252]0051>
2020-01-13T16:19:58:[TESTMD,0050]"pint"
2020-01-13T16:20:00:[TESTMD,0029]80002Pa
2020-01-13T16:20:00:[TESTMD,0252]0051>
2020-01-13T16:21:46:[TESTMD,0050]"act"
2020-01-13T16:21:46:[SURFIN,0020]filling external bladder
2020-01-13T16:21:54:[PUMP  ,0016]pump during 300000ms
2020-01-13T16:22:50:[PUMP  ,0210]aborted, 24400ticks remain
2020-01-13T16:22:52:[SURFIN,0019]external bladder full
2020-01-13T16:22:57:[VALVE ,0034]valve opening 30000ms
2020-01-13T16:23:32:[SURFIN,0020]filling external bladder
2020-01-13T16:23:40:[PUMP  ,0016]pump during 300000ms
2020-01-13T16:23:54:[PUMP  ,0210]aborted, 28700ticks remain
2020-01-13T16:23:56:[SURFIN,0019]external bladder full
2020-01-13T16:23:56:[TESTMD,0045]pump run 14s
2020-01-13T16:24:01:[BYPASS,0035]bypass opening 30000ms
2020-01-13T16:24:41:[BYPASS,0105]bypass closed
2020-01-13T16:24:46:[SURFIN,0020]filling external bladder
2020-01-13T16:24:54:[PUMP  ,0016]pump during 300000ms
2020-01-13T16:26:26:[PUMP  ,0210]aborted, 20800ticks remain
2020-01-13T16:26:28:[SURFIN,0019]external bladder full
2020-01-13T16:26:28:[TESTMD,0045]pump run 92s
2020-01-13T16:26:33:[TESTMD,0066]test done
2020-01-13T16:26:33:[TESTMD,0252]0051>
2020-01-13T16:29:24:[TESTMD,0050]"ui"
2020-01-13T16:29:26:[MAIN  ,0006]battery 15051mV,   11712uA
2020-01-13T16:29:26:[TESTMD,0252]0051>
2020-01-13T16:31:29:[TESTMD,0050]"pext"
2020-01-13T16:31:33:[PRESS ,0038]P-65535915mbar,T+20830mdegC
2020-01-13T16:31:33:[TESTMD,0252]0051>
2020-01-13T16:31:50:[TESTMD,0050]"pext"
2020-01-13T16:31:54:[PRESS ,0038]P-65535925mbar,T+20828mdegC
2020-01-13T16:31:54:[TESTMD,0252]0051>
2020-01-13T16:34:42:[TESTMD,0050]"sysiridium0088160000544osean005eAN%"
2020-01-13T16:34:42:[SYSCMD,0261]iridium (Number:0088160000544 user:osean password:005eAN%)
2020-01-13T16:34:42:[SYSCMD,0267]iridium stored (Number:0088160000544 user:osean password:005eAN%)
2020-01-13T16:34:42:[TESTMD,0252]0051>
2020-01-13T16:35:22:[TESTMD,0050]"syspromptosean@mermaid:~>"
2020-01-13T16:35:22:[SYSCMD,0263]prompteur: osean@mermaid:~>
2020-01-13T16:35:22:[SYSCMD,0269]prompteur stored: osean@mermaid:~>
2020-01-13T16:35:23:[TESTMD,0252]0051>
2020-01-13T16:35:33:[TESTMD,0050]"sysstore"
2020-01-13T16:35:33:[SYSCMD,0265]sys param stored
2020-01-13T16:35:33:[TESTMD,0252]0051>
2020-01-13T16:37:45:[TESTMD,0050]"gps"
2020-01-13T16:37:53:[SURF  ,0022]GPS fix...
2020-01-13T16:37:53:<WARN>[GPSFIX,0122]GPRMC no fix #0
2020-01-13T16:37:54:<WARN>[GPSFIX,0123]GPRMC ms=420 #1
2020-01-13T16:38:24:<WARN>[GPSFIX,0123]GPRMC ms=10 #1
2020-01-13T16:38:44:[SURF  ,0015]10 PPS detected...
2020-01-13T16:38:46:[MRMAID,0052]Mermaid $GPSACK:+50,+0,+12,+16,+18,+1,-751525;
2020-01-13T16:38:56:[MRMAID,0052]Mermaid $GPSOFF:3686319;
2020-01-13T16:38:57:[GPSFIX,0179]-6s diff
2020-01-13T16:39:03:[SURF  ,0222]2020-01-13T16:39:03
2020-01-13T16:39:03:[SURF  ,0082]Latitude : N43deg06.481mn, Longitude :E006deg02.285mn
2020-01-13T16:39:03:[SURF  ,0223]fix3D,5satellites
2020-01-13T16:39:03:[SURF  ,0084]GPS fix GPGSA : hdop2.980,vdop1.840
2020-01-13T16:39:18:[TESTMD,0252]0051>
2020-01-13T16:40:52:[TESTMD,0050]"help"
2020-01-13T16:40:52:[TESTMD,0249]
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


2020-01-13T16:40:52:[TESTMD,0252]0051>
2020-01-13T16:40:56:[TESTMD,0050]"gps"
2020-01-13T16:41:05:[SURF  ,0022]GPS fix...
2020-01-13T16:41:25:[SURF  ,0015]10 PPS detected...
2020-01-13T16:41:26:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-01-13T16:41:36:[MRMAID,0052]Mermaid $GPSOFF:3686319;
2020-01-13T16:41:38:[GPSFIX,0179]-1s diff
2020-01-13T16:41:39:[SURF  ,0222]2020-01-13T16:41:39
2020-01-13T16:41:39:[SURF  ,0082]Latitude : N43deg06.486mn, Longitude :E006deg02.285mn
2020-01-13T16:41:39:[SURF  ,0223]fix3D,5satellites
2020-01-13T16:41:39:[SURF  ,0084]GPS fix GPGSA : hdop2.020,vdop1.650
2020-01-13T16:41:54:[TESTMD,0252]0051>
2020-01-13T16:42:14:[TESTMD,0050]"iridium"
2020-01-13T16:42:22:[SURF  ,0025]Iridium...
2020-01-13T16:44:13:[SURF  ,0009]connected in 110s, signal quality 4
2020-01-13T16:44:47:<WARN>[SURF  ,0071]timeout
2020-01-13T16:44:47:<WARN>[SURF  ,0056]peer mute
2020-01-13T16:44:57:[SURF  ,0014]disconnected after 154s
2020-01-13T16:45:02:[TESTMD,0252]0051>
2020-01-13T16:45:05:[TESTMD,0050]"iridium"
2020-01-13T16:45:13:[SURF  ,0025]Iridium...
2020-01-13T16:45:58:[SURF  ,0009]connected in 44s, signal quality 2
2020-01-13T16:46:21:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:24:[BUOY  ,0083]Default parameters restored
2020-01-13T16:46:25:[BYCMD ,0136]    default: 0
2020-01-13T16:46:25:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:26:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:28:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:29:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:30:<WARN>[SURF  ,0018]64 received
2020-01-13T16:46:50:<WARN>[SURF  ,0071]timeout
2020-01-13T16:46:50:<WARN>[SURF  ,0056]peer mute
2020-01-13T16:47:00:[SURF  ,0014]disconnected after 106s
2020-01-13T16:47:05:[TESTMD,0252]0051>
2020-01-13T16:47:07:[TESTMD,0050]"iridium"
2020-01-13T16:47:16:[SURF  ,0025]Iridium...
2020-01-13T16:52:05:[SURF  ,0009]connected in 289s, signal quality 1
2020-01-13T16:52:31:[SURF  ,0218]prompt received, remote cmd end
2020-01-13T16:52:32:[SURF  ,0012]0 cmd(s) received
2020-01-13T16:52:49:[UPLOAD,0248]Upload data files...
2020-01-13T16:53:04:[ZIO   ,0240]"NO CARRIER" received, aborting
2020-01-13T16:53:04:<ERR>[UPLOAD,0131]opening upload
2020-01-13T16:53:04:<ERR>[UPLOAD,0132]opening upload "0051"
2020-01-13T16:53:20:[SURF  ,0014]disconnected after 364s
2020-01-13T16:53:25:[TESTMD,0252]0051>
2020-01-13T16:53:32:[TESTMD,0050]"iridium"
2020-01-13T16:53:43:[SURF  ,0025]Iridium...
2020-01-13T16:54:40:[SURF  ,0009]connected in 57s, signal quality 5
2020-01-13T16:55:25:<WARN>[SURF  ,0071]timeout
2020-01-13T16:55:25:<WARN>[SURF  ,0056]peer mute
2020-01-13T16:55:30:[SURF  ,0014]disconnected after 107s
2020-01-13T16:55:35:[TESTMD,0252]0051>
2020-01-13T16:55:41:[TESTMD,0050]"iridium"
2020-01-13T16:55:52:[SURF  ,0025]Iridium...
2020-01-13T16:57:04:<WARN>[SURF  ,0023]failed to connect #1, code -5, net 4, qual -1, dial -1
2020-01-13T16:58:24:<WARN>[SURF  ,0023]failed to connect #2, code -5, net 4, qual -1, dial -1
2020-01-13T16:59:44:<WARN>[SURF  ,0023]failed to connect #3, code -5, net 4, qual -1, dial -1
2020-01-13T17:02:19:[SURF  ,0009]connected in 387s, signal quality 1
2020-01-13T17:02:43:[BUOY  ,0083]Default parameters restored
2020-01-13T17:02:43:[BYCMD ,0136]    default: 0
2020-01-13T17:02:45:[BYCMD ,0135]    store: 102
2020-01-13T17:02:57:<WARN>[SURF  ,0071]timeout
2020-01-13T17:02:57:<WARN>[SURF  ,0056]peer mute
2020-01-13T17:03:02:[SURF  ,0014]disconnected after 430s
2020-01-13T17:03:08:[TESTMD,0252]0051>
2020-01-13T17:03:09:[TESTMD,0050]"iridium"
2020-01-13T17:03:20:[SURF  ,0025]Iridium...
2020-01-13T17:04:30:[SURF  ,0009]connected in 70s, signal quality 3
2020-01-13T17:05:24:<WARN>[SURF  ,0071]timeout
2020-01-13T17:05:24:<WARN>[SURF  ,0056]peer mute
2020-01-13T17:05:34:[SURF  ,0014]disconnected after 134s
2020-01-13T17:05:39:[TESTMD,0252]0051>
2020-01-13T17:05:47:[TESTMD,0050]"iridium"
2020-01-13T17:05:57:[SURF  ,0025]Iridium...
2020-01-13T17:07:10:<WARN>[SURF  ,0023]failed to connect #1, code -5, net 4, qual -1, dial -1
2020-01-13T17:08:23:[SURF  ,0009]connected in 146s, signal quality 5
2020-01-13T17:08:52:[BUOY  ,0083]Default parameters restored
2020-01-13T17:08:52:[BYCMD ,0136]    default: 0
2020-01-13T17:09:02:[BYCMD ,0135]    store: 102
2020-01-13T17:09:04:[BYCMD ,0120]    bypass 10000ms 100000ms (20000ms 60000ms stored)
2020-01-13T17:09:09:[BYCMD ,0125]    near 1500mbar 3mbar/s (15000mbar 3mbar/s stored)
2020-01-13T17:09:11:[BYCMD ,0126]    far 2500mbar 4mbar/s (25000mbar 4mbar/s stored)
2020-01-13T17:09:13:[BYCMD ,0128]    dead 60s (300s stored)
2020-01-13T17:09:15:[MRMAID,0052]Mermaid $TRIG:10,1;
2020-01-13T17:09:18:[MRMAID,0052]Mermaid $DTRIG:1,1;
2020-01-13T17:09:23:[MRMAID,0052]Mermaid $SCALES:2;
2020-01-13T17:09:25:[P2TCMD,0155]p2t log dp > 50mbar
2020-01-13T17:09:32:[STACMD,0168]stage del 0
2020-01-13T17:09:35:[STAGE ,0080]Stage [0] 3000mbar (+/-500mbar) 1200s (<1200s)
2020-01-13T17:09:45:<WARN>[SURF  ,0071]timeout
2020-01-13T17:09:45:<WARN>[SURF  ,0056]peer mute
2020-01-13T17:09:50:[SURF  ,0014]disconnected after 233s
2020-01-13T17:09:55:[TESTMD,0252]0051>
