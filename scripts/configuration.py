import dives
import utils
import re
from obspy import UTCDateTime
import numpy as np

class Stage :
    stage_type=None
    pressure_ref_mbar=None
    pressure_diff_mbar=None
    duration_s=None
    duration_estimated_s=None
    expiration_date_s=None
    scientific_type=None
    def __init__(self, stage_type=None,pressure_ref_mbar=None,pressure_diff_mbar=None,duration_s=None,expiration_date_s=None,scientific_type=None, duration_estimated_s=None):
        self.stage_type = stage_type
        self.pressure_ref_mbar = pressure_ref_mbar
        self.duration_s = duration_s
        self.expiration_date_s = expiration_date_s
        self.scientific_type = scientific_type
        self.duration_estimated_s = duration_estimated_s

class Sbe41_parameters :
    dsreplyformat=None
    addtimingdelays=None
    outputdensity=None
    echocmd=None
    outputrt=None
    outputpts=None
    outputsn=None
    outputpressure=None
    pcutoff=None
    tswait=None
    pumpfastpt=None
    samplerate=None
    top_bin_interval=None
    top_bin_size=None
    top_bin_max=None
    middle_bin_interval=None
    middle_bin_size=None
    middle_bin_max=None
    bottom_bin_interval=None
    bottom_bin_size=None
    includetransitionbin=None
    includenbin=None
    autobinavg=None
    def __init__(self, dive):
        dsreplyformat = re.findall(" +dsreplyformat=(\d+).*",  dive.log_content)
        addtimingdelays = re.findall(" +addtimingdelays=(\d+).*",  dive.log_content)
        outputdensity = re.findall(" +outputdensity=(\d+).*",  dive.log_content)
        echocmd = re.findall(" +echocmd=(\d+).*",  dive.log_content)
        outputrt = re.findall(" +outputrt=(\d+).*",  dive.log_content)
        outputpts = re.findall(" +outputpts=(\d+).*",  dive.log_content)
        outputsn = re.findall(" +outputsn=(\d+).*",  dive.log_content)
        outputpressure = re.findall(" +outputpressure=(\d+).*",  dive.log_content)
        pcutoff = re.findall(" +pcutoff=(\d+).*",  dive.log_content)
        tswait = re.findall(" +tswait=(\d+).*",  dive.log_content)
        pumpfastpt = re.findall(" +pumpfastpt=(\d+).*",  dive.log_content)
        samplerate = re.findall(" +samplerate=(\d+).*",  dive.log_content)
        mmtime = re.findall(" +mmtime=(\d+).*",  dive.log_content)
        top_bin_interval = re.findall(" +top_bin_interval=(\d+).*",  dive.log_content)
        top_bin_size = re.findall(" +top_bin_size=(\d+).*",  dive.log_content)
        top_bin_max = re.findall(" +top_bin_max=(\d+).*",  dive.log_content)
        middle_bin_interval = re.findall(" +middle_bin_interval=(\d+).*",  dive.log_content)
        middle_bin_size = re.findall(" +middle_bin_size=(\d+).*",  dive.log_content)
        middle_bin_max = re.findall(" +middle_bin_max=(\d+).*",  dive.log_content)
        bottom_bin_interval = re.findall(" +bottom_bin_interval=(\d+).*",  dive.log_content)
        bottom_bin_size = re.findall(" +bottom_bin_size=(\d+).*",  dive.log_content)
        includetransitionbin = re.findall(" +includetransitionbin=(\d+).*",  dive.log_content)
        includenbin = re.findall(" +includenbin=(\d+).*",  dive.log_content)
        autobinavg = re.findall(" +autobinavg=(\d+).*",  dive.log_content)
        if len(dsreplyformat) > 0 :
            self.dsreplyformat = int(dsreplyformat[-1][0])
        if len(addtimingdelays) > 0 :
            self.addtimingdelays = int(addtimingdelays[-1][0])
        if len(outputdensity) > 0 :
            self.outputdensity = int(outputdensity[-1][0])
        if len(echocmd) > 0 :
            self.echocmd = int(echocmd[-1][0])
        if len(outputrt) > 0 :
            self.outputrt = int(outputrt[-1][0])
        if len(outputpts) > 0 :
            self.outputpts = int(outputpts[-1][0])
        if len(outputsn) > 0 :
            self.outputsn = int(outputsn[-1][0])
        if len(outputpressure) > 0 :
            self.outputpressure = int(outputpressure[-1][0])
        if len(pcutoff) > 0 :
            self.pcutoff = int(pcutoff[-1][0])
        if len(tswait) > 0 :
            self.tswait = int(tswait[-1][0])
        if len(pumpfastpt) > 0 :
            self.pumpfastpt = int(pumpfastpt[-1][0])
        if len(samplerate) > 0 :
            self.samplerate = int(samplerate[-1][0])
        if len(mmtime) > 0 :
            self.mmtime = int(mmtime[-1][0])
        if len(top_bin_interval) > 0 :
            self.top_bin_interval = int(top_bin_interval[-1][0])
        if len(top_bin_size) > 0 :
            self.top_bin_size = int(top_bin_size[-1][0])
        if len(top_bin_max) > 0 :
            self.top_bin_max = int(top_bin_max[-1][0])
        if len(middle_bin_interval) > 0 :
            self.middle_bin_interval = int(middle_bin_interval[-1][0])
        if len(middle_bin_size) > 0 :
            self.middle_bin_size = int(middle_bin_size[-1][0])
        if len(middle_bin_max) > 0 :
            self.middle_bin_max = int(middle_bin_max[-1][0])
        if len(bottom_bin_interval) > 0 :
            self.bottom_bin_interval = int(bottom_bin_interval[-1][0])
        if len(bottom_bin_size) > 0 :
            self.bottom_bin_size = int(bottom_bin_size[-1][0])
        if len(includetransitionbin) > 0 :
            self.includetransitionbin = int(includetransitionbin[-1][0])
        if len(includenbin) > 0 :
            self.includenbin = int(includenbin[-1][0])
        if len(autobinavg) > 0 :
            self.autobinavg = int(autobinavg[-1][0])

class Sbe41_pilots :
    continiousprofile=None
    speeddetection=None
    hexoutput=None
    binaverageoutput=None
    manualprofilerate=None
    runningpumpbeforeprofile=None
    speedstart=None
    speedcontrol=None
    def __init__(self, dive):
        continiousprofile = re.findall(" +continiousprofile=(\d+).*",  dive.log_content)
        speeddetection = re.findall(" +speeddetection=(\d+).*",  dive.log_content)
        hexoutput = re.findall(" +hexoutput=(\d+).*",  dive.log_content)
        binaverageoutput = re.findall(" +binaverageoutput=(\d+).*",  dive.log_content)
        manualprofilerate = re.findall(" +manualprofilerate=(\d+).*",  dive.log_content)
        runningpumpbeforeprofile = re.findall(" +runningpumpbeforeprofile=(\d+).*",  dive.log_content)
        speedstart = re.findall(" +speedstart=(\d+).*",  dive.log_content)
        speedcontrol = re.findall(" +speedcontrol=(\d+).*",  dive.log_content)
        if len(continiousprofile) > 0 :
            self.continiousprofile = int(continiousprofile[-1][0])
        if len(speeddetection) > 0 :
            self.speeddetection = int(speeddetection[-1][0])
        if len(hexoutput) > 0 :
            self.hexoutput = int(hexoutput[-1][0])
        if len(binaverageoutput) > 0 :
            self.binaverageoutput = int(binaverageoutput[-1][0])
        if len(manualprofilerate) > 0 :
            self.manualprofilerate = int(manualprofilerate[-1][0])
        if len(runningpumpbeforeprofile) > 0 :
            self.runningpumpbeforeprofile = int(runningpumpbeforeprofile[-1][0])
        if len(speedstart) > 0 :
            self.speedstart = int(speedstart[-1][0])
        if len(speedcontrol) > 0 :
            self.speedcontrol = int(speedcontrol[-1][0])

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
    pump_power_percent=None
    pump_power_percent_stored=None
    pump_coeff=None
    pump_coeff_stored=None
    pump_fill_power_percent=None
    pump_fill_power_percent_stored=None
    speed_mbar_per_s=None
    speed_mbar_per_s_stored=None
    surface_mbar=None
    surface_mbar_stored=None
    near_mbar=None
    near_mbar_stored=None
    near_mbar_per_s=None
    near_mbar_per_s_stored=None
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
    dv_landing_ml=None
    dv_landing_ml_stored=None
    p2t_addr=None
    p2t_historic_depth=None
    p2t_period_ms=None
    p2t_offset_mbar=None
    p2t_log_mbar=None
    p2t_log_mdegc=None
    stages=None
    stages_nb=None
    sbe41_parameters=None
    sbe41_pilots=None
    def __init__(self, dive):
        if not dive.is_complete_dive :
            return
        if dive.is_init :
            return
        bypass = re.findall(":\[BYCMD.+\] +bypass (\d+)ms (\d+)ms \((\d+)ms (\d+)ms stored\)",  dive.log_content)
        valve = re.findall(":\[BYCMD.+\] +valve (\d+)ms (\d+) \((\d+)ms (\d+) stored\)",  dive.log_content)
        pump = re.findall(":\[BYCMD.+\] +pump (\d+)ms (\d+)% (\d+) (\d+)% \((\d+)ms (\d+)% (\d+) (\d+)% stored\)",  dive.log_content)
        rate = re.findall(":\[BYCMD.+\] +rate (\d+)mbar/s \((\d+)mbar/s stored\)",  dive.log_content)
        surface = re.findall(":\[BYCMD.+\] +surface (\d+)mbar \((\d+)mbar stored\)",  dive.log_content)
        near = re.findall(":\[BYCMD.+\] +near (\d+)mbar (\d+)mbar/s \((\d+)mbar (\d+)mbar/s stored\)",  dive.log_content)
        far = re.findall(":\[BYCMD.+\] +far (\d+)mbar (\d+)mbar/s \((\d+)mbar (\d+)mbar/s stored\)",  dive.log_content)
        ascent = re.findall(":\[BYCMD.+\] +ascent (\d+)mbar/s \((\d+)mbar/s stored\)",  dive.log_content)
        dead = re.findall(":\[BYCMD.+\] +dead (\d+)s \((\d+)s stored\)",  dive.log_content)
        coeff = re.findall(":\[BYCMD.+\] +coeff (\d+)/(\d+) \((\d+)/(\d+) stored\)",  dive.log_content)
        stab = re.findall(":\[BYCMD.+\] +stab (\d+) \((\d+) stored\)",  dive.log_content)
        delay = re.findall(":\[BYCMD.+\] +delay (\d+)s (\d+)s \((\d+)s (\d+)s stored\)",  dive.log_content)
        mmtime = re.findall(":\[BYCMD.+\] +mmtime (\d+)min \((\d+)min stored\)",  dive.log_content)
        dv_landing = re.findall(":\[BYCMD.+\] +dv_landing (\d+)ml \((\d+)ml stored\)",  dive.log_content)
        p2t_1 = re.findall(":\[MKDCMD.+\] +p2t(\d+): (\d+)x(\d+)ms, offset (\d+)mbar",  dive.log_content)
        p2t_2 = re.findall(":\[P2TCMD.+\] +p2t\d+: dp (\d+)mbar, dt (\d+)mdegC",  dive.log_content)
        sbe41_parameters = re.findall(":\[SBE41.+\]SBE41 parameters.*",  dive.log_content)
        sbe41_pilots = re.findall(":\[SBE41.+\]SBE41 pilot.*",  dive.log_content)

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
        if len(pump) > 0 :
            self.pump_max_ms=int(pump[0][0])
            self.pump_max_ms_stored=int(pump[0][4])
            self.pump_power_percent=int(pump[0][1])
            self.pump_power_percent_stored=int(pump[0][5])
            self.pump_coeff=int(pump[0][2])
            self.pump_coeff_stored=int(pump[0][6])
            self.pump_fill_power_percent=int(pump[0][3])
            self.pump_fill_power_percent_stored=int(pump[0][7])
        if len(rate) > 0 :
            self.speed_mbar_per_s=int(rate[0][0])
            self.speed_mbar_per_s_stored=int(rate[0][1])
        if len(surface) > 0 :
            self.surface_mbar=int(surface[0][0])
            self.surface_mbar_stored=int(surface[0][1])
        if len(near) > 0 :
            self.near_mbar=int(near[0][0])
            self.near_mbar_stored=int(near[0][2])
            self.near_mbar_per_s=int(near[0][1])
            self.near_mbar_per_s_stored=int(near[0][3])
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
        if len(p2t_1) > 0 :
            self.p2t_addr=int(p2t_1[0][0])
            self.p2t_historic_depth=int(p2t_1[0][1])
            self.p2t_period_ms=int(p2t_1[0][2])
            self.p2t_offset_mbar=int(p2t_1[0][3])
        if len(p2t_2) > 0 :
            self.p2t_log_mbar=int(p2t_2[0][0])
            self.p2t_log_mdegc=int(p2t_2[0][1])
        if len(sbe41_parameters) > 0:
            self.sbe41_parameters = Sbe41_parameters(dive)
        if len(sbe41_pilots) > 0:
            self.sbe41_pilots = Sbe41_pilots(dive)
        # get all stages
        self.stages = []
        stage_nb = 0
        while stage_nb < 6 :
            classic_LOG0080 = re.findall(":\[STAGE.+,0080\]Stage \["+str(stage_nb)+"\] (-?\d+)mbar \(\+/-(\d+)mbar\) (-?\d+)s \(<(-?\d+)s\) ?(\w+)?", dive.log_content)
            classic_LOG0375 = re.findall(":\[STAGE.+,0375\]Stage \["+str(stage_nb)+"\] (-?\d+)mbar \(\+/-(\d+)mbar\) (-?\d+)s ?(\w+)?", dive.log_content)
            surfacing_LOG0091 = re.findall(":\[STAGE.+,0091\]Stage \["+str(stage_nb)+"\] surfacing (-?\d+)s \(<(-?\d+)s\) ?(\w+)?", dive.log_content)
            landing_LOG0081 = re.findall(":\[STAGE.+,0081\]Stage \["+str(stage_nb)+"\] landing (-?\d+)mbar (-?\d+)s \(<(\d+)s\) ?(\w+)?", dive.log_content)
            landing_LOG0374 = re.findall(":\[STAGE.+,0374\]Stage \["+str(stage_nb)+"\] landing (-?\d+)mbar \(\+/-(\d+)mbar\) (-?\d+)s ?(\w+)?", dive.log_content)
            if len(classic_LOG0080) > 0 :
                press_ref_mbar=int(classic_LOG0080[0][0])
                pressure_diff_mbar=int(classic_LOG0080[0][1])
                duration_s=int(classic_LOG0080[0][2])
                expiration_date_s=int(classic_LOG0080[0][3])
                scientific_type = ""
                if len(classic_LOG0080[0]) > 4 :
                    scientific_type=classic_LOG0080[0][4]
                self.stages.append(Stage("classic",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific_type))
                stage_nb = stage_nb + 1
            elif len(classic_LOG0375) > 0 :
                press_ref_mbar=int(classic_LOG0375[0][0])
                pressure_diff_mbar=int(classic_LOG0375[0][1])
                duration_s=-1
                expiration_date_s=int(classic_LOG0375[0][2])
                scientific_type = ""
                if len(classic_LOG0375[0]) > 3 :
                    scientific_type=classic_LOG0375[0][3]
                self.stages.append(Stage("classic",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific_type))
            elif len(surfacing_LOG0091) > 0 :
                press_ref_mbar=0
                pressure_diff_mbar=0
                duration_s=int(surfacing_LOG0091[0][0])
                expiration_date_s=int(surfacing_LOG0091[0][1])
                scientific_type = ""
                if len(surfacing_LOG0091[0]) > 2 :
                    scientific_type=surfacing_LOG0091[0][2]
                self.stages.append(Stage("surfacing",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific_type))
                stage_nb = stage_nb + 1
            elif len(landing_LOG0081) > 0 :
                press_ref_mbar=int(landing_LOG0081[0][0])
                pressure_diff_mbar=0
                duration_s=int(landing_LOG0081[0][1])
                expiration_date_s=int(landing_LOG0081[0][2])
                scientific_type = ""
                if len(landing_LOG0081[0]) > 3 :
                    scientific_type=landing_LOG0081[0][3]
                self.stages.append(Stage("landing",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific_type))
                stage_nb = stage_nb + 1
            elif len(landing_LOG0374) > 0 :
                press_ref_mbar=int(landing_LOG0374[0][0])
                pressure_diff_mbar=int(landing_LOG0374[0][1])
                duration_s=-1
                expiration_date_s=int(landing_LOG0374[0][2])
                scientific_type = ""
                if len(landing_LOG0374[0]) > 3 :
                    scientific_type=landing_LOG0374[0][3]
                self.stages.append(Stage("landing",press_ref_mbar,pressure_diff_mbar,duration_s,expiration_date_s,scientific_type))
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
        string = ""
        string += 'bypass_1st_ms={0:d},bypass_1st_ms_stored={1:d},bypass_max_ms={2:d},bypass_max_ms_stored={3:d}\r\n'.format(
        self.bypass_1st_ms,
        self.bypass_1st_ms_stored,
        self.bypass_max_ms,
        self.bypass_max_ms_stored)
        string += 'valve_max_ms={0:d},valve_max_ms_stored={1:d},valve_coeff={2:d},valve_coeff_stored={3:d}\r\n'.format(
        self.valve_max_ms,
        self.valve_max_ms_stored,
        self.valve_coeff,
        self.valve_coeff_stored)
        string += 'pump_max_ms={0:d},pump_max_ms_stored={1:d},pump_power_percent={2:d},pump_power_percent_stored={3:d},pump_coeff={4:d},pump_coeff_stored={5:d},pump_fill_power_percent={6:d},pump_fill_power_percent_stored={7:d}\r\n'.format(
        self.pump_max_ms,
        self.pump_max_ms_stored,
        self.pump_power_percent,
        self.pump_power_percent_stored,
        self.pump_coeff,
        self.pump_coeff_stored,
        self.pump_fill_power_percent,
        self.pump_fill_power_percent_stored)
        string += 'speed_mbar_per_s={0:d},speed_mbar_per_s_stored={1:d}\r\n'.format(
        self.speed_mbar_per_s,
        self.speed_mbar_per_s_stored)
        string += 'surface_mbar={0:d},surface_mbar_stored={1:d}\r\n'.format(
        self.surface_mbar,
        self.surface_mbar_stored)
        string += 'near_mbar={0:d},near_mbar_stored={1:d},near_mbar_per_s={2:d},near_mbar_per_s_stored={3:d}\r\n'.format(
        self.near_mbar,
        self.near_mbar_stored,
        self.near_mbar_per_s,
        self.near_mbar_per_s_stored)
        string += 'far_mbar={0:d},far_mbar_stored={1:d},far_mbar_per_s={2:d},far_mbar_per_s_stored={3:d}\r\n'.format(
        self.far_mbar,
        self.far_mbar_stored,
        self.far_mbar_per_s,
        self.far_mbar_per_s_stored)
        string += 'ascent_mbar_per_s={0:d},ascent_mbar_per_s_stored={1:d}\r\n'.format(
        self.ascent_mbar_per_s,
        self.ascent_mbar_per_s_stored)
        string += 'dead_delay_s={0:d},dead_delay_s_stored={1:d}\r\n'.format(
        self.dead_delay_s,
        self.dead_delay_s_stored)
        string += 'oil_coeff_num={0:d},oil_coeff_num_stored={1:d},oil_coeff_den={2:d},oil_coeff_den_stored={3:d}\r\n'.format(
        self.oil_coeff_num,
        self.oil_coeff_num_stored,
        self.oil_coeff_den,
        self.oil_coeff_den_stored)
        string += 'stab_counts={0:d},stab_counts_stored={1:d}\r\n'.format(
        self.stab_counts,
        self.stab_counts_stored)
        string += 'min_surface_delay_s={0:d},min_surface_delay_s_stored={1:d},max_surface_delay_s={2:d},max_surface_delay_s_stored={3:d}\r\n'.format(
        self.min_surface_delay_s,
        self.min_surface_delay_s_stored,
        self.max_surface_delay_s,
        self.max_surface_delay_s_stored)
        string += 'minimum_mission_time_mn={0:d},minimum_mission_time_mn_stored={1:d}\r\n'.format(
        self.minimum_mission_time_mn,
        self.minimum_mission_time_mn_stored)
        string += 'dv_landing_ml={0:d},dv_landing_ml_stored={1:d}\r\n'.format(
        self.dv_landing_ml,
        self.dv_landing_ml_stored)
        string += 'p2t_addr={0:d},p2t_historic_depth={1:d},p2t_period_ms={2:d},p2t_offset_mbar={3:d},p2t_log_mbar={4:d},p2t_log_mdegc={5:d}\r\n'.format(
        self.p2t_addr,
        self.p2t_historic_depth,
        self.p2t_period_ms,
        self.p2t_offset_mbar,
        self.p2t_log_mbar,
        self.p2t_log_mdegc)
        return string
