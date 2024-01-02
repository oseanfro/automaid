# @Author: Frédéric Rocca <fro>
# @Date:   2023-06-09T09:36:17+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: configuration.py
# @Last modified by:   fro
# @Last modified time: 2023-07-06T16:20:20+02:00

import re
from obspy import UTCDateTime
import numpy as np

try :
    import dives
    import utils
except:
    import automaid.dives as dives
    import automaid.utils as utils


## Profil class ##
## Get profile parameters in function of type
## ascent or park
class Profil :
    manual_profil=None
    manual_profil_rate=None
    speed_detection=None
    bin_average_output=None
    include_transition_bin=None
    include_nbin=None
    load_test_sample=None
    p_cut_off=None
    top_bin_interval=None
    top_bin_size=None
    top_bin_max=None
    middle_bin_interval=None
    middle_bin_size=None
    middle_bin_max=None
    bottom_bin_interval=None
    bottom_bin_size=None
    pump_time=None
    speed_start=None
    speed_control=None
    def __init__(self, dive, type="ascent"):
        if type == "park":
            self.manual_profil = 0
            rate = re.findall(":\[PROFIL.+\] +manual_profil_rate=(\d+)",  dive.log_content)
            if len(rate) > 0 :
                self.manual_profil_rate = rate[0][0]
        else :
            self.manual_profil = 1
            speed_detection = re.findall(":\[PROFIL.+\] +speed_detection=(\d+)",  dive.log_content)
            bin_average_output = re.findall(":\[PROFIL.+\] +bin_average_output=(\d+)",  dive.log_content)
            include_transition_bin = re.findall(":\[PROFIL.+\] +include_transition_bin=(\d+)",  dive.log_content)
            include_nbin = re.findall(":\[PROFIL.+\] +include_nbin=(\d+)",  dive.log_content)
            load_test_sample = re.findall(":\[PROFIL.+\] +load_test_sample=(\d+)",  dive.log_content)
            p_cut_off = re.findall(":\[PROFIL.+\] +p_cut_off=(\d+)",  dive.log_content)
            top_bin_interval = re.findall(":\[PROFIL.+\] +top_bin_interval=(\d+)",  dive.log_content)
            top_bin_size = re.findall(":\[PROFIL.+\] +top_bin_size=(\d+)",  dive.log_content)
            top_bin_max = re.findall(":\[PROFIL.+\] +top_bin_max=(\d+)",  dive.log_content)
            middle_bin_interval = re.findall(":\[PROFIL.+\] +middle_bin_interval=(\d+)",  dive.log_content)
            middle_bin_size = re.findall(":\[PROFIL.+\] +middle_bin_size=(\d+)",  dive.log_content)
            middle_bin_max = re.findall(":\[PROFIL.+\] +middle_bin_max=(\d+)",  dive.log_content)
            bottom_bin_interval = re.findall(":\[PROFIL.+\] +bottom_bin_interval=(\d+)",  dive.log_content)
            bottom_bin_size = re.findall(":\[PROFIL.+\] +bottom_bin_size=(\d+)",  dive.log_content)
            pump_time = re.findall(":\[PROFIL.+\] +pump_time=(\d+)",  dive.log_content)
            speed_start = re.findall(":\[PROFIL.+\] +speed_start=(\d+)",  dive.log_content)
            speed_control = re.findall(":\[PROFIL.+\] +speed_control=(\d+)",  dive.log_content)
            if len(speed_detection) > 0 :
                self.speed_detection = speed_detection[0][0]
            if len(bin_average_output) > 0 :
                self.bin_average_output = bin_average_output[0][0]
            if len(include_transition_bin) > 0 :
                self.include_transition_bin = include_transition_bin[0][0]
            if len(include_nbin) > 0 :
                self.include_nbin = include_nbin[0][0]
            if len(load_test_sample) > 0 :
                self.load_test_sample = load_test_sample[0][0]
            if len(p_cut_off) > 0 :
                self.p_cut_off = p_cut_off[0][0]
            if len(top_bin_interval) > 0 :
                self.top_bin_interval = top_bin_interval[0][0]
            if len(top_bin_size) > 0 :
                self.top_bin_size = top_bin_size[0][0]
            if len(top_bin_max) > 0 :
                self.top_bin_max = top_bin_max[0][0]
            if len(middle_bin_interval) > 0 :
                self.middle_bin_interval = middle_bin_interval[0][0]
            if len(middle_bin_max) > 0 :
                self.middle_bin_max = middle_bin_max[0][0]
            if len(middle_bin_size) > 0 :
                self.middle_bin_size = middle_bin_size[0][0]
            if len(bottom_bin_interval) > 0 :
                self.bottom_bin_interval = bottom_bin_interval[0][0]
            if len(bottom_bin_size) > 0 :
                self.bottom_bin_size = bottom_bin_size[0][0]
            if len(pump_time) > 0 :
                self.pump_time = pump_time[0][0]
            if len(speed_start) > 0 :
                self.speed_start = speed_start[0][0]
            if len(speed_control) > 0 :
                self.speed_control = speed_control[0][0]

## Stage class ##
## Store stage parameters and profil associated
class Stage :
    type=None
    pressure_ref_mbar=None
    pressure_diff_mbar=None
    duration_s=None
    duration_estimated_s=None
    expiration_date_s=None
    scientific=None
    profil=None
    def __init__(self,type=None,pressure_ref_mbar=None,pressure_diff_mbar=None,duration_s=None,expiration_date_s=None,scientific=None, profil=None, duration_estimated_s=None):
        self.type = type
        self.pressure_ref_mbar = pressure_ref_mbar
        self.duration_s = duration_s
        self.expiration_date_s = expiration_date_s
        self.scientific = scientific
        self.duration_estimated_s = duration_estimated_s
        self.profil = profil

class Configuration :
    bypass_1st_ms=None
    bypass_1st_ms_stored=None
    bypass_max_ms=None
    bypass_max_ms_stored=None
    valve_max_ms=None
    valve_max_ms_stored=None
    valve_coeff=None
    valve_coeff_stored=None
    pump_max_ms=None
    pump_max_ms_stored=None
# parameters for pump 2000m
    pump_power_percent=None
    pump_power_percent_stored=None
    pump_coeff=None
    pump_coeff_stored=None
    pump_fill_power_percent=None
    pump_fill_power_percent_stored=None
# parameters for pump 4000m
    pump_deep_outflow_uL_mn_V=None
    pump_deep_outflow_uL_mn_V_stored=None
    pump_deep_linear_slope=None
    pump_deep_linear_slope_stored=None
    pump_deep_linear_y_intercept=None
    pump_deep_linear_y_intercept_stored=None
# speed and zona parameters
    speed_mbar_per_s=None
    speed_mbar_per_s_stored=None
# Surface parameters
    surface_mbar=None
    surface_mbar_stored=None
# Near parameters
    near_mbar=None
    near_mbar_stored=None
    near_min_mbar_per_s=None
    near_min_mbar_per_s_stored=None
    near_mbar_per_s=None
    near_mbar_per_s_stored=None
    near_max_mbar_per_s=None
    near_max_mbar_per_s_stored=None
# Middle parameters
    middle_mbar_per_s = None
# Far parameters
    far_mbar=None
    far_mbar_stored=None
    far_mbar_per_s=None
    far_mbar_per_s_stored=None
    ascent_mbar_per_s=None
    ascent_mbar_per_s_stored=None
    dead_delay_s=None
    dead_delay_s_stored=None
    oil_coeff_num=None
    oil_coeff_num_stored=None
    oil_coeff_den=None
    oil_coeff_den_stored=None
    stab_counts=None
    stab_counts_stored=None
    min_surface_delay_s=None
    min_surface_delay_s_stored=None
    max_surface_delay_s=None
    max_surface_delay_s_stored=None
    minimum_mission_time_mn=None
    minimum_mission_time_mn_stored=None
# landing parameters
    dv_landing_ml=None
    dv_landing_ml_stored=None
    landing_confirmation=None
    landing_confirmation_stored=None
    p2t_addr=None
    p2t_historic_depth=None
    p2t_period_ms=None
    p2t_offset_mbar=None
    p2t_log_mbar=None
    p2t_log_mdegc=None
    stages=None
    stages_nb=None
    def __init__(self, dive):
        if not dive.is_complete_dive :
            return
        if dive.is_init :
            return
        bypass = re.findall(":\[.+\] +bypass (\d+)ms (\d+)ms \((\d+)ms (\d+)ms stored\)",  dive.log_content)
        valve = re.findall(":\[.+\] +valve (\d+)ms (\d+) \((\d+)ms (\d+) stored\)",  dive.log_content)
        pump_2000m = re.findall(":\[.+\] +pump (\d+)ms (\d+)% (\d+) (\d+)% \((\d+)ms (\d+)% (\d+) (\d+)% stored\)",  dive.log_content)
        pump_4000m = re.findall(":\[.+\] +pump (\d+)ms (\d+) (\d+) (\d+) \((\d+)ms (\d+) (\d+) (\d+) stored\)",  dive.log_content)
        rate = re.findall(":\[.+\] +rate (\d+)mbar/s \((\d+)mbar/s stored\)",  dive.log_content)
        surface = re.findall(":\[.+\] +surface (\d+)mbar \((\d+)mbar stored\)",  dive.log_content)
        near_2000m = re.findall(":\[.+\] +near (\d+)mbar (\d+)mbar/s \((\d+)mbar (\d+)mbar/s stored\)",  dive.log_content)
        near_4000m = re.findall(":\[.+\] +near (\d+)mbar (\d+):(\d+):(\d+)mbar/s \((\d+)mbar (\d+):(\d+):(\d+)mbar/s stored\)",  dive.log_content)
        middle = re.findall(":\[.+\] +middle (\d+)mbar/s \((\d+)mbar/s stored\)",  dive.log_content)
        far = re.findall(":\[.+\] +far (\d+)mbar (\d+)mbar/s \((\d+)mbar (\d+)mbar/s stored\)",  dive.log_content)
        ascent = re.findall(":\[.+\] +ascent (\d+)mbar/s \((\d+)mbar/s stored\)",  dive.log_content)
        dead = re.findall(":\[.+\] +dead (\d+)s \((\d+)s stored\)",  dive.log_content)
        coeff = re.findall(":\[.+\] +coeff (\d+)/(\d+) \((\d+)/(\d+) stored\)",  dive.log_content)
        stab = re.findall(":\[.+\] +stab (\d+) \((\d+) stored\)",  dive.log_content)
        delay = re.findall(":\[.+\] +delay (\d+)s (\d+)s \((\d+)s (\d+)s stored\)",  dive.log_content)
        mmtime = re.findall(":\[.+\] +mmtime (\d+)min \((\d+)min stored\)",  dive.log_content)
        dv_landing = re.findall(":\[.+\] +dv_landing (\d+)ml \((\d+)ml stored\)",  dive.log_content)
        conf_landing = re.findall(":\[.+\] +landing confirmation (\d+) \((\d+) stored\)",  dive.log_content)
        p2t_1 = re.findall(":\[.+\] +p2t(\d+): (\d+)x(\d+)ms, offset (\d+)mbar",  dive.log_content)
        p2t_2 = re.findall(":\[.+\] +p2t\d+: dp (\d+)mbar",  dive.log_content)

        if len(bypass) > 0 :
            self.bypass_1st_ms = int(bypass[0][0])
            self.bypass_max_ms = int(bypass[0][1])
            self.bypass_1st_ms_stored = int(bypass[0][2])
            self.bypass_max_ms_stored = int(bypass[0][3])
        if len(valve) > 0 :
            self.valve_max_ms=int(valve[0][0])
            self.valve_max_ms_stored=int(valve[0][2])
            self.valve_coeff=int(valve[0][1])
            self.valve_coeff_stored=int(valve[0][3])
        if len(pump_2000m) > 0 :
            self.pump_max_ms=int(pump_2000m[0][0])
            self.pump_max_ms_stored=int(pump_2000m[0][4])
            self.pump_power_percent=int(pump_2000m[0][1])
            self.pump_power_percent_stored=int(pump_2000m[0][5])
            self.pump_coeff=int(pump_2000m[0][2])
            self.pump_coeff_stored=int(pump_2000m[0][6])
            self.pump_fill_power_percent=int(pump_2000m[0][3])
            self.pump_fill_power_percent_stored=int(pump_2000m[0][7])
        if len(pump_4000m) > 0 :
            self.pump_max_ms=int(pump_4000m[0][0])
            self.pump_max_ms_stored=int(pump_4000m[0][4])
            self.pump_deep_outflow_uL_mn_V=int(pump_4000m[0][1])
            self.pump_deep_outflow_uL_mn_V_stored=int(pump_4000m[0][5])
            self.pump_deep_linear_slope=int(pump_4000m[0][2])
            self.pump_deep_linear_slope_stored=int(pump_4000m[0][6])
            self.pump_deep_linear_y_intercept=int(pump_4000m[0][3])
            self.pump_deep_linear_y_intercept_stored=int(pump_4000m[0][7])
        if len(rate) > 0 :
            self.speed_mbar_per_s=int(rate[0][0])
            self.speed_mbar_per_s_stored=int(rate[0][1])
        if len(surface) > 0 :
            self.surface_mbar=int(surface[0][0])
            self.surface_mbar_stored=int(surface[0][1])
        if len(near_2000m) > 0 :
            self.near_mbar=int(near_2000m[0][0])
            self.near_mbar_stored=int(near_2000m[0][2])
            self.near_mbar_per_s=int(near_2000m[0][1])
            self.near_mbar_per_s_stored=int(near_2000m[0][3])
        if len(near_4000m) > 0 :
            self.near_mbar=int(near_4000m[0][0])
            self.near_mbar_stored=int(near_4000m[0][4])
            self.near_min_mbar_per_s=int(near_4000m[0][1])
            self.near_min_mbar_per_s_stored=int(near_4000m[0][5])
            self.near_mbar_per_s=int(near_4000m[0][2])
            self.near_mbar_per_s_stored=int(near_4000m[0][6])
            self.near_max_mbar_per_s=int(near_4000m[0][3])
            self.near_max_mbar_per_s_stored=int(near_4000m[0][7])
        if len(middle) > 0 :
            self.middle_mbar_per_s=int(middle[0][0])
            self.middle_mbar_per_s_stored=int(middle[0][1])
        if len(far) > 0 :
            self.far_mbar=int(far[0][0])
            self.far_mbar_stored=int(far[0][2])
            self.far_mbar_per_s=int(far[0][1])
            self.far_mbar_per_s_stored=int(far[0][3])
        if len(ascent) > 0 :
            self.ascent_mbar_per_s=int(ascent[0][0])
            self.ascent_mbar_per_s_stored=int(ascent[0][1])
        if len(dead) > 0 :
            self.dead_delay_s=int(dead[0][0])
            self.dead_delay_s_stored=int(dead[0][1])
        if len(coeff) > 0 :
            self.oil_coeff_num=int(coeff[0][0])
            self.oil_coeff_num_stored=int(coeff[0][2])
            self.oil_coeff_den=int(coeff[0][1])
            self.oil_coeff_den_stored=int(coeff[0][3])
        if len(stab) > 0 :
            self.stab_counts=int(stab[0][0])
            self.stab_counts_stored=int(stab[0][1])
        if len(delay) > 0 :
            self.min_surface_delay_s=int(delay[0][0])
            self.min_surface_delay_s_stored=int(delay[0][2])
            self.max_surface_delay_s=int(delay[0][1])
            self.max_surface_delay_s_stored=int(delay[0][3])
        if len(mmtime) > 0 :
            self.minimum_mission_time_mn=int(mmtime[0][0])
            self.minimum_mission_time_mn_stored=int(mmtime[0][1])
        if len(dv_landing) > 0 :
            self.dv_landing_ml=int(dv_landing[0][0])
            self.dv_landing_ml_stored=int(dv_landing[0][1])
        if len(conf_landing) > 0 :
            self.landing_confirmation=int(conf_landing[0][0])
            self.landing_confirmation_stored=int(conf_landing[0][1])
        if len(p2t_1) > 0 :
            self.p2t_addr=int(p2t_1[0][0])
            self.p2t_historic_depth=int(p2t_1[0][1])
            self.p2t_period_ms=int(p2t_1[0][2])
            self.p2t_offset_mbar=int(p2t_1[0][3])
        if len(p2t_2) > 0 :
            self.p2t_log_mbar=int(p2t_2[0][0])
            self.p2t_log_mdegc=-1
        # get all stages
        self.stages = []
        stage_nb = 0
        while stage_nb < 6 :
            classic_LOG0080 = re.findall(":\[STAGE.+,0080\]Stage \["+str(stage_nb)+"\] (-?\d+)mbar \(\+/-(\d+)mbar\) (-?\d+)s \(<(-?\d+)s\) ?(\w+)?", dive.log_content)
            classic_LOG0375 = re.findall(":\[STAGE.+,0375\]Stage \["+str(stage_nb)+"\] (-?\d+)mbar \(\+/-(\d+)mbar\) (-?\d+)s ?(\w+)?", dive.log_content)
            surfacing_LOG0091 = re.findall(":\[STAGE.+,0091\]Stage \["+str(stage_nb)+"\] surfacing (-?\d+)s \(<(-?\d+)s\) ?(\w+)?", dive.log_content)
            if len(classic_LOG0080) > 0 :
                press_ref_mbar=int(classic_LOG0080[0][0])
                pressure_diff_mbar=int(classic_LOG0080[0][1])
                duration_s=int(classic_LOG0080[0][2])
                expiration_date_s=int(classic_LOG0080[0][3])
                scientific = ""
                profil=None
                if len(classic_LOG0080[0]) > 4 :
                    scientific=classic_LOG0080[0][4]
                    if "SBE61" in scientific:
                        profil=Profil(dive,"park")
                self.stages.append(Stage("classic",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific,profil))
                stage_nb = stage_nb + 1
            elif len(classic_LOG0375) > 0 :
                press_ref_mbar=int(classic_LOG0375[0][0])
                pressure_diff_mbar=int(classic_LOG0375[0][1])
                duration_s=-1
                expiration_date_s=int(classic_LOG0375[0][2])
                scientific = ""
                profil=None
                if len(classic_LOG0375[0]) > 3 :
                    scientific=classic_LOG0375[0][3]
                    if "SBE61" in scientific:
                        profil=Profil(dive,"park")
                self.stages.append(Stage("classic",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific,profil))
            elif len(surfacing_LOG0091) > 0 :
                press_ref_mbar=0
                pressure_diff_mbar=0
                duration_s=int(surfacing_LOG0091[0][0])
                expiration_date_s=int(surfacing_LOG0091[0][1])
                scientific = ""
                profil=None
                if len(surfacing_LOG0091[0]) > 2 :
                    scientific=surfacing_LOG0091[0][2]
                    if "SBE61" in scientific:
                        profil=Profil(dive,"ascent")
                self.stages.append(
                Stage("surfacing",
                press_ref_mbar,
                pressure_diff_mbar,
                duration_s,
                expiration_date_s,
                scientific,
                profil))
                stage_nb = stage_nb + 1
            else :
                break
        self.stages_nb = stage_nb
        stage_nb = 0
        while stage_nb < len(self.stages):
            if self.stages[stage_nb].duration_s < 0 :
                if stage_nb == 0 :
                    self.stages[stage_nb].duration_estimated_s = self.stages[stage_nb].expiration_date_s
                else :
                    self.stages[stage_nb].duration_estimated_s = self.stages[stage_nb].expiration_date_s - self.stages[stage_nb-1].expiration_date_s
            else :
                self.stages[stage_nb].duration_estimated_s = self.stages[stage_nb].duration_s
            stage_nb = stage_nb + 1
    def __str__(self):
        attrs = vars(self)
        string = ', '.join("%s: %s" % item for item in attrs.items())
        return string
