import dives
import utils
import re
from obspy import UTCDateTime
import numpy as np
import configuration
import sbe41_profile

class ConfigurationParameter:
    name=None
    value=None
    def __init__(self, name=None, value=None, description=None):
        self.name = name
        self.value = value
        self.description = description
    def __NE__(self, other):
        if self.name == other.name and self.value == other.value :
            return False
        else :
            return True

class ConfigurationParameters:
    parametersList = None
    park_pressure_dbar = None
    park_pressure_mbar = None
    ascent_speed_mbar_per_s = None
    descent_to_profile_timeout_h = None
    profile_pressure_dbar = None
    profile_pressure_mbar = None
    surface_mbar = None
    ascent_end_threshold_dbar = None
    sampling_period_s = None
    ascent_speed_min_mbar_per_s = None
    ascent_to_surface_timeout_h = None
    buoyancy_reduction_first_threshold_dbar = None
    buoyancy_reduction_second_threshold_dbar = None
    connection_timeout_sec = None
    ascent_duration_s = None
    down_time_s = None
    down_time_h = None
    cycle_time_max_h = None
    descent_to_park_timeout_h = None
    park_time_h = None
    profile_sampling_method = None
    depth_interval_dbar = None
    profile_bottom_bin_interval_cbar = None
    profile_bottom_slices_tickness_dbar = None
    profile_include_transition_bin = None
    profile_intermediate_bin_interval_cbar = None
    profile_intermediate_slices_tickness_dbar = None
    profile_surface_bin_interval_cbar = None
    profile_surface_slices_tickness_dbar = None
    pressure_threshold_data_reduction_shallow_to_intermediate_dbar = None
    pressure_threshold_data_reduction_intermediate_to_deep_dbar = None
    surface_timeout_h = None
    up_time_h = None

    def __init__(self, diveConfig=None):
        self.parametersList=[]
        self.park_pressure_dbar = None
        if not diveConfig :
            return
        # get ascent speed
        self.ascent_speed_mbar_per_s = np.float64(8.0)
        if diveConfig.ascent_mbar_per_s :
            self.ascent_speed_mbar_per_s = np.float64(diveConfig.ascent_mbar_per_s)
        if diveConfig.sbe41_pilots :
            self.ascent_speed_mbar_per_s = np.float64(diveConfig.sbe41_pilots.speedcontrol)
        # get park pressure
        self.park_pressure_mbar = None
        self.park_pressure_dbar = None
        if diveConfig.stages :
            self.park_pressure_mbar = diveConfig.stages[0].pressure_ref_mbar
        if self.park_pressure_mbar :
            self.park_pressure_dbar = np.float64(self.park_pressure_mbar/100.0)
        # get descent to profile timeout in seconds
        self.descent_to_profile_timeout_h = None
        # get profile pressure
        self.profile_pressure_dbar = None
        self.profile_pressure_mbar = self.park_pressure_mbar
        if diveConfig.stages :
            for stage in diveConfig.stages:
                if stage.pressure_ref_mbar > self.park_pressure_mbar:
                    #Profile depth is not the same than park pressure
                    self.descent_to_profile_timeout_h = np.float64(stage.duration_estimated_s/3600.0)
                    self.profile_pressure_mbar = stage.pressure_ref_mbar
        if self.profile_pressure_mbar :
            self.profile_pressure_dbar = np.float64(self.profile_pressure_mbar/100.0)
        # get surface pressure
        self.surface_mbar = 500
        if diveConfig.surface_mbar :
            self.surface_mbar = diveConfig.surface_mbar
        self.ascent_end_threshold_dbar = np.float64(self.surface_mbar/100.0)
        # get sampling period in second
        self.sampling_period_s = None
        if diveConfig.sbe41_parameters :
            if int(diveConfig.sbe41_parameters.samplerate) == 1 :
                self.sampling_period_s = np.float64(1)
            elif int(diveConfig.sbe41_parameters.samplerate) == 0 :
                self.sampling_period_s = np.float64(2)
        # get speed min to start profile
        self.ascent_speed_min_mbar_per_s = None
        if diveConfig.sbe41_pilots :
            self.ascent_speed_min_mbar_per_s = np.float64(diveConfig.sbe41_pilots.speedstart)
        # get ascent to surface timeout in sec
        self.ascent_to_surface_timeout_h = None
        if diveConfig.stages :
            if diveConfig.stages[-1].stage_type == "surfacing" and diveConfig.stages[-1].scientific_type == "SBE41":
                self.ascent_to_surface_timeout_h = np.float64(diveConfig.stages[-1].duration_estimated_s/3600.0)
        # get buoyancy reduction firdt threshold
        self.buoyancy_reduction_first_threshold_dbar = None
        if diveConfig.far_mbar :
            self.buoyancy_reduction_first_threshold_dbar = np.float64(diveConfig.far_mbar/100.0)
        # get buoyancy reduction second threshold
        self.buoyancy_reduction_second_threshold_dbar = None
        if diveConfig.near_mbar :
            self.buoyancy_reduction_second_threshold_dbar = np.float64(diveConfig.near_mbar/100.0)
        # get connection timeout in seconds
        self.connection_timeout_sec = None
        if diveConfig.max_surface_delay_s :
            self.connection_timeout_sec = np.float64(diveConfig.max_surface_delay_s)
        # get ascent duration in seconds
        self.ascent_duration_s = None
        if self.profile_pressure_mbar and self.ascent_speed_mbar_per_s :
            self.ascent_duration_s = np.float64(self.profile_pressure_mbar) / np.float64(self.ascent_speed_mbar_per_s)
        # get down time in seconds
        self.down_time_s = None
        self.down_time_h = None
        if diveConfig.stages :
            if diveConfig.stages[-1].stage_type == "surfacing" :
                self.down_time_s = diveConfig.stages[-2].expiration_date_s
            else :
                self.down_time_s = diveConfig.stages[-1].expiration_date_s
        if self.down_time_s:
            self.down_time_h = np.float64(self.down_time_s/3600.0)
        # get cycle time max in seconds
        self.cycle_time_max_h = None
        if self.ascent_duration_s and self.down_time_s and self.connection_timeout_sec :
            self.cycle_time_max_h = np.float64((self.down_time_s + self.ascent_duration_s + self.connection_timeout_sec)/3600.0)
        # get descent to park timeout in seconds
        self.descent_to_park_timeout_h = None
        if diveConfig.stages :
            self.descent_to_park_timeout_h = np.float64(diveConfig.stages[0].duration_estimated_s/3600.0)
        # get park time in seconds
        self.park_time_h = None
        if diveConfig.stages :
            if diveConfig.stages[1] and (diveConfig.stages[0].pressure_ref_mbar == diveConfig.stages[1].pressure_ref_mbar) :
                self.park_time_h = np.float64(diveConfig.stages[1].duration_estimated_s/3600.0)
        # get profile sampling methode
        self.profile_sampling_method = None
        if diveConfig.sbe41_pilots :
            self.profile_sampling_method = np.int32(diveConfig.sbe41_pilots.binaverageoutput)
        # Target depth interval between final CTD samples when in the spot sampling mode.
        self.depth_interval_dbar = None
        if self.ascent_speed_mbar_per_s and self.sampling_period_s and self.profile_sampling_method == 0 :
            self.depth_interval_dbar = np.float64((self.ascent_speed_mbar_per_s * self.sampling_period_s)/100.0)
        # Depth intervals for bottom depth (algorithm of data reduction).
        self.profile_bottom_bin_interval_cbar = None
        if diveConfig.sbe41_parameters :
            self.profile_bottom_bin_interval_cbar = np.float64(diveConfig.sbe41_parameters.bottom_bin_interval*10.0)
        # Thickness of the slices for deep depths (algorithm of data reduction) (in dbars).
        self.profile_bottom_slices_tickness_dbar = None
        if diveConfig.sbe41_parameters :
            self.profile_bottom_slices_tickness_dbar = np.float64(diveConfig.sbe41_parameters.bottom_bin_size)
        # Include transition bins between depth zones (shallow/intermediate/bottom) (Yes=1/No=0).
        self.profile_include_transition_bin = None
        if diveConfig.sbe41_parameters :
            self.profile_include_transition_bin = np.int32(diveConfig.sbe41_parameters.includetransitionbin)

        self.profile_intermediate_bin_interval_cbar = None
        if diveConfig.sbe41_parameters :
            self.profile_intermediate_bin_interval_cbar = np.float64(diveConfig.sbe41_parameters.middle_bin_interval*10.0)

        self.profile_intermediate_slices_tickness_dbar = None
        if diveConfig.sbe41_parameters :
            self.profile_intermediate_slices_tickness_dbar = np.float64(diveConfig.sbe41_parameters.middle_bin_size)

        self.profile_surface_bin_interval_cbar = None
        if diveConfig.sbe41_parameters :
            self.profile_surface_bin_interval_cbar = np.float64(diveConfig.sbe41_parameters.top_bin_interval*10.0)

        self.profile_surface_slices_tickness_dbar = None
        if diveConfig.sbe41_parameters :
            self.profile_surface_slices_tickness_dbar = np.float64(diveConfig.sbe41_parameters.top_bin_size)

        self.pressure_threshold_data_reduction_shallow_to_intermediate_dbar = None
        if diveConfig.sbe41_parameters :
            self.pressure_threshold_data_reduction_shallow_to_intermediate_dbar = np.float64(diveConfig.sbe41_parameters.top_bin_max)

        self.pressure_threshold_data_reduction_intermediate_to_deep_dbar = None
        if diveConfig.sbe41_parameters :
            self.pressure_threshold_data_reduction_intermediate_to_deep_dbar = np.float64(diveConfig.sbe41_parameters.middle_bin_max)

        self.surface_timeout_h = None
        if self.connection_timeout_sec :
            self.surface_timeout_h = np.float64(self.connection_timeout_sec/3600.0)

        self.up_time_h = None
        if self.ascent_duration_s and self.connection_timeout_sec :
            self.up_time_h = np.float64((self.ascent_duration_s + self.connection_timeout_sec)/3600.0)

        self.parametersList.append(ConfigurationParameter("CONFIG_AscentEndThreshold_dbar",self.ascent_end_threshold_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_AscentSamplingPeriod_seconds",self.sampling_period_s))
        self.parametersList.append(ConfigurationParameter("CONFIG_AscentSpeed_cm/s",self.ascent_speed_mbar_per_s))
        self.parametersList.append(ConfigurationParameter("CONFIG_AscentSpeedMin_cm/s",self.ascent_speed_min_mbar_per_s))
        self.parametersList.append(ConfigurationParameter("CONFIG_AscentToSurfaceTimeOut_hours",self.ascent_to_surface_timeout_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_BuoyancyReductionFirstThreshold_dbar",self.buoyancy_reduction_first_threshold_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_BuoyancyReductionSecondThreshold_dbar",self.buoyancy_reduction_second_threshold_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ConnectionTimeOut_seconds",self.connection_timeout_sec))
        self.parametersList.append(ConfigurationParameter("CONFIG_Direction_NUMBER",1))
        self.parametersList.append(ConfigurationParameter("CONFIG_CycleTime_hours",self.cycle_time_max_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_DescentToParkTimeOut_hours",self.descent_to_park_timeout_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_DescentToProfTimeOut_hours",self.descent_to_profile_timeout_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_DownTime_hours",self.down_time_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_ParkPressure_dbar",self.park_pressure_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfilePressure_dbar",self.profile_pressure_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ParkTime_hours",self.park_time_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileSamplingMethod_LOGICAL",self.profile_sampling_method))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileDepthInterval_dbar",self.depth_interval_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileBottomBinInterval_cbar",self.profile_bottom_bin_interval_cbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileBottomSlicesThickness_dbar",self.profile_bottom_slices_tickness_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_PressureThresholdDataReductionIntermediateToDeep_dbar",self.pressure_threshold_data_reduction_intermediate_to_deep_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileIncludeTransitionBin_LOGICAL",self.profile_include_transition_bin))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileIntermediateBinInterval_cbar",self.profile_intermediate_bin_interval_cbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileIntermediateSlicesThickness_dbar",self.profile_intermediate_slices_tickness_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_PressureThresholdDataReductionShallowToIntermediate_dbar",self.pressure_threshold_data_reduction_shallow_to_intermediate_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileSurfaceBinInterval_cbar",self.profile_surface_bin_interval_cbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_ProfileSurfaceSlicesThickness_dbar",self.profile_surface_slices_tickness_dbar))
        self.parametersList.append(ConfigurationParameter("CONFIG_SurfaceTimeOut_hours",self.surface_timeout_h))
        self.parametersList.append(ConfigurationParameter("CONFIG_UpTime_hours",self.up_time_h))
    def __str__(self):
        str = ""
        for parameter in self.parametersList :
            str += '{0}={1}\r\n'.format(parameter.name,parameter.value)
        return str
    def __NE__(self, other):
        if self.parametersList == other.parametersList :
            return False
        else :
            return True
class Measurement:
    code=None
    cycle=None
    date=None
    pressure=None
    temperature=None
    salinity=None
    longitude=None
    latitude=None
    description=None
    def __init__(self,cycle,code,date,description,longitude=None,latitude=None,pressure=None,temperature=None,salinity=None):
        self.cycle = cycle
        self.code = code
        # UTCDateTime
        self.date = date
        self.description = description
        if pressure :
            self.pressure = pressure
        else :
            self.pressure = np.float64(99999.0)
        if temperature :
            self.temperature = temperature
        else :
            self.temperature = np.float64(99999.0)
        if salinity :
            self.salinity = salinity
        else :
            self.salinity = np.float64(99999.0)
        if longitude :
            self.longitude = longitude
        else :
            self.longitude = np.float64(99999.0)
        if latitude :
            self.latitude = latitude
        else :
            self.latitude = np.float64(99999.0)

class Measurements:
    list=None
    log_name=None
    clockOffset=None
    def __init__(self, dive):
        self.list = list()
        self.stages = list()
        self.log_name = dive.log_name
        if not dive.is_complete_dive :
            return
        if dive.is_init :
            if dive.gps_list_is_complete :
                for gps in dive.gps_list:
                    # Each GPS position
                    self.list.append(Measurement(0,703,gps.date,"GPS positions in surface",gps.longitude,gps.latitude))
            return
        currentPressure_mbar = 0
        currentPressure_time = 0
        cycle_nb = int(dive.cycle_nb)
        # get last clock offset
        derive_s = utils.find_timestamped_values(":\[GPSFIX.+\].*(-?\d+)s diff.*", dive.log_content)
        self.clockOffset = np.float64(int(derive_s[-1][0]) / 86400.0)
        ############## First surface step (cycle_nb -1) ##################################################
        connections = utils.find_timestamped_values(":\[SURF.+\].*connected in \d+s, signal quality \d+", dive.log_content)
        disconnections = utils.find_timestamped_values(":\[SURF.+\].*disconnected after \d+s", dive.log_content)
        # All positions of (cycle_nb - 1)
        if dive.gps_list_is_complete :
            for gps in dive.gps_list[:-1]:
                # Each GPS position
                self.list.append(Measurement(cycle_nb-1,703,gps.date,"GPS positions in surface",gps.longitude,gps.latitude))
        # First connection
        self.list.append(Measurement(cycle_nb-1,700,connections[0][1],"Time when first connection is done."))
        # First disconnection
        self.list.append(Measurement(cycle_nb-1,702,disconnections[0][1],"Time when first disconnection is occured"))
        # Last disconnection
        self.list.append(Measurement(cycle_nb-1,704,connections[-1][1],"Time when last connection is done"))
        # End of transmissions
        self.list.append(Measurement(cycle_nb-1,800,disconnections[-1][1],"Time when last disconnection is done"))
        ########################################## Mission (cycle_nb) ######################################
        mc = 100
        lines = utils.split_log_lines(dive.log_content)
        for line in lines :
            pressure = utils.find_timestamped_value("\[PRESS ,0038\]P *\+(\d+)mbar,T *\+\d+mdegC", line)
            if len(pressure) > 0 :
                currentPressure_mbar = int(pressure[0])
                currentPressure_time = pressure[1]

            # detect bypass line
            bypass = utils.find_timestamped_value(":\[BYPASS.+\].*opening.*[0-9]+ms", line)
            if len(bypass) > 0 :
                self.list.append(Measurement(cycle_nb,mc-11,bypass[1],"Active bypass"))
            # detect valve line
            valve = utils.find_timestamped_value(":\[VALVE.+\].*opening.*[0-9]+ms", line)
            if len(valve) > 0 :
                self.list.append(Measurement(cycle_nb,mc-11,valve[1],"Active valve"))
            # detect pump line
            pump = utils.find_timestamped_value(":\[PUMP.+\].*during.*[0-9]+ms", line)
            if len(pump) > 0 :
                self.list.append(Measurement(cycle_nb,mc-11,pump[1],"Active pump"))

            if mc == 100 :
                # detect Descent to park start Time (DST)
                match = utils.find_timestamped_value(":\[DIVING.+\][0-9]+mbar reached .*", line)
                if len(match) > 0 :
                    self.list.append(Measurement(cycle_nb,100,match[1],"Descent to park start Time (5 meters reached)"))
                    mc = 200
            elif mc == 200 :
                # detect Descent end time (DET)
                tree_per_cent_threshold = dive.configuration.stages[0].pressure_ref_mbar - (dive.configuration.stages[0].pressure_ref_mbar/100*3)
                if (len(pressure) > 0)  and (currentPressure_mbar >= tree_per_cent_threshold) :
                    self.list.append(Measurement(cycle_nb,200,currentPressure_time,"Descent end time (park zone detected)"))
                    mc = 300
            elif mc == 300 :
                # detect park end time (PET)
                match = utils.find_timestamped_value(":\[MAIN.+\]stage\[1\] complete.*", line)
                if len(match) > 0 :
                    self.list.append(Measurement(cycle_nb,300,match[1],"Park end time (second step finished)"))
                    mc = 400
            elif mc == 400 :
                # detect deep descent end time (DDET)
                tree_per_cent_threshold = dive.configuration.stages[-2].pressure_ref_mbar - (dive.configuration.stages[-2].pressure_ref_mbar/100*3)
                if (len(pressure) > 0)  and (currentPressure_mbar >= tree_per_cent_threshold) :
                    self.list.append(Measurement(cycle_nb,400,currentPressure_time,"Deep descent end time (3% of profile detected))"))
                    mc = 500
                match_surfacing = utils.find_timestamped_value(":\[STAGE.+\]Stage \[2\] surfacing.*", line)
                match_deepest = utils.find_timestamped_value(":\[MAIN.+\]stage\[2\] complete.*", line)
                if len(match_surfacing) > 0 :
                    self.list.append(Measurement(cycle_nb,400,match_surfacing[1],"Deep descent end time (3rd step begin when surfacing)"))
                    mc = 500
                if len(match_deepest) > 0 :
                    self.list.append(Measurement(cycle_nb,400,match_deepest[1],"Deep descent end time (3rd step is finished)"))
                    mc = 500
            elif mc == 500 :
                # detect ascent start time (AST)
                match = utils.find_timestamped_value(":\[SBE41.+\]Speed start detected.*", line)
                if len(match) > 0 :
                    self.list.append(Measurement(cycle_nb,500,match[1],"Ascent start time (profile started)"))
                    mc = 600
            elif mc == 600 :
                # detect end of ascent (AET)
                match = utils.find_timestamped_value(":\[STAGE.+\]The float reached the surface.*", line)
                if len(match) > 0 :
                    self.list.append(Measurement(cycle_nb,600,match[1],"Ascent end time (profiler reach the surface)"))
                    mc = 700
                    break;

        self.list.append(Measurement(cycle_nb,703,dive.gps_list[-1].date,"First GPS position in surface",dive.gps_list[-1].longitude,dive.gps_list[-1].latitude))
    def print_all(self) :
        index = 0
        print('LOG:{0},clockOffset:{1}'.format(self.log_name,self.clockOffset))
        for element in self.list :
            print('Measurement[{0}]:Code{1},Cycle{2},{3},{4},{5},{6}'.format(index,element.code,element.cycle,element.date,element.description,element.latitude,element.longitude))
            index = index +1


class Cycle :
    cycleNb = None
    descentStartTime = None
    firstStabilizationTime = None
    descentEndTime = None
    parkStartTime = None
    parkEndTime = None
    deepDescentEndTime = None
    deepParkStartTime = None
    deepAscentStartTime = None
    ascentStartTime = None
    ascentEndTime = None
    transmissionStartTime = None
    firstMessageTime = None
    firstLocationTime = None
    lastLocationTime = None
    lastMessageTime = None
    transmissionEndTime = None
    clockOffset = None
    park_pressure_dbar = None
    park_pressure_status = None
    stages = None
    stages_nb = None
    configMissionNumber = None
    locations = None
    measures = None
    parameters = None
    launchParameters = None
    logNames = None
    sbe41Profiles = None
    sbe41ProfileFileName = None
    sbe41ProfileEnvironnement = None

    def __init__(self, cycleNb, dst=None, fst=None, det=None, pst=None, pet=None, ddet=None, dpst=None, dast=None, ast=None, aet=None, tst=None, fmt=None, flt=None, llt=None, lmt=None, tet=None):
        self.cycleNb = cycleNb
        self.descentStartTime = dst
        self.firstStabilizationTime = fst
        self.descentEndTime = det
        self.parkStartTime = pst
        self.parkEndTime = pet
        self.deepDescentEndTime = ddet
        self.deepParkStartTime = dpst
        self.deepAscentStartTime = dast
        self.ascentStartTime = ast
        self.ascentEndTime = aet
        self.firstMessageTime = fmt
        self.firstLocationTime = flt
        self.lastLocationTime = llt
        self.lastMessageTime = lmt
        self.transmissionEndTime = tet
        self.clockOffset = np.float64(99999.0)
        self.park_pressure_dbar = np.float64(99999.0)
        self.park_pressure_status = '7'
        self.configMissionNumber = 0;
        self.stages_nb = 0;
        self.stages = list()
        self.locations = list()
        self.measures = list()
        self.logNames = list()
        self.parameters = ConfigurationParameters()
        self.launchParameters = ConfigurationParameters()
        self.configurationParameters = ConfigurationParameters()
        self.sbe41Profiles = sbe41_profile.Profiles()
        self.sbe41ProfileFileName = None
        self.sbe41ProfileEnvironnement = None

class Cycles :
    list = None
    parametersNb = None
    launchParametersNb = None
    configurationParametersNb = None
    missionsConfigurationParameters = None
    def __init__(self,dives) :
        self.list = list()
        cycleNb = 0
        cycle = Cycle(0)
        for dive in dives.get_dives() :
            measures = Measurements(dive)
            if dive.log_name not in cycle.logNames :
                cycle.logNames.append(dive.log_name)
            for measure in measures.list :
                if measure.cycle > cycleNb :
                    self.list.append(cycle)
                    cycleNb = cycleNb + 1
                    cycle = Cycle(cycleNb)
                    if dive.log_name not in cycle.logNames :
                        cycle.logNames.append(dive.log_name)

                cycle.measures.append(measure)
                if measure.code == 100 :
                    cycle.descentStartTime = measure.date
                elif measure.code == 200 :
                    cycle.descentEndTime = measure.date
                elif measure.code == 300 :
                    cycle.parkEndTime = measure.date
                elif measure.code == 400 :
                    cycle.deepDescentEndTime = measure.date
                elif measure.code == 500 :
                    cycle.ascentStartTime = measure.date
                elif measure.code == 600 :
                    cycle.ascentEndTime = measure.date
                elif measure.code == 700 :
                    cycle.transmissionStartTime = measure.date
                elif measure.code == 702 :
                    cycle.firstMessageTime = measure.date
                elif measure.code == 703 :
                    cycle.locations.append(measure)
                    if len(cycle.locations) == 1 :
                        cycle.firstLocationTime = cycle.locations[0].date
                    elif len(cycle.locations) >= 2 :
                        cycle.lastLocationTime = cycle.locations[-1].date
                elif measure.code == 704 :
                    cycle.lastMessageTime = measure.date
                elif measure.code == 800 :
                    cycle.transmissionEndTime = measure.date

            cycle.sbe41Profiles = dive.profiles
            cycle.sbe41ProfileFileName = dive.s41_name
            cycle.sbe41ProfileEnvironnement = dive.s41_environment
            cycle.station_name =  dive.station_name
            cycle.station_number = dive.station_number
            cycle.soft_version = dive.soft_version
            if dive.configuration:
                cycle.parameters = ConfigurationParameters(dive.configuration)
                self.parametersNb = len(cycle.parameters.parametersList)
            if measures.clockOffset:
                cycle.clockOffset = measures.clockOffset
            if dive.configuration.stages :
                cycle.stages = dive.configuration.stages
            if dive.configuration.stages_nb :
                cycle.stages_nb = dive.configuration.stages_nb
        self.list.append(cycle)
        cycleNb = cycleNb + 1

        self.missionsConfigurationParameters = list()
        self.missionsConfigurationParameters.append(self.list[0].parameters)
        # All parameters are launched by default
        indexLaunchParameters = [1] * self.parametersNb
        for cycle in self.list :
            #get park pressure on configurationParameters
            cycle.park_pressure_status = '7'
            cycle.park_pressure_dbar = cycle.parameters.park_pressure_dbar

            # check if parameter never change during all missions
            indexParameter = 0
            while indexParameter < self.parametersNb:
                for mission_config in self.missionsConfigurationParameters :
                    if cycle.parameters.parametersList[indexParameter].value != mission_config.parametersList[indexParameter].value :
                        indexLaunchParameters[indexParameter] = 0
                indexParameter = indexParameter + 1

            #
            newMission = True
            configMissionNumber = 0
            for mission_config in self.missionsConfigurationParameters :
                indexParameter = 0
                sameNumber = 0
                while indexParameter < self.parametersNb:
                    if cycle.parameters.parametersList[indexParameter].value == mission_config.parametersList[indexParameter].value :
                        sameNumber = sameNumber + 1
                    indexParameter = indexParameter + 1
                if sameNumber >= self.parametersNb :
                    newMission = False
                    break
                configMissionNumber = configMissionNumber + 1
            if newMission :
                self.missionsConfigurationParameters.append(cycle.parameters)
            cycle.configMissionNumber = configMissionNumber

        # split into 2 list with parameters that never change and mission parameters
        for cycle in self.list :
            indexParameter = 0
            cycle.launchParameters.parametersList = list()
            cycle.configurationParameters.parametersList = list()
            while indexParameter < self.parametersNb:
                if indexLaunchParameters[indexParameter] == 1 :
                    cycle.launchParameters.parametersList.append(cycle.parameters.parametersList[indexParameter])
                else :
                    cycle.configurationParameters.parametersList.append(cycle.parameters.parametersList[indexParameter])
                indexParameter = indexParameter + 1
            self.launchParametersNb = len(cycle.launchParameters.parametersList)
            self.configurationParametersNb = len(cycle.configurationParameters.parametersList)



    def __str__(self) :
        str = ""
        for element in self.list :
            str += '\r\n\r\nCycle[{0:d}]:{1}\r\n'.format(element.cycleNb,element.logNames)
            str += 'descentStartTime={0}\r\n'.format(element.descentStartTime)
            str += 'firstStabilizationTime={0}\r\n'.format(element.firstStabilizationTime)
            str += 'descentEndTime={0}\r\n'.format(element.descentEndTime)
            str += 'parkStartTime={0}\r\n'.format(element.parkStartTime)
            str += 'parkEndTime={0}\r\n'.format(element.parkEndTime)
            str += 'deepDescentEndTime={0}\r\n'.format(element.deepDescentEndTime)
            str += 'deepParkStartTime={0}\r\n'.format(element.deepParkStartTime)
            str += 'deepAscentStartTime={0}\r\n'.format(element.deepAscentStartTime)
            str += 'ascentStartTime={0}\r\n'.format(element.ascentStartTime)
            str += 'ascentEndTime={0}\r\n'.format(element.ascentEndTime)
            str += 'firstMessageTime={0}\r\n'.format(element.firstMessageTime)
            str += 'firstLocationTime={0}\r\n'.format(element.firstLocationTime)
            str += 'lastLocationTime={0}\r\n'.format(element.lastLocationTime)
            str += 'lastMessageTime={0}\r\n'.format(element.lastMessageTime)
            str += 'transmissionEndTime={0}\r\n'.format(element.transmissionEndTime)
            str += 'REPRESENTATIVE_PARK_PRESSURE_STATUS={0}\r\n'.format(element.park_pressure_status)
            str += 'REPRESENTATIVE_PARK_PRESSURE={0}\r\n'.format(element.park_pressure_dbar)
            str += 'CONFIG_MISSION_NUMBER={0}\r\n'.format(element.configMissionNumber)
            str += '\r\nCONFIGURATIONS PARAMETERS : \r\n{0}'.format(element.configurationParameters)
            str += '\r\nLAUNCH CONFIGURATION PARAMETERS : \r\n{0}'.format(element.launchParameters)
        return str
    def get_N_CYCLE(self) :
        return len(self.list)
    def get_N_MEASUREMENTS(self) :
        n_measurements = 0
        for cycle in self.list :
            n_measurements += len(cycle.measures)
        return n_measurements
    def get_station_nb(self) :
        for cycle in self.list :
            if cycle.station_number :
                return cycle.station_number
    def get_software_versions(self) :
        soft_versions = []
        for cycle in self.list :
            if cycle.soft_version :
                if cycle.soft_version not in soft_versions :
                    soft_versions.append(cycle.soft_version)
        return soft_versions
