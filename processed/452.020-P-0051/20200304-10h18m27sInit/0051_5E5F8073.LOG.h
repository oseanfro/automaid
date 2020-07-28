2020-03-04T10:18:27:[MONITR,0197]reboot code 0x0000, src/monitor.c@520
2020-03-04T10:18:27:[MAIN  ,0007]buoy 452.020-P-0051
2020-03-04T10:18:27:[MAIN  ,0055]soft pilotage 452.012.300_V2.14-20200303
2020-03-04T10:18:27:[MAIN  ,0011]date 2020-03-04T10:18:27
2020-03-04T10:18:33:[MAIN  ,0006]battery 15300mV,   14274uA
2020-03-04T10:18:36:[MAIN  ,0024]internal pressure 78224Pa
2020-03-04T10:18:37:[PRESS ,0038]P   -109mbar,T+14727mdegC
2020-03-04T10:18:38:[MRMAID,0182]thread started
2020-03-04T10:18:39:[MRMAID,0186]no wake-up
2020-03-04T10:18:40:[MRMAID,0188]acq already stopped
2020-03-04T10:18:40:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-03-04T10:18:41:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-03-04T10:18:41:[TESTMD,0053]Enter in test mode? yes/no
2020-03-04T10:18:41:[TESTMD,0252]0051>
2020-03-04T10:18:49:[TESTMD,0050]"yes"
2020-03-04T10:18:49:[TESTMD,0249]
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


2020-03-04T10:18:49:[TESTMD,0252]0051>
2020-03-04T10:19:15:[TESTMD,0050]"act"
2020-03-04T10:19:15:[SURFIN,0020]filling external bladder
2020-03-04T10:19:18:[SURFIN,0019]external bladder full
2020-03-04T10:19:23:[VALVE ,0034]valve opening 30000ms
2020-03-04T10:19:58:[SURFIN,0020]filling external bladder
2020-03-04T10:20:01:[SURFIN,0019]external bladder full
2020-03-04T10:20:01:<ERR>[TESTMD,0130]oil not transfered dt=-7s
2020-03-04T10:20:06:[BYPASS,0035]bypass opening 30000ms
2020-03-04T10:20:51:[SURFIN,0020]filling external bladder
2020-03-04T10:20:59:[PUMP  ,0016]pump during 300000ms
2020-03-04T10:22:01:[SURFIN,0019]external bladder full
2020-03-04T10:22:01:[TESTMD,0045]pump run 60s
2020-03-04T10:22:06:[TESTMD,0066]test done
2020-03-04T10:22:06:[TESTMD,0252]0051>
2020-03-04T10:22:16:[TESTMD,0050]"act"
2020-03-04T10:22:16:[SURFIN,0020]filling external bladder
2020-03-04T10:22:24:[PUMP  ,0016]pump during 300000ms
2020-03-04T10:22:34:[SURFIN,0019]external bladder full
2020-03-04T10:22:39:[VALVE ,0034]valve opening 30000ms
2020-03-04T10:23:14:[SURFIN,0020]filling external bladder
2020-03-04T10:23:22:[PUMP  ,0016]pump during 300000ms
2020-03-04T10:23:33:[SURFIN,0019]external bladder full
2020-03-04T10:23:34:[TESTMD,0045]pump run 10s
2020-03-04T10:23:39:[BYPASS,0035]bypass opening 30000ms
2020-03-04T10:24:24:[SURFIN,0020]filling external bladder
2020-03-04T10:24:32:[PUMP  ,0016]pump during 300000ms
2020-03-04T10:25:40:[SURFIN,0019]external bladder full
2020-03-04T10:25:40:[TESTMD,0045]pump run 66s
2020-03-04T10:25:45:[TESTMD,0066]test done
2020-03-04T10:25:45:[TESTMD,0252]0051>
2020-03-04T10:25:52:[TESTMD,0050]"gps"
2020-03-04T10:26:00:[SURF  ,0022]GPS fix...
2020-03-04T10:26:23:<WARN>[GPSFIX,0123]GPRMC ms=10 #1
2020-03-04T10:26:49:[SURF  ,0015]10 PPS detected...
2020-03-04T10:26:51:[MRMAID,0052]Mermaid $GPSACK:+50,+2,+3,+10,+17,+13,-76965;
2020-03-04T10:27:01:[MRMAID,0052]Mermaid $GPSOFF:3686321;
2020-03-04T10:27:03:[GPSFIX,0179]-1s diff
2020-03-04T10:27:04:[SURF  ,0222]2020-03-04T10:27:04
2020-03-04T10:27:04:[SURF  ,0082]Latitude : N43deg41.967mn, Longitude :E007deg18.509mn
2020-03-04T10:27:04:[SURF  ,0223]fix3D,5satellites
2020-03-04T10:27:04:[SURF  ,0084]GPS fix GPGSA : hdop1.360,vdop1.720
2020-03-04T10:27:19:[TESTMD,0252]0051>
2020-03-04T10:28:03:[TESTMD,0050]"gps"
2020-03-04T10:28:15:[SURF  ,0022]GPS fix...
2020-03-04T10:28:35:[SURF  ,0015]10 PPS detected...
2020-03-04T10:28:36:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,-30;
2020-03-04T10:28:46:[MRMAID,0052]Mermaid $GPSOFF:3686321;
2020-03-04T10:28:48:[GPSFIX,0179]+0s diff
2020-03-04T10:28:48:[SURF  ,0222]2020-03-04T10:28:48
2020-03-04T10:28:48:[SURF  ,0082]Latitude : N43deg41.966mn, Longitude :E007deg18.513mn
2020-03-04T10:28:48:[SURF  ,0223]fix3D,5satellites
2020-03-04T10:28:48:[SURF  ,0084]GPS fix GPGSA : hdop1.350,vdop1.710
2020-03-04T10:29:03:[TESTMD,0252]0051>
2020-03-04T10:29:17:[TESTMD,0050]"iridium"
2020-03-04T10:29:27:[SURF  ,0025]Iridium...
2020-03-04T10:30:24:[SURF  ,0009]connected in 57s, signal quality 2
2020-03-04T10:31:45:[SURF  ,0218]prompt received, remote cmd end
2020-03-04T10:31:45:[SURF  ,0012]18 cmd(s) received
2020-03-04T10:32:07:[UPLOAD,0248]Upload data files...
2020-03-04T10:32:30:[UPLOAD,0231]"0051/5E5E5DAC.BIN" uploaded at 114bytes/s
2020-03-04T10:32:41:[UPLOAD,0231]"0051/5E5E73C5.BIN" uploaded at 102bytes/s
2020-03-04T10:32:58:[MAIN  ,0013]2 file(s) uploaded
2020-03-04T10:33:29:[SURF  ,0014]disconnected after 242s
2020-03-04T10:33:34:[TESTMD,0252]0051>
