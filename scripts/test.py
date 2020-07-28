import os
import shutil
import sys
import glob
import dives
import events
import profile
import re
import utils
from obspy import UTCDateTime
import datetime


def dive(mfloat,date_begin,date_end):
        # Set the path for the float
        mfloat_path = "../processed/" + mfloat + "/"
        #set the filter Date
        filterDate = [(mfloat,date_begin,date_end)]
        # Get float number
        mfloat_nb = re.findall("(\d+)$", mfloat)[0]

        # Copy appropriate files in the directory
        for f in glob.glob("../processed/"+ mfloat +"/*/*.LOG.h"):
            shutil.copy(f, mfloat_path)

        for f in glob.glob("../processed/"+ mfloat +"/*/*.MER.env"):
            shutil.copy(f, mfloat_path)

        for f in glob.glob("../processed/"+ mfloat +"/*.LOG.h"):
            shutil.move(f, f[0:len(f)-2])

        for f in glob.glob("../processed/"+ mfloat +"/*.MER.env"):
            sp=f.split(".")
            shutil.move(f, "../processed/"+ mfloat +"/"+sp[5]+".MER")

        # Build list of all mermaid events recorded by the float
        mevents = events.Events(mfloat_path)

        # Build list of all profiles recorded
        ms41s = profile.Profiles(mfloat_path)

        # Process data for each dive
        mdives = dives.get_dives(mfloat_path, mevents, ms41s)

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
                soft_version = re.findall(".+soft.+", formatted_log)
                if len(soft_version) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : No software version available"
                    continue
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
                position_list += re.findall(".+N\d+deg\d+\.\d+mn,.*E\d+deg\d+\.\d+mn.+", formatted_log)

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

        # Temps de pompe pour le bladder full en fin de plongee
        print ""
        print "Temps de pompe pour le bladder full en fin de plongee (s):"
        temps_bladder_full = list()
        for dive in mdives:
            if dive.is_complete_dive:
                start_filling_date = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)[-1][1]
                bdf_time = 300*5
                try :
                    bladder_full_date = utils.find_timestampedUTC_values("external bladder full", dive.log_content)[-1][1]
                except :
                    print "No external bladder full : " + dive.log_name
                else :
                    bdf_time = int(UTCDateTime(bladder_full_date) - UTCDateTime(start_filling_date))
                temps_bladder_full.append(bdf_time)
                print str(UTCDateTime(dive.date).isoformat()) + " : " + str(bdf_time)
        temps_bladder_full_moyen = int(float(sum(temps_bladder_full)) / dive_nb)
        print "Temps moyen (s): " + str(temps_bladder_full_moyen)
        print "Temps moyen (h:min:s): 00:" + str(temps_bladder_full_moyen/60) + ":" + str(temps_bladder_full_moyen % 60)

        # Consommation de la pompe pendant le bladder full
        print ""
        print "Consommation de la pompe pendant le bladder full (amperes):"
        amp_val_list = list()
        for dive in mdives:
            if dive.is_complete_dive:
                all_filling_str = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)
                if len(all_filling_str) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : Pas de debut de remplissage de vessie" 
                    continue
                start_filling_date = all_filling_str[-1][1]
                all_bladder_full_str = utils.find_timestampedUTC_values("external bladder full", dive.log_content)
                if len(all_bladder_full_str) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : Pas de fin de remplissage de vessie" 
                    continue
                bladder_full_date =  all_bladder_full_str[-1][1]
                bladder_full_power = utils.find_timestampedUTC_values("battery.+", dive.log_content)
                max_pwr = str(UTCDateTime(dive.date).isoformat()) + ": " + "Aucune mesure (" + dive.log_name + ")"
                max_amp = 0
                for bfp in bladder_full_power:
                    bfp_date = bfp[1]
                    if bladder_full_date > bfp_date > start_filling_date:
                        amp_val = int(re.findall("(\d+)uA", bfp[0])[0])
                        if amp_val > max_amp:
                            # On cherche la valeur la plus elevee de la plongee
                            max_amp = amp_val
                            max_pwr = str(UTCDateTime(bfp_date).isoformat()) + ": " + str(round(float(amp_val) / 1000000., 2)) + "A"
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
                bypass_all_str = re.findall(":\[BYPASS.+\].*opening (\d+)ms", dive.log_content)
                if len(bypass_all_str) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : Pas de coups de bypass " 
                    continue
                bypass_first = int(bypass_all_str[0])
                bypass_second = [int(x) for x in bypass_all_str[1:]]
                temps_bypass += [bypass_first + sum(bypass_second)]
                print str(UTCDateTime(dive.date).isoformat()) + " : " + str((bypass_first + sum(bypass_second))/1000)
                nb_ouverture_secondaire_bypass += [len(bypass_second)]
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
        temps_pompe_min = 600000
        for dive in mdives:
            if dive.is_complete_dive:
                all_filling_str = utils.find_timestampedUTC_values("filling external bladder", dive.log_content)
                if len(all_filling_str) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : Pas de remplissage de vessie, ne peut pas estimer une fin de plongee" 
                    continue
                start_filling_date = all_filling_str[-1][1]
                all_bypass_str = utils.find_timestampedUTC_values(":\[BYPASS.+\].*opening (\d+)ms", dive.log_content)
                if len(all_bypass_str) == 0:
                    print str(UTCDateTime(dive.date).isoformat()) + " : Pas de coup de bypass, ne peut pas estimer un debut de plongee" 
                    continue
                first_bypass_date = all_bypass_str[0][1]
                temps_pompe_timestamp_str = utils.find_timestampedUTC_values(":\[PUMP.+\].*during (\d+)ms", dive.log_content)
                liste_activation_pompe = [int(tp[0]) for tp in temps_pompe_timestamp_str if tp[1] < start_filling_date and tp[1] > first_bypass_date]
                for time in liste_activation_pompe :
                    if time < temps_pompe_min :
                        temps_pompe_min = time
                temps_total_pompe_par_plongee = sum(liste_activation_pompe)
                temps_pompe += [temps_total_pompe_par_plongee]
                print str(UTCDateTime(dive.date).isoformat()) + " : " + str(round(float(temps_total_pompe_par_plongee) / 1000, 3))
        # print "Temps total (s): " + str(sum(temps_pompe)/1000)
        temps_pompe_moyen = int(float(sum(temps_pompe)) / dive_nb)/1000
        print "Temps moyen (s): " + str(temps_pompe_moyen)
        print "Temp min (ms): " + str(temps_pompe_min)

        # Temps de valve
        print ""
        print "Temps de valve (s):"
        temps_valve = []
        temps_valve_min = 60000
        for dive in mdives:
            if dive.is_complete_dive:
                temps_valve_str = re.findall(":\[VALVE.+\].*opening f?o?r? ?(\d+)ms", dive.log_content)
                liste_activation_valve = [int(tv) for tv in temps_valve_str]
                for time in liste_activation_valve :
                    if time < temps_valve_min:
                        temps_valve_min = time
                temps_total_valve_par_plongee = sum(liste_activation_valve)
                temps_valve += [temps_total_valve_par_plongee]
                print str(UTCDateTime(dive.date).isoformat()) + " : " + str(round(float(tv) / 1000, 3))
        # print "Temps total (ms): " + str(sum(temps_valve))
        temps_valve_moyen = float(sum(temps_valve)) / dive_nb / 1000
        print "Temps moyen (s): " + str(round(temps_valve_moyen, 3))
        print "Temps min (ms): " + str(temps_valve_min)

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
