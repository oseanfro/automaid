2020-06-05T09:52:23:[MONITR,0197]reboot code 0x0000, src/monitor.c@520
2020-06-05T09:52:23:[MAIN  ,0007]buoy 452.020-P-0051
2020-06-05T09:52:23:[MAIN  ,0055]soft pilotage 452.012.300_V2.18-20200518
2020-06-05T09:52:23:[MAIN  ,0011]date 2020-06-05T09:52:23
2020-06-05T09:52:29:[MAIN  ,0006]battery 15311mV,   13908uA
2020-06-05T09:52:32:[MAIN  ,0024]internal pressure 80299Pa
2020-06-05T09:52:33:[PRESS ,0038]P    -63mbar,T+22450mdegC
2020-06-05T09:52:33:[MRMAID,0182]thread started
2020-06-05T09:52:34:[MRMAID,0186]no wake-up
2020-06-05T09:52:35:[MRMAID,0188]acq already stopped
2020-06-05T09:52:36:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-06-05T09:52:37:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-06-05T09:52:37:[TESTMD,0053]Enter in test mode? yes/no
2020-06-05T09:52:37:[TESTMD,0252]0051>
2020-06-05T09:52:45:[TESTMD,0050]"yes"
2020-06-05T09:52:45:[TESTMD,0249]
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


2020-06-05T09:52:45:[TESTMD,0252]0051>
2020-06-05T09:54:30:[TESTMD,0050]"pint"
2020-06-05T09:54:32:[TESTMD,0029]80359Pa
2020-06-05T09:54:32:[TESTMD,0252]0051>
2020-06-05T09:54:41:[TESTMD,0050]"pint"
2020-06-05T09:54:43:[TESTMD,0029]80325Pa
2020-06-05T09:54:43:[TESTMD,0252]0051>
2020-06-05T09:55:03:[TESTMD,0050]"pext"
2020-06-05T09:55:07:[PRESS ,0038]P    -63mbar,T+22454mdegC
2020-06-05T09:55:07:[TESTMD,0252]0051>
2020-06-05T09:56:06:[TESTMD,0050]"ui"
2020-06-05T09:56:08:[MAIN  ,0006]battery 15331mV,   11590uA
2020-06-05T09:56:08:[TESTMD,0252]0051>
2020-06-05T09:56:27:[TESTMD,0050]"act"
2020-06-05T09:56:27:[SURFIN,0020]filling external bladder
2020-06-05T09:56:30:[SURFIN,0019]external bladder full
2020-06-05T09:56:35:[VALVE ,0034]valve opening 30000ms
2020-06-05T09:57:10:[SURFIN,0020]filling external bladder
2020-06-05T09:57:13:[SURFIN,0019]external bladder full
2020-06-05T09:57:13:<ERR>[TESTMD,0130]oil not transfered dt=-7s
2020-06-05T09:57:18:[BYPASS,0035]bypass opening 30000ms
2020-06-05T09:58:03:[SURFIN,0020]filling external bladder
2020-06-05T09:58:11:[PUMP  ,0016]pump during 300000ms
2020-06-05T09:59:34:[SURFIN,0019]external bladder full
2020-06-05T09:59:34:[TESTMD,0045]pump run 81s
2020-06-05T09:59:39:[TESTMD,0066]test done
2020-06-05T09:59:39:[TESTMD,0252]0051>
2020-06-05T09:59:50:[TESTMD,0050]"act"
2020-06-05T09:59:50:[SURFIN,0020]filling external bladder
2020-06-05T09:59:53:[SURFIN,0019]external bladder full
2020-06-05T09:59:58:[VALVE ,0034]valve opening 30000ms
2020-06-05T10:00:33:[SURFIN,0020]filling external bladder
2020-06-05T10:00:41:[PUMP  ,0016]pump during 300000ms
2020-06-05T10:00:57:[SURFIN,0019]external bladder full
2020-06-05T10:00:57:[TESTMD,0045]pump run 14s
2020-06-05T10:01:02:[BYPASS,0035]bypass opening 30000ms
2020-06-05T10:01:47:[SURFIN,0020]filling external bladder
2020-06-05T10:01:55:[PUMP  ,0016]pump during 300000ms
2020-06-05T10:03:19:[SURFIN,0019]external bladder full
2020-06-05T10:03:19:[TESTMD,0045]pump run 82s
2020-06-05T10:03:24:[TESTMD,0066]test done
2020-06-05T10:03:24:[TESTMD,0252]0051>
2020-06-05T10:04:18:[TESTMD,0050]"gps"
2020-06-05T10:04:25:[SURF  ,0022]GPS fix...
2020-06-05T10:04:27:<WARN>[GPSFIX,0123]GPRMC ms=720 #1
2020-06-05T10:05:26:<WARN>[GPSFIX,0123]GPRMC ms=500 #1
2020-06-05T10:05:52:<WARN>[GPSFIX,0121]GPRMC #1
2020-06-05T10:06:19:[SURF  ,0015]10 PPS detected...
2020-06-05T10:06:21:[MRMAID,0052]Mermaid $GPSACK:+50,+5,+4,+10,-8,-29,-199188;
2020-06-05T10:06:31:[MRMAID,0052]Mermaid $GPSOFF:3686318;
2020-06-05T10:06:32:[GPSFIX,0179]-1s diff
2020-06-05T10:06:33:[SURF  ,0222]2020-06-05T10:06:33
2020-06-05T10:06:33:[SURF  ,0082]Latitude : N43deg06.485mn, Longitude :E006deg02.283mn
2020-06-05T10:06:33:[SURF  ,0223]fix3D,5satellites
2020-06-05T10:06:33:[SURF  ,0084]GPS fix GPGSA : hdop1.310,vdop1.580
2020-06-05T10:06:48:[TESTMD,0252]0051>
2020-06-05T10:07:23:[TESTMD,0050]"gps"
2020-06-05T10:07:34:[SURF  ,0022]GPS fix...
2020-06-05T10:07:54:[SURF  ,0015]10 PPS detected...
2020-06-05T10:07:55:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-06-05T10:08:05:[MRMAID,0052]Mermaid $GPSOFF:3686318;
2020-06-05T10:08:06:[GPSFIX,0179]-1s diff
2020-06-05T10:08:07:[SURF  ,0222]2020-06-05T10:08:07
2020-06-05T10:08:07:[SURF  ,0082]Latitude : N43deg06.484mn, Longitude :E006deg02.288mn
2020-06-05T10:08:07:[SURF  ,0223]fix3D,6satellites
2020-06-05T10:08:07:[SURF  ,0084]GPS fix GPGSA : hdop1.250,vdop1.450
2020-06-05T10:08:22:[TESTMD,0252]0051>
2020-06-05T10:08:34:[TESTMD,0050]"iridium"
2020-06-05T10:08:45:[SURF  ,0025]Iridium...
2020-06-05T10:09:32:[SURF  ,0009]connected in 47s, signal quality 5
2020-06-05T10:10:02:[SURF  ,0218]prompt received, remote cmd end
2020-06-05T10:10:02:[SURF  ,0012]0 cmd(s) received
2020-06-05T10:10:18:[UPLOAD,0248]Upload data files...
2020-06-05T10:10:38:[ZIO   ,0240]"NO CARRIER" received, aborting
2020-06-05T10:10:38:<ERR>[UPLOAD,0131]opening upload
2020-06-05T10:10:38:<ERR>[UPLOAD,0132]opening upload "0051"
2020-06-05T10:10:53:[SURF  ,0014]disconnected after 128s
2020-06-05T10:10:58:[TESTMD,0252]0051>
2020-06-05T10:12:38:[TESTMD,0050]"ridium"
2020-06-05T10:12:38:[TESTMD,0008]command not supported
2020-06-05T10:12:38:[TESTMD,0252]0051>
2020-06-05T10:12:48:[TESTMD,0050]"iridium"
2020-06-05T10:12:59:[SURF  ,0025]Iridium...
2020-06-05T10:14:13:<WARN>[SURF  ,0023]failed to connect #1, code -5, net 4, qual -1, dial -1
2020-06-05T10:15:34:<WARN>[SURF  ,0023]failed to connect #2, code -5, net 4, qual -1, dial -1
2020-06-05T10:16:53:<WARN>[SURF  ,0023]failed to connect #3, code -5, net 4, qual -1, dial -1
2020-06-05T10:18:34:[SURF  ,0009]connected in 335s, signal quality 2
2020-06-05T10:19:02:[SURF  ,0218]prompt received, remote cmd end
2020-06-05T10:19:02:[SURF  ,0012]0 cmd(s) received
2020-06-05T10:19:18:[UPLOAD,0248]Upload data files...
2020-06-05T10:19:38:[ZIO   ,0240]"NO CARRIER" received, aborting
2020-06-05T10:19:38:<ERR>[UPLOAD,0131]opening upload
2020-06-05T10:19:38:<ERR>[UPLOAD,0132]opening upload "0051"
2020-06-05T10:19:54:[SURF  ,0014]disconnected after 415s
2020-06-05T10:19:59:[TESTMD,0252]0051>
2020-06-05T10:20:35:[TESTMD,0050]"iridium"
2020-06-05T10:20:52:[SURF  ,0025]Iridium...
2020-06-05T10:22:04:<WARN>[SURF  ,0023]failed to connect #1, code -5, net 4, qual -1, dial -1
2020-06-05T10:23:25:<WARN>[SURF  ,0023]failed to connect #2, code -5, net 4, qual -1, dial -1
2020-06-05T10:24:45:<WARN>[SURF  ,0023]failed to connect #3, code -5, net 4, qual -1, dial -1
2020-06-05T10:26:05:<WARN>[SURF  ,0023]failed to connect #4, code -5, net 4, qual -1, dial -1
2020-06-05T10:27:10:[SURF  ,0009]connected in 378s, signal quality 5
2020-06-05T10:27:58:<WARN>[SURF  ,0071]timeout
2020-06-05T10:27:58:<WARN>[SURF  ,0056]peer mute
2020-06-05T10:28:08:[SURF  ,0014]disconnected after 436s
2020-06-05T10:28:13:[TESTMD,0252]0051>
2020-06-05T10:28:56:[TESTMD,0050]"iridium"
2020-06-05T10:29:10:[SURF  ,0025]Iridium...
