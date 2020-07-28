2020-02-12T10:21:43:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-02-12T10:21:43:[MAIN  ,0007]buoy 452.020-P-0051
2020-02-12T10:21:43:[MAIN  ,0055]soft pilotage 452.012.300_V2.12-20200211
2020-02-12T10:21:43:[MAIN  ,0011]date 2020-02-12T10:21:43
2020-02-12T10:21:49:[MAIN  ,0006]battery 15318mV,   14152uA
2020-02-12T10:21:52:[MAIN  ,0024]internal pressure 79156Pa
2020-02-12T10:21:53:[PRESS ,0038]P    -19mbar,T+17679mdegC
2020-02-12T10:21:54:[MRMAID,0182]thread started
2020-02-12T10:21:55:[MRMAID,0186]no wake-up
2020-02-12T10:21:56:[MRMAID,0188]acq already stopped
2020-02-12T10:21:56:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-02-12T10:21:57:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-02-12T10:21:57:[TESTMD,0053]Enter in test mode? yes/no
2020-02-12T10:21:57:[TESTMD,0252]0051>
2020-02-12T10:22:05:[TESTMD,0050]"yes"
2020-02-12T10:22:05:[TESTMD,0249]
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


2020-02-12T10:22:05:[TESTMD,0252]0051>
2020-02-12T10:22:41:[TESTMD,0050]"act"
2020-02-12T10:22:41:[SURFIN,0020]filling external bladder
2020-02-12T10:22:44:[SURFIN,0019]external bladder full
2020-02-12T10:22:49:[VALVE ,0034]valve opening 30000ms
2020-02-12T10:23:19:[VALVE ,0234]closed 14315mV/605364uA
2020-02-12T10:23:24:[SURFIN,0020]filling external bladder
2020-02-12T10:23:27:[SURFIN,0019]external bladder full
2020-02-12T10:23:27:<ERR>[TESTMD,0130]oil not transfered dt=-7s
2020-02-12T10:23:32:[BYPASS,0035]bypass opening 30000ms
2020-02-12T10:23:37:[BYPASS,0104]bypass opening: 14748mV/364536uA
2020-02-12T10:24:12:[BYPASS,0106]bypass closing: 14703mV/403942uA
2020-02-12T10:24:17:[SURFIN,0020]filling external bladder
2020-02-12T10:24:26:[PUMP  ,0207]pump warmup 15182mV/49166uA
2020-02-12T10:24:26:[PUMP  ,0016]pump during 300000ms
2020-02-12T10:25:28:[PUMP  ,0212]pump stopped, 14087mV/1467569uA
2020-02-12T10:25:28:[PUMP  ,0210]aborted, 24000ticks remain
2020-02-12T10:25:30:[SURFIN,0019]external bladder full
2020-02-12T10:25:31:[TESTMD,0045]pump run 64s
2020-02-12T10:25:36:[TESTMD,0066]test done
2020-02-12T10:25:36:[TESTMD,0252]0051>
2020-02-12T10:25:41:[TESTMD,0050]"act"
2020-02-12T10:25:41:[SURFIN,0020]filling external bladder
2020-02-12T10:25:49:[PUMP  ,0207]pump warmup 14851mV/49898uA
2020-02-12T10:25:49:[PUMP  ,0016]pump during 300000ms
2020-02-12T10:25:55:[PUMP  ,0212]pump stopped, 14043mV/1498843uA
2020-02-12T10:25:55:[PUMP  ,0210]aborted, 29400ticks remain
2020-02-12T10:25:57:[SURFIN,0019]external bladder full
2020-02-12T10:26:03:[VALVE ,0034]valve opening 30000ms
2020-02-12T10:26:32:[VALVE ,0234]closed 14452mV/603900uA
2020-02-12T10:26:38:[SURFIN,0020]filling external bladder
2020-02-12T10:26:46:[PUMP  ,0207]pump warmup 14835mV/49532uA
2020-02-12T10:26:46:[PUMP  ,0016]pump during 300000ms
2020-02-12T10:26:55:[PUMP  ,0212]pump stopped, 14060mV/1496269uA
2020-02-12T10:26:55:[PUMP  ,0210]aborted, 29100ticks remain
2020-02-12T10:26:57:[SURFIN,0019]external bladder full
2020-02-12T10:26:57:[TESTMD,0045]pump run 9s
2020-02-12T10:27:02:[BYPASS,0035]bypass opening 30000ms
2020-02-12T10:27:07:[BYPASS,0104]bypass opening: 14560mV/362584uA
2020-02-12T10:27:42:[BYPASS,0106]bypass closing: 14475mV/397842uA
2020-02-12T10:27:47:[SURFIN,0020]filling external bladder
2020-02-12T10:27:56:[PUMP  ,0207]pump warmup 14847mV/49898uA
2020-02-12T10:27:56:[PUMP  ,0016]pump during 300000ms
2020-02-12T10:29:11:[PUMP  ,0212]pump stopped, 14001mV/1479386uA
2020-02-12T10:29:11:[PUMP  ,0210]aborted, 22800ticks remain
2020-02-12T10:29:13:[SURFIN,0019]external bladder full
2020-02-12T10:29:13:[TESTMD,0045]pump run 76s
2020-02-12T10:29:18:[TESTMD,0066]test done
2020-02-12T10:29:18:[TESTMD,0252]0051>
2020-02-12T10:29:37:[TESTMD,0050]"gps"
2020-02-12T10:29:45:[SURF  ,0022]GPS fix...
2020-02-12T10:29:46:<WARN>[GPSFIX,0123]GPRMC ms=690 #1
2020-02-12T10:29:46:<WARN>[GPSFIX,0122]GPRMC no fix #0
2020-02-12T10:30:19:[SURF  ,0015]10 PPS detected...
2020-02-12T10:30:21:[MRMAID,0052]Mermaid $GPSACK:+50,+1,+11,+10,+20,-13,-388793;
2020-02-12T10:30:31:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-12T10:30:33:[GPSFIX,0179]-1s diff
2020-02-12T10:30:34:[SURF  ,0222]2020-02-12T10:30:34
2020-02-12T10:30:34:[SURF  ,0082]Latitude : N43deg41.977mn, Longitude :E007deg18.515mn
2020-02-12T10:30:34:[SURF  ,0223]fix3D,5satellites
2020-02-12T10:30:34:[SURF  ,0084]GPS fix GPGSA : hdop1.990,vdop2.100
2020-02-12T10:30:49:[TESTMD,0252]0051>
2020-02-12T10:30:51:[TESTMD,0050]"gps"
2020-02-12T10:31:01:[SURF  ,0022]GPS fix...
2020-02-12T10:31:21:[SURF  ,0015]10 PPS detected...
2020-02-12T10:31:22:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,-30;
2020-02-12T10:31:32:[MRMAID,0052]Mermaid $GPSOFF:3686320;
2020-02-12T10:31:34:[GPSFIX,0179]+0s diff
2020-02-12T10:31:34:[SURF  ,0222]2020-02-12T10:31:34
2020-02-12T10:31:34:[SURF  ,0082]Latitude : N43deg41.975mn, Longitude :E007deg18.515mn
2020-02-12T10:31:34:[SURF  ,0223]fix3D,5satellites
2020-02-12T10:31:34:[SURF  ,0084]GPS fix GPGSA : hdop1.590,vdop1.280
2020-02-12T10:31:49:[TESTMD,0252]0051>
2020-02-12T10:31:50:[TESTMD,0050]"iridium"
2020-02-12T10:32:02:[SURF  ,0025]Iridium...
2020-02-12T10:32:55:[SURF  ,0009]connected in 53s, signal quality 5
2020-02-12T10:33:24:[BUOY  ,0083]Default parameters restored
2020-02-12T10:33:24:[BYCMD ,0136]    default: 0
2020-02-12T10:33:29:[BYCMD ,0135]    store: 102
2020-02-12T10:33:38:[BYCMD ,0120]    bypass 10000ms 100000ms (20000ms 60000ms stored)
2020-02-12T10:33:40:[BYCMD ,0125]    near 1500mbar 3mbar/s (15000mbar 3mbar/s stored)
2020-02-12T10:33:43:[BYCMD ,0126]    far 2500mbar 4mbar/s (25000mbar 4mbar/s stored)
2020-02-12T10:33:45:[BYCMD ,0128]    dead 60s (300s stored)
2020-02-12T10:33:49:[P2TCMD,0155]p2t log dp > 50mbar
2020-02-12T10:33:51:[STACMD,0168]stage del 0
2020-02-12T10:33:53:[STAGE ,0080]Stage [0] 2500mbar (+/-500mbar) 900s (<900s) 
2020-02-12T10:33:56:[STAGE ,0080]Stage [1] 2500mbar (+/-500mbar) 900s (<1800s) MERMAID
2020-02-12T10:33:58:[STAGE ,0080]Stage [2] 5000mbar (+/-500mbar) 900s (<2700s) 
2020-02-12T10:34:00:[STAGE ,0091]Stage [3] surfacing 3600s (<6300s) SBE41
2020-02-12T10:34:00:[STAGE ,0340]Stage with SBE41: all parameters saved
2020-02-12T10:34:17:[STACMD,0170]stage store 104
2020-02-12T10:34:29:[SURF  ,0218]prompt received, remote cmd end
2020-02-12T10:34:29:[SURF  ,0012]21 cmd(s) received
2020-02-12T10:34:55:[UPLOAD,0248]Upload data files...
2020-02-12T10:35:21:[UPLOAD,0231]"0051/5E42E754.BIN" uploaded at 121bytes/s
2020-02-12T10:35:38:[MAIN  ,0013]1 file(s) uploaded
2020-02-12T10:36:11:[SURF  ,0014]disconnected after 249s
2020-02-12T10:36:16:[TESTMD,0252]0051>
