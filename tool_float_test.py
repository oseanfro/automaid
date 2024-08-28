import os
import shutil
import glob
import re
from math import sqrt
import math
from obspy import UTCDateTime
import datetime
import sys
import openpyxl

try:
    import dives
    import events
    import utils
    import sbe41
    import sbe61
    import decrypt
except:
    import automaid.dives as dives
    import automaid.utils as utils
    import automaid.events as events
    import automaid.decrypt as decrypt
    import automaid.sbe41 as sbe41
    import automaid.sbe61 as sbe61

# Set a time range of analysis for a specific float
#infos = ("467.174-T-0100",datetime.datetime(2023, 6, 20), datetime.datetime(2100, 1, 1))
#infos = ("467.174-T-0101",datetime.datetime(2023, 4, 14), datetime.datetime(2100, 1, 1))
infos = ("467.120-T-0055",datetime.datetime(2023, 2, 5), datetime.datetime(2100, 1, 1))
#infos = ("467.164-T-0102",datetime.datetime(2023, 6, 20), datetime.datetime(2100, 1, 1))

bladder_max_ml = 3000
bypass_flow_ml_per_s = 5.0
pump_deep_flow_ml_per_s = 0.416
pump_surface_flow_ml_per_s = 20.000


def print_emergency(dive):
    formatted_log = dive.log_content
    emergency_list = re.findall(".+TRIGGERED BY.+", formatted_log)
    if len(emergency_list) > 0 :
        print("!!!!!! EMERGENCY !!!!!!!!")
        return True
    return False


def print_software_version(dive):
    # Software version
    formatted_log = dive.log_content
    for soft in re.findall(".+soft.+", formatted_log):
        print(soft)

def print_cycle_nb(dive):
    # Software version
    formatted_log = dive.log_content
    for cycle in re.findall(".+cycle \d+", formatted_log):
        print(cycle)

def print_errors(dive):
    # Find errors
    formatted_log = dive.log_content
    for err in re.findall(".+<ERR>.+", formatted_log):
        print(err)

def print_warning(dive):
    # Find warnings
    formatted_log = dive.log_content
    for err in re.findall(".+<WARN>.+", formatted_log):
        print(err)

def print_bladder_full_time(dive):
    list_pump = list()
    log_lines = utils.split_log_lines(dive.log_content)
    timestamp_last = UTCDateTime()
    comp_duration = False
    end_file = False
    filling = False

    for line in log_lines:
        timestamp_catch = re.findall("(\S+):\\[", line)
        pump_catch = re.findall("PUMP.+\]pump during (\d+)ms", line)
        full_catch = re.findall("external bladder full", line)
        if not end_file:
            end_catch = re.findall("\]surfacing", line)
            if len(end_catch) > 0 :
                end_file = True
        else :
            filling_catch = re.findall("filling external bladder", line)
            if len(filling_catch) > 0 :
                filling = True;

        if filling :
            if len(pump_catch) > 0:
                list_pump.append(int(pump_catch[0]) / 1000)
                timestamp_last = UTCDateTime(str(timestamp_catch[0]), iso8601=True)
            elif len(full_catch) > 0:
                timestamp = UTCDateTime(str(timestamp_catch[0]), iso8601=True)
                diff_s = timestamp - timestamp_last
                if len(list_pump) > 0 :
                    if diff_s < list_pump[-1] :
                        list_pump[-1] = diff_s
                break;

    bdf_time = round(sum(list_pump))
    volume = round(bdf_time*pump_surface_flow_ml_per_s)
    print("")
    print("----- PUMP SURFACE ------ (Flow : " + str(pump_surface_flow_ml_per_s) + " ml/s)")
    print("Temps d'activations         : " + str(list_pump) + " (s)")
    print("Temps pour le Bladder full  : " + str(bdf_time) + " s")
    print("Volume d'huile transféré    : " + str(volume) + " ml")
    print("-------------------")
    return (volume,bdf_time)

def print_bypass(dive):
    bypass_all_str = re.findall("BYPASS.+\].*opening (\d+)", dive.log_content)
    if len(bypass_all_str) == 0:
        return 0
    bypass_first = int(bypass_all_str[0])
    bypass_second = [int(x) for x in bypass_all_str[1:]]
    temps_bypass_ms = bypass_first + sum(bypass_second)
    temps_bypass_s = round(float(temps_bypass_ms) / 1000)

    volume = round(temps_bypass_s*bypass_flow_ml_per_s,3)
    print("")
    print("----- BYPASS ------ (Flow : " + str(bypass_flow_ml_per_s) + " ml/s) ")
    print("Temps de bypass             : " + str(temps_bypass_s) + " s")
    print("Volume d'huile transféré    : " + str(volume) + " ml")
    print("-------------------")
    return (volume,temps_bypass_s)

def print_pump(dive):
    surfacing_regex = "\]surfacing"
    surfacing_stage = re.findall("Stage \[(\d)\] surfacing", dive.log_content)
    if len(surfacing_stage) > 0 :
        surfacing_regex = "stage\[" + str(surfacing_stage[0]) + "\]"

    list_pump = list()
    list_before_pump = list()
    log_lines = utils.split_log_lines(dive.log_content)
    timestamp_last = UTCDateTime()

    comp_duration = False
    surfacing = False
    ascent = False
    start = False

    for line in log_lines:
        start_catch = re.findall("bypass opening",line)
        pump_catch = re.findall("PUMP.+\]pump during (\d+)ms", line)
        speed_catch = re.findall("from -(\d+)mbar/s to",line)

        if surfacing :
            filling_catch = re.findall("filling external bladder", line)
            acquisitions_catch = re.findall("Start profil acquisitions", line);
            press_catch = re.findall("0038\]P *\+?(\d+)mbar", line);
            if len(acquisitions_catch) > 0 :
                ascent = True;
            if len(press_catch) > 0 :
                ascent = True;
            if len(filling_catch) > 0 :
                break;

        if len(start_catch) > 0:
            start = True
        if start :
            surfacing_catch = re.findall(surfacing_regex, line)
            if len(surfacing_catch) > 0:
                surfacing = True
            if len(pump_catch) > 0:
                list_pump.append(int(pump_catch[0]))
                if not ascent :
                    list_before_pump.append(int(pump_catch[0]))

    print(list_pump)
    pump_total_time_ms = sum(list_pump)
    pump_before_time_ms = sum(list_before_pump)

    pump_total_time_s = round(float(pump_total_time_ms) / 1000)
    pump_before_time_s = round(float(pump_before_time_ms) / 1000)

    volume = round(pump_total_time_s*pump_deep_flow_ml_per_s)
    volume_before = round(pump_before_time_s*pump_deep_flow_ml_per_s)

    print("")
    print("----- PUMP DEEP ------ (Flow  : " + str(pump_deep_flow_ml_per_s) + " ml/s)")
    print("Temps de pompe en plongee     : " + str(pump_total_time_s) + " s")
    print("Volume d'huile transféré      : " + str(volume) + " ml")
    print("")
    print("Temps de pompe avant remontée : " + str(pump_before_time_s) + " s")
    print("Volume d'huile transféré      : " + str(volume_before) + " ml")
    print("-------------------")
    return (volume,volume_before, pump_total_time_s, pump_before_time_s)

def print_pump_emergency(dive):
    list_pump = list()
    log_lines = utils.split_log_lines(dive.log_content)
    timestamp_last = UTCDateTime()
    comp_duration = False

    for line in log_lines:
        timestamp_catch = re.findall("(\S+):\\[", line)
        pump_catch = re.findall("PUMP.+\]pump during (\d+)ms", line)
        if len(pump_catch) > 0:
            list_pump.append(int(pump_catch[0]))
            timestamp_last = UTCDateTime(str(timestamp_catch[0]), iso8601=True)
            comp_duration = True
        elif len(timestamp_catch) > 0 and comp_duration :
            timestamp = UTCDateTime(str(timestamp_catch[0]), iso8601=True)
            duration_pump_s = round(float(list_pump[-1]) / 1000, 3)
            diff_s = timestamp - timestamp_last
            if diff_s < (duration_pump_s - 10) :
                list_pump[-1] = 0
                print(timestamp)
            comp_duration = False

    pump_total_time_ms = sum(list_pump)
    pump_total_time_s = round(float(pump_total_time_ms) / 1000)
    volume = round(pump_total_time_s*pump_deep_flow_ml_per_s)

    print("")
    print("----- PUMP EMERGENCY ------ (Flow  : " + str(pump_deep_flow_ml_per_s) + " ml/s)")
    print("Temps de pompe en plongee     : " + str(pump_total_time_s) + " s")
    print("Volume d'huile transféré      : " + str(volume) + " ml")
    print("")
    print("-------------------")
    return (volume, pump_total_time_s)

def print_valve(dive):
    list_xfer = utils.find_timestampedUTC_values("need to transfer -(\d+)mL \(valve during (\d+)ms", dive.log_content)
    if len(list_xfer) == 0 :
        list_valve = utils.find_timestampedUTC_values("VALVE.+\]valve opening (\d+)ms", dive.log_content)
        list_press = utils.find_timestampedUTC_values("]P\s*(\+?\-?\d+)mbar", dive.log_content)
        volume_list = list()
        for valve in list_valve :
            press_before = 0
            press_after = 0
            for press in list_press :
                if valve[1] >= press[1] :
                    press_before = int(press[0])
                else :
                    press_after = int(press[0])
                    break;
            press_average = (press_before + press_after) / 2
            flow = sqrt(2.534 * round(float(press_after) / 1000, 3))
            valve_s = round(float(valve[0]) / 1000, 3)
            volume_ml = round(flow * valve_s,3)
            volume_list.append(volume_ml)

        list_valve = [int(tv[0]) for tv in list_valve]
        valve_total_time_ms = sum(list_valve)
        valve_total_time_s = round(float(valve_total_time_ms) / 1000, 3)
        volume_total_ml = round(sum(volume_list),3)
        print("")
        print("----- EVH ------- (Flow : sqrt(2.534 * PRESS))")
        print("Temps de valve en plongee   : " + str(valve_total_time_s) + " s")
        print("Volume d'huile transféré    : " + str(volume_total_ml) + " ml")
        print("------------------")
        print("")
        return (volume_total_ml,valve_total_time_s)
    else :
        list_volume = list()
        list_volume_real = list()
        list_time = list()
        for xfer in list_xfer :
            list_volume.append(int(xfer[0][0]))
            list_time.append(int(xfer[0][1]))
            time_s = int(xfer[0][1]) / 1000

            press_bar = float(math.pow(12750 * int(xfer[0][0]) / int(xfer[0][1]),2)) / 1000.0
            debit_l_min = 288 * sqrt(press_bar/0.881) / 4000
            debit_ml_s = debit_l_min * 1000.0 / 60.0
            real_volume = float(debit_ml_s * int(xfer[0][1])) / 1000
            list_volume_real.append(round(real_volume))

        volume_total_ml = sum(list_volume)
        volume_real_ml = sum(list_volume_real)
        valve_total_time_s = round(float(sum(list_time)) / 1000,3)
        print("")
        print("----- EVH ------- ")
        print("Temps de valve en plongee   : " + str(valve_total_time_s) + " s")
        print("Volume calculé par la bouée : " + str(volume_total_ml) + " ml")
        print("------------------")
        return (volume_total_ml,valve_total_time_s)


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def process(mdives,mfloat) :
    print("*******************")
    print("*******************")
    print("*******************")

    is_emergency = False;
    resum = list()
    icycle = 0;
    for idive, dive in enumerate(mdives):
        if dive.is_dive :
            is_emergency = print_emergency(dive)

            print("")
            print("Date of dive :")
            print (dive.date)
            print("")
            print("Software version :")
            print_software_version(dive)
            print("")
            print("Cycle number :")
            print_cycle_nb(dive)

            bladder_end_ml = 3000
            bladder_start_ascent = 3000
            bypass = 0
            pump = ()
            valve = 0
            pump_surface = 0
            pump_emergency = (0,0)

            if is_emergency and idive+1 < len(mdives) :
                print("")
                print("List of errors :")
                print_errors(dive)
                print_errors(mdives[idive+1])
                print("")
                print("List of warnings :")
                print_warning(dive)
                print_warning(mdives[idive+1])
                print("")
                bypass = print_bypass(dive)
                pump = print_pump(dive)
                valve = print_valve(dive)
                pump_surface = print_bladder_full_time(dive)

                print("ASCENT IN EMERGENCY")
                pump_emergency = print_pump_emergency(mdives[idive+1])
                print("")
                bladder_end_ml = round(bladder_max_ml - bypass[0] - valve[0] + pump[0] + pump_emergency[0] + pump_surface[0])
                bladder_start_ascent = round(bladder_max_ml - bypass[0] - valve[0] + pump[0] + pump_surface[0])
            else :
                print("")
                print("List of errors : ")
                print_errors(dive)
                print("")
                print("List of warnings :")
                print_warning(dive)
                print("")
                bypass = print_bypass(dive)
                pump = print_pump(dive)
                valve = print_valve(dive)
                pump_surface = print_bladder_full_time(dive)
                bladder_end_ml = round(bladder_max_ml - bypass[0] - valve[0] + pump[0] + pump_surface[0])
                bladder_start_ascent = round(bladder_max_ml - bypass[0] - valve[0] + pump[1])

            diff = round(bladder_max_ml - bladder_end_ml)
            print("")
            print ("----- BILAN ------")
            print("Bladder full volume : " + str(bladder_max_ml) + " ml")
            print("Bladder end volume  : " + str(bladder_end_ml) + " ml")
            print("Diff                : " + str(diff) + " ml")
            if not is_emergency :
                print("bladder start ascent: " + str(bladder_start_ascent) + " ml")
            else :
                print("bladder before emergency: " + str(bladder_start_ascent) + " ml")
            print("-------------------")
            print("")

            icycle = icycle + 1
            resum.append((icycle,str(dive.date),bypass[1],pump[2],pump[3],pump_emergency[1],pump_surface[1],valve[0]))

    print("*******************")
    print("*******************")
    print("*******************")

    test_file_path = mfloat + "_test.xlsx"
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(("Bladder init volume : ",bladder_max_ml,"ml"))
    sheet.append(("Pump deep flow      : ",pump_deep_flow_ml_per_s,"ml/s"))
    sheet.append(("bypass flow         : ",bypass_flow_ml_per_s,"ml/s"))
    sheet.append(("Pump surface flow   : ",pump_surface_flow_ml_per_s,"ml/s"))
    sheet.append(())
    sheet.append(("N","Date","Bypass(s)","pump(s)","pump before ascent (s)","pump emergency(s)","pump surface(s)","Valve volume (ml)","bypass volume(ml)","pump (ml)","pump before ascent (ml)", "pump emergency (ml)", "pump surface (ml)"," bladder ascent (ml)","bladder surface (ml)","bladder full (ml)"," bladder diff (ml)"))


    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 30
    sheet.column_dimensions['C'].width = 10
    sheet.column_dimensions['D'].width = 10
    sheet.column_dimensions['E'].width = 20
    sheet.column_dimensions['F'].width = 20
    sheet.column_dimensions['G'].width = 20
    sheet.column_dimensions['H'].width = 20
    sheet.column_dimensions['I'].width = 20
    sheet.column_dimensions['J'].width = 20
    sheet.column_dimensions['K'].width = 20
    sheet.column_dimensions['L'].width = 20
    sheet.column_dimensions['M'].width = 20
    sheet.column_dimensions['N'].width = 20
    sheet.column_dimensions['O'].width = 20
    sheet.column_dimensions['P'].width = 20
    sheet.column_dimensions['Q'].width = 20

    row_nb = 6
    for row in resum :
        sheet.append(row)
        row_nb = row_nb + 1
        sheet.cell(row=row_nb, column=9).value = "=ROUNDUP(C" + str(row_nb) + "*$B$3)"
        sheet.cell(row=row_nb, column=10).value = "=ROUNDUP(D" + str(row_nb) + "*$B$2)"
        sheet.cell(row=row_nb, column=11).value = "=ROUNDUP(E" + str(row_nb) + "*$B$2)"
        sheet.cell(row=row_nb, column=12).value = "=ROUNDUP(F" + str(row_nb) + "*$B$2)"
        sheet.cell(row=row_nb, column=13).value = "=ROUNDUP(G" + str(row_nb) + "*$B$4)"
        sheet.cell(row=row_nb, column=14).value = "=ROUNDUP($B$1-H"+str(row_nb)+"-I"+str(row_nb)+"+K"+str(row_nb)+")"
        sheet.cell(row=row_nb, column=15).value = "=ROUNDUP($B$1-H"+str(row_nb)+"-I"+str(row_nb)+"+J"+str(row_nb)+"+L"+str(row_nb)+")"
        sheet.cell(row=row_nb, column=16).value = "=ROUNDUP($B$1-H"+str(row_nb)+"-I"+str(row_nb)+"+J"+str(row_nb)+"+L"+str(row_nb)+"+M"+str(row_nb)+")"
        sheet.cell(row=row_nb, column=17).value = "=ROUNDUP($B$1 - P"+str(row_nb)+")"

    wb.save(test_file_path)


def main():
    mfloat = infos[0]
    # Set the path for the float
    mfloat_path = "../processed/" + mfloat + "/"
    # Get float number
    mfloat_nb = re.findall("(\d+)$", mfloat)[0]

    # Copy appropriate files in the directory
    for f in glob.glob("../processed/"+mfloat+"/processed/*/*.LOG.h"):
        shutil.copy(f, mfloat_path)

    for f in glob.glob("../processed/"+mfloat+"/processed/*/*.MER.env"):
        shutil.copy(f, mfloat_path)

    for f in glob.glob("../processed/"+mfloat+"/processed/*.LOG.h"):
        shutil.move(f, f[0:len(f)-2])

    for f in glob.glob("../processed/"+mfloat+"/processed/*.MER.env"):
        shutil.move(f, "../processed/"+mfloat+"/processed/"+f[len(f)-21:len(f)-4])


    blockPrint()
    # Build list of all mermaid events recorded by the float
    mevents = events.Events(mfloat_path)
    # Build list of all S41 profiles recorded
    ms41s = sbe41.Profiles(mfloat_path)
    # Build list of all S61 profiles recorded
    ms61s = sbe61.Profiles(mfloat_path)
    # Process data for each dive
    mdives = dives.Dives(mfloat_path, mevents, ms41s,ms61s)
    # Filter dives between begin and end date
    mdives = [dive for dive in mdives.get_dives() if infos[1] <= dive.date <= infos[2]]
    enablePrint()

    with open(mfloat + "_test.log", 'w') as sys.stdout:
        process(mdives,mfloat)


    # Clean directories
    for f in glob.glob(mfloat_path + "/*.LOG.h"):
        os.remove(f)
    for f in glob.glob(mfloat_path + "/*.MER.env"):
        os.remove(f)


if __name__ == "__main__":
    main()
