2020-03-03T15:12:05:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-03-03T15:12:05:[MAIN  ,0007]buoy 452.020-P-0051
2020-03-03T15:12:05:[MAIN  ,0055]soft pilotage 452.012.300_V2.14-20200303
2020-03-03T15:12:05:[MAIN  ,0011]date 2020-03-03T15:12:05
2020-03-03T15:12:11:[MAIN  ,0006]battery 15323mV,   14274uA
2020-03-03T15:12:14:[MAIN  ,0024]internal pressure 78728Pa
2020-03-03T15:12:15:[PRESS ,0038]P   -129mbar,T+16288mdegC
2020-03-03T15:12:16:[MRMAID,0182]thread started
2020-03-03T15:12:17:[MRMAID,0186]no wake-up
2020-03-03T15:12:18:[MRMAID,0188]acq already stopped
2020-03-03T15:12:18:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-03-03T15:12:19:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-03-03T15:12:19:[TESTMD,0053]Enter in test mode? yes/no
2020-03-03T15:12:19:[TESTMD,0252]0051>
2020-03-03T15:12:20:[TESTMD,0050]"yes"
2020-03-03T15:12:20:[TESTMD,0249]
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


2020-03-03T15:12:20:[TESTMD,0252]0051>
2020-03-03T15:12:23:[TESTMD,0050]"pext"
2020-03-03T15:12:27:[PRESS ,0038]P   -119mbar,T+16289mdegC
2020-03-03T15:12:27:[TESTMD,0252]0051>
2020-03-03T15:12:28:[TESTMD,0050]"pint"
2020-03-03T15:12:31:[TESTMD,0029]78768Pa
2020-03-03T15:12:31:[TESTMD,0252]0051>
2020-03-03T15:12:36:[TESTMD,0050]"q"
2020-03-03T15:12:36:[MAIN  ,0018]end of test mode
2020-03-03T15:12:36:[MAIN  ,0048]reboot MERMAID board
2020-03-03T15:12:38:[MAIN  ,0047]reboot float
2020-03-03T15:12:39:[MONITR,0198]rebooting with code 0x0000, data "src/monitor.c@520002"
