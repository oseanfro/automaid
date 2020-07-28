2020-01-13T14:29:11:[MONITR,0197]reboot code 0x0000, src/monitor.c@516
2020-01-13T14:29:11:[MAIN  ,0007]buoy 452.020-P-0051
2020-01-13T14:29:11:[MAIN  ,0055]soft pilotage 452.012.300_V2.9-20200113
2020-01-13T14:29:12:[MAIN  ,0011]date 2020-01-13T14:29:12
2020-01-13T14:29:18:[MAIN  ,0006]battery 15366mV,   11468uA
2020-01-13T14:29:20:[MAIN  ,0024]internal pressure 102006Pa
2020-01-13T14:29:22:[PRESS ,0038]P-65535965mbar,T+20167mdegC
2020-01-13T14:29:22:[MRMAID,0182]thread started
2020-01-13T14:29:23:[MRMAID,0186]no wake-up
2020-01-13T14:29:24:[MRMAID,0188]acq already stopped
2020-01-13T14:29:24:[MRMAID,0052]Mermaid $BOARD:452116600-51;
2020-01-13T14:29:25:[MRMAID,0052]Mermaid $SOFT:2.1344;
2020-01-13T14:29:25:[TESTMD,0053]Enter in test mode? yes/no
2020-01-13T14:29:25:[TESTMD,0252]0051>
2020-01-13T14:29:28:[TESTMD,0050]"yes"
2020-01-13T14:29:28:[TESTMD,0249]
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


2020-01-13T14:29:29:[TESTMD,0252]0051>
2020-01-13T14:30:06:[TESTMD,0050]"fiilb"
2020-01-13T14:30:06:[TESTMD,0008]command not supported
2020-01-13T14:30:06:[TESTMD,0252]0051>
2020-01-13T14:30:16:[TESTMD,0050]"fillb"
2020-01-13T14:30:16:[SURFIN,0020]filling external bladder
2020-01-13T14:30:25:[PUMP  ,0016]pump during 300000ms
2020-01-13T14:30:34:[PUMP  ,0210]aborted, 29100ticks remain
2020-01-13T14:30:36:[SURFIN,0019]external bladder full
2020-01-13T14:30:36:[TESTMD,0252]0051>
