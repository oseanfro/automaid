import os
import shutil
import glob
import dives
import events
import re
import utils
from obspy import UTCDateTime
import datetime

mfloat = "452.020-P-0050"

dataPath = "../server"
# "server"

# Set a time range of analysis for a specific float
filterDate = [
    ("452.112-N-01",datetime.datetime(2018, 12, 27), datetime.datetime(2100, 1, 1)),
    ("452.112-N-02",datetime.datetime(2018, 12, 28), datetime.datetime(2100, 1, 1)),
    ("452.112-N-03",datetime.datetime(2018, 1, 1), datetime.datetime(2100, 1, 1)),
    ("452.112-N-04",datetime.datetime(2019, 1, 3), datetime.datetime(2100, 1, 1)),
    ("452.112-N-05",datetime.datetime(2019, 1, 3), datetime.datetime(2100, 1, 1)),
    ("452.020-P-06",datetime.datetime(2018, 5, 7), datetime.datetime(2018, 5, 7)),
    ("452.020-P-07",datetime.datetime(2018, 4, 26), datetime.datetime(2100, 1, 1)),
    ("452.020-P-08",datetime.datetime(2018, 8, 5), datetime.datetime(2100, 1, 1)),
    ("452.020-P-09",datetime.datetime(2018, 8, 6), datetime.datetime(2100, 1, 1)),
    ("452.020-P-10",datetime.datetime(2018, 8, 7), datetime.datetime(2100, 1, 1)),
    ("452.020-P-11",datetime.datetime(2018, 8, 9), datetime.datetime(2100, 1, 1)),
    ("452.020-P-12",datetime.datetime(2018, 8, 10), datetime.datetime(2100, 1, 1)),
    ("452.020-P-13",datetime.datetime(2018, 8, 31), datetime.datetime(2100, 1, 1)),
    ("452.020-P-16",datetime.datetime(2018, 9, 3), datetime.datetime(2100, 1, 1)),
    ("452.020-P-17",datetime.datetime(2018, 9, 4), datetime.datetime(2100, 1, 1)),
    ("452.020-P-18",datetime.datetime(2018, 9, 5), datetime.datetime(2100, 1, 1)),
    ("452.020-P-19",datetime.datetime(2018, 9, 6), datetime.datetime(2100, 1, 1)),
    ("452.020-P-20",datetime.datetime(2018, 9, 8), datetime.datetime(2100, 1, 1)),
    ("452.020-P-21",datetime.datetime(2018, 9, 9), datetime.datetime(2100, 1, 1)),
    ("452.020-P-22",datetime.datetime(2018, 9, 10), datetime.datetime(2100, 1, 1)),
    ("452.020-P-23",datetime.datetime(2018, 9, 12), datetime.datetime(2100, 1, 1)),
    ("452.020-P-24",datetime.datetime(2018, 9, 13), datetime.datetime(2100, 1, 1)),
    ("452.020-P-25",datetime.datetime(2018, 6, 12), datetime.datetime(2100, 1, 1)),
    ("452.020-P-0050",datetime.datetime(2019, 5, 6), datetime.datetime(2100, 1, 1)),
    ("452.020-P-0051",datetime.datetime(2019, 5, 9), datetime.datetime(2100, 1, 1)),
    ("452.020-P-0052",datetime.datetime(2019, 5, 8), datetime.datetime(2100, 1, 1)),
    ("452.020-P-0053",datetime.datetime(2019, 5, 10), datetime.datetime(2100, 1, 1))
]


def main():
    # Set the path for the float
    mfloat_path = "../processed/" + mfloat + "/"

    # Get float number
    mfloat_nb = re.findall("(\d+)$", mfloat)[0]

    # Copy appropriate files in the directory
    for f in glob.glob("../processed/"+mfloat+"/*/*.LOG.h"):
        shutil.copy(f, mfloat_path)

    for f in glob.glob("../processed/"+mfloat+"/*/*.MER.env"):
        shutil.copy(f, mfloat_path)

    for f in glob.glob("../processed/"+mfloat+"/*.LOG.h"):
        shutil.move(f, f[0:len(f)-2])

    for f in glob.glob("../processed/"+mfloat+"/*.MER.env"):
        shutil.move(f, "../processed/"+mfloat+"/"+f[len(f)-21:len(f)-4])

    # Build list of all mermaid events recorded by the float
    mevents = events.Events(mfloat_path)

    # Process data for each dive
    mdives = dives.get_dives(mfloat_path, mevents)

    # Filter dives between begin and end date
    for fd in filterDate:
        fname = fd[0]
        begin = fd[1]
        end = fd[2]
        if fname == mfloat:
            mdives = [dive for dive in mdives if begin <= dive.date <= end]

    # Software version
    print ""
    print "Software version"
    for dive in mdives:
        if dive.is_init:
            formatted_log = dive.log_content #utils.format_log(dive.log_content)
            print re.findall(".+soft.+", formatted_log)[0]

    # Find errors and warnings
    print ""
    print "List of errors"
    for dive in mdives:
        if dive.is_complete_dive:
            formatted_log = dive.log_content #utils.format_log(dive.log_content)
            for err in re.findall(".+<ERR>.+", formatted_log):
                print err

    print ""
    print "List of warnings"
    for dive in mdives:
        if dive.is_complete_dive:
            formatted_log = dive.log_content #utils.format_log(dive.log_content)
            for wrn in re.findall(".+<WRN>.+", formatted_log):
                print wrn

    # Synchronisations GPS
    print ""
    print "Synchronisations GPS"
    pps_detect_list = list()
    gpsack_list = list()
    gpsoff_list = list()
    position_list = list()
    for dive in mdives:
        if dive.is_complete_dive:
            formatted_log = dive.log_content #utils.format_log(dive.log_content)
            pps_detect_list += re.findall(".+PPS.+", formatted_log)
            gpsack_list += re.findall(".+GPSACK.+", formatted_log)
            gpsoff_list += re.findall(".+GPSOFF.+", formatted_log)
            position_list += re.findall(".+N\d+deg\d+\.\d+mn, E\d+deg\d+\.\d+mn.+", formatted_log)

    if len(pps_detect_list) != len(gpsack_list) and len(gpsack_list) != len(gpsoff_list) \
            and len(gpsoff_list) != len(position_list):
        print "LENGTH ERROR !!!!"
    else:
        for pps_detect in pps_detect_list:
            print pps_detect
        for gpsack in gpsack_list:
            print gpsack
        for gpsoff in gpsoff_list:
            print gpsoff
        for position in position_list:
            print position

    # Get dive number
    dive_nb = 0
    for dive in mdives:
        if dive.is_complete_dive:
            dive_nb += 1

    # Temps de pompe pour le bladder full
    print ""
    print "Temps de pompe pour le bladder full (s):"
    temps_bladder_full = list()
    for dive in mdives:
        if dive.is_complete_dive:
            start_filling_date = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)[0][1]
            bladder_full_date = utils.find_timestampedUTC_values("external bladder full", dive.log_content)[0][1]
            bdf_time = int(UTCDateTime(bladder_full_date) - UTCDateTime(start_filling_date))
            temps_bladder_full.append(bdf_time)
    for bdft in temps_bladder_full:
        print bdft
    temps_bladder_full_moyen = int(float(sum(temps_bladder_full)) / dive_nb)
    print "Temps moyen (s): " + str(temps_bladder_full_moyen)
    print "Temps moyen (h:min:s): 00:" + str(temps_bladder_full_moyen/60) + ":" + str(temps_bladder_full_moyen % 60)

    # Consommation de la pompe pendant le bladder full
    print ""
    print "Consommation de la pompe pendant le bladder full (amperes):"
    amp_val_list = list()
    for dive in mdives:
        if dive.is_complete_dive:
            start_filling_date = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)[0][1]
            bladder_full_date = utils.find_timestampedUTC_values("external bladder full", dive.log_content)[0][1]
            bladder_full_power = utils.find_timestampedUTC_values("battery.+", dive.log_content)
            max_pwr = "Aucune mesure dans " + dive.log_name
            max_amp = 0
            for bfp in bladder_full_power:
                bfp_date = bfp[1]
                if bladder_full_date > bfp_date > start_filling_date:
                    amp_val = int(re.findall("(\d+)uA", bfp[0])[0])
                    if amp_val > max_amp:
                        # On cherche la valeur la plus elevee de la plongee
                        max_amp = amp_val
                        max_pwr = str(bfp_date) + ": " + str(round(float(amp_val) / 1000000., 2)) + "A"
            # Pour chaque plongee on affiche la valeur de courant max et on enrigstre sa valeur dans une liste
            print max_pwr
            amp_val_list += [max_amp]
    print "Consommation moyenne: " + str(round(float(sum(amp_val_list)) / len(amp_val_list) / 1000000., 2)) + "A"

    # Temps de bypass
    print ""
    print "Temps de bypass (s):"
    temps_bypass = []
    nb_ouverture_secondaire_bypass = []
    for dive in mdives:
        if dive.is_complete_dive:
            bypass_all_str = re.findall("BYPASS,\d+\]opening (\d+)", dive.log_content)
            if len(bypass_all_str) == 0:
                break
            bypass_first = int(bypass_all_str[0])
            bypass_second = [int(x) for x in bypass_all_str[1:]]
            temps_bypass += [bypass_first + sum(bypass_second)]
            nb_ouverture_secondaire_bypass += [len(bypass_second)]
    for tb in temps_bypass:
        print tb / 1000
    print "Nombre d'ouvreture secondaires: " + str(nb_ouverture_secondaire_bypass)
    # print "Temps total (s): " + str(sum(temps_bypass)/1000)
    temps_bypass_moyen = int(float(sum(temps_bypass)) / dive_nb)/1000
    print "Temps moyen (s): " + str(temps_bypass_moyen)

    # Rapport (temps pour le bladder full) / (temps de bypass)
    print ""
    print "Rapport (temps pour le bladder full) / (temps de bypass):"
    print str(round(float(temps_bladder_full_moyen) / float(temps_bypass_moyen), 1))

    # Temps de pompe en plongee
    print ""
    print "Temps de pompe en plongee (s):"
    temps_pompe = []
    for dive in mdives:
        if dive.is_complete_dive:
            start_filling_date = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)[0][1]
            temps_pompe_timestamp_str = utils.find_timestampedUTC_values("PUMP  ,\d+\]during (\d+)", dive.log_content)
            liste_activation_pompe = [int(tp[0]) for tp in temps_pompe_timestamp_str if tp[1] < start_filling_date]
            temps_total_pompe_par_plongee = sum(liste_activation_pompe)
            temps_pompe += [temps_total_pompe_par_plongee]
    # print "Temps total (s): " + str(sum(temps_pompe)/1000)
    for tp in temps_pompe:
        print round(float(tp) / 1000, 3)
    temps_pompe_moyen = int(float(sum(temps_pompe)) / dive_nb)/1000
    print "Temps moyen (s): " + str(temps_pompe_moyen)

    # Temps de valve
    print ""
    print "Temps de valve (s):"
    temps_valve = []
    for dive in mdives:
        if dive.is_complete_dive:
            temps_valve_str = re.findall("VALVE ,\d+\]opening for (\d+)", dive.log_content)
            liste_activation_valve = [int(tv) for tv in temps_valve_str]
            temps_total_valve_par_plongee = sum(liste_activation_valve)
            temps_valve += [temps_total_valve_par_plongee]
    # print "Temps total (ms): " + str(sum(temps_valve))
    for tv in temps_valve:
        print round(float(tv) / 1000, 3)
    temps_valve_moyen = float(sum(temps_valve)) / dive_nb / 1000
    print "Temps moyen (s): " + str(round(temps_valve_moyen, 3))

    # Rapport (temps pour le bladder full) / (temps de bypass)
    print ""
    print "Rapport (temps de pompe en plongee) / (temps de valve):"
    print str(round(float(temps_pompe_moyen) / float(temps_valve_moyen), 1))

    # Clean directories
    for f in glob.glob(mfloat_path + "/" + mfloat + "*"):
        os.remove(f)
    for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.LOG"):
        os.remove(f)
    for f in glob.glob(mfloat_path + "/" + mfloat_nb + "_*.MER"):
        os.remove(f)


if __name__ == "__main__":
    main()
