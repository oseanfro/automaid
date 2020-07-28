2020-06-25T08:37:59:[MONITR,0197]reboot code 0x0000, src/monitor.c@520
2020-06-25T08:37:59:[MAIN  ,0007]buoy 452.020-P-0051
2020-06-25T08:37:59:[MAIN  ,0055]soft pilotage 452.012.300_V2.20-20200612
2020-06-25T08:37:59:[MAIN  ,0011]date 2020-06-25T08:37:59
2020-06-25T08:38:05:[MAIN  ,0006]battery 15357mV,   14030uA
2020-06-25T08:38:08:[MAIN  ,0024]internal pressure 82841Pa
2020-06-25T08:38:09:[PRESS ,0038]P    -89mbar,T+24958mdegC
2020-06-25T08:38:09:[MRMAID,0182]thread started
2020-06-25T08:38:10:[MRMAID,0186]no wake-up
2020-06-25T08:38:11:[MRMAID,0188]acq already stopped
2020-06-25T08:38:12:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-06-25T08:38:13:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-06-25T08:38:13:[TESTMD,0053]Enter in test mode? yes/no
2020-06-25T08:38:13:[TESTMD,0252]0051>
2020-06-25T08:38:23:[TESTMD,0050]"yes"
2020-06-25T08:38:23:[TESTMD,0249]
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


2020-06-25T08:38:23:[TESTMD,0252]0051>
2020-06-25T08:38:35:[TESTMD,0050]"pint"
2020-06-25T08:38:38:[TESTMD,0029]82871Pa
2020-06-25T08:38:38:[TESTMD,0252]0051>
2020-06-25T08:38:45:[TESTMD,0050]"pext"
2020-06-25T08:38:49:[PRESS ,0038]P    -79mbar,T+24971mdegC
2020-06-25T08:38:49:[TESTMD,0252]0051>
2020-06-25T08:38:58:[TESTMD,0050]"ui"
2020-06-25T08:39:00:[MAIN  ,0006]battery 15356mV,   14762uA
2020-06-25T08:39:00:[TESTMD,0252]0051>
2020-06-25T08:39:10:[TESTMD,0050]"act"
2020-06-25T08:39:10:[SURFIN,0020]filling external bladder
2020-06-25T08:39:18:[PUMP  ,0016]pump during 300000ms
2020-06-25T08:39:28:[SURFIN,0019]external bladder full
2020-06-25T08:39:33:[VALVE ,0034]valve opening 30000ms
2020-06-25T08:40:08:[SURFIN,0020]filling external bladder
2020-06-25T08:40:11:[SURFIN,0019]external bladder full
2020-06-25T08:40:11:<ERR>[TESTMD,0130]oil not transfered dt=-7s
2020-06-25T08:40:16:[BYPASS,0035]bypass opening 30000ms
2020-06-25T08:41:01:[SURFIN,0020]filling external bladder
2020-06-25T08:41:09:[PUMP  ,0016]pump during 300000ms
2020-06-25T08:41:27:[SURFIN,0019]external bladder full
2020-06-25T08:41:27:[TESTMD,0045]pump run 16s
2020-06-25T08:41:32:[TESTMD,0066]test done
2020-06-25T08:41:32:[TESTMD,0252]0051>
2020-06-25T08:42:22:[TESTMD,0050]"gps"
2020-06-25T08:42:29:[SURF  ,0022]GPS fix...
2020-06-25T08:43:15:[SURF  ,0015]10 PPS detected...
2020-06-25T08:43:17:[MRMAID,0052]Mermaid $GPSACK:+50,+5,+24,+8,+35,-21,-89385;
2020-06-25T08:43:27:[MRMAID,0052]Mermaid $GPSOFF:3686315;
2020-06-25T08:43:28:[GPSFIX,0179]-1s diff
2020-06-25T08:43:29:[SURF  ,0222]2020-06-25T08:43:29
2020-06-25T08:43:29:[SURF  ,0082]Latitude : N43deg25.448mn, Longitude :E007deg48.375mn
2020-06-25T08:43:29:[SURF  ,0223]fix3D,9satellites
2020-06-25T08:43:29:[SURF  ,0084]GPS fix GPGSA : hdop0.890,vdop0.980
2020-06-25T08:43:44:[TESTMD,0252]0051>
2020-06-25T08:44:02:[TESTMD,0050]"GPS"
2020-06-25T08:44:02:[TESTMD,0008]command not supported
2020-06-25T08:44:02:[TESTMD,0252]0051>
2020-06-25T08:44:10:[TESTMD,0050]"gps"
2020-06-25T08:44:21:[SURF  ,0022]GPS fix...
2020-06-25T08:44:41:[SURF  ,0015]10 PPS detected...
2020-06-25T08:44:42:[MRMAID,0052]Mermaid $GPSACK:+0,+0,+0,+0,+0,+0,+0;
2020-06-25T08:44:52:[MRMAID,0052]Mermaid $GPSOFF:3686315;
2020-06-25T08:44:53:[GPSFIX,0179]-1s diff
2020-06-25T08:44:54:[SURF  ,0222]2020-06-25T08:44:54
2020-06-25T08:44:54:[SURF  ,0082]Latitude : N43deg25.316mn, Longitude :E007deg48.668mn
2020-06-25T08:44:54:[SURF  ,0223]fix3D,9satellites
2020-06-25T08:44:54:[SURF  ,0084]GPS fix GPGSA : hdop0.890,vdop0.980
2020-06-25T08:45:09:[TESTMD,0252]0051>
