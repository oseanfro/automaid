import os
import shutil
import sys
import decrypt
import glob
import dives
import events
import sbe41_profile
import re
import utils
import netCDF.init_values as init
from obspy import UTCDateTime
from netCDF4 import Dataset
from netCDF4 import stringtochar
from datetime import datetime,timezone
import numpy as np
import mermaid_to_nc_cfg as cfg

def get_data_from_nc_file(mfloat_nc_path,dataDict) :
    rd_cdf = Dataset(mfloat_nc_path, "r", format="NETCDF3_CLASSIC")
    for key in dataDict.keys() :
        variables = rd_cdf.get_variables_by_attribute(self, name=dataDict.keys())
        if len(variables) > 0:
            dataDict[key] = variables[0]
    return dataDict

def create_dim_tuple(dimensions,value):
    result = value
    for dim in dimensions:
        result = tuple(result for _ in range(dim))
    return result

def putStringArray(var,stringArray,varlen):
    nparray = np.array(stringArray,dtype=np.dtype(('S', varlen)))
    var[:] = stringtochar(nparray)
    #var._Encoding = 'ascii' # this enables automatic conversion

def putString(var,string,varlen):
    putStringArray(var,[string],varlen)

def putNString(var,string,nb,varlen):
    putStringArray(var,[string]*nb,varlen)

def create_nc_multi_prof_c_file_3_1(FloatWmoID,mfloat_nc_path,mCycles,ms41s):
        multiProfCFilePath = mfloat_nc_path + FloatWmoID + "_prof.nc"
        print(multiProfCFilePath)

        #information to retrieve from a possible existing multi-profile file
        if os.path.exists(multiProfCFilePath):
            os.remove(multiProfCFilePath)

        file_cdf = Dataset(multiProfCFilePath, "w", format="NETCDF3_CLASSIC")

        ##################################################################################################
        ###                                                                                             ##
        ###                                     Create Dimensions                                       ##
        ###                                                                                             ##
        ##################################################################################################

        dateTimeDim = file_cdf.createDimension('DATE_TIME', 14);
        string256Dim = file_cdf.createDimension('STRING256', 256);
        string64Dim = file_cdf.createDimension('STRING64', 64);
        string32Dim = file_cdf.createDimension('STRING32', 32);
        string16Dim = file_cdf.createDimension('STRING16', 16);
        string8Dim = file_cdf.createDimension('STRING8', 8);
        string4Dim = file_cdf.createDimension('STRING4', 4);
        string2Dim = file_cdf.createDimension('STRING2', 2);
        nProfDim = file_cdf.createDimension('N_PROF', ms41s.get_N_PROF());
        nParamDim = file_cdf.createDimension('N_PARAM', ms41s.get_N_PARAMS());
        nLevelsDim = file_cdf.createDimension('N_LEVELS', ms41s.get_N_LEVELS());

        nCalibDim = file_cdf.createDimension('N_CALIB',1);
        nHistoryDim = file_cdf.createDimension('N_HISTORY',1);


        nProfDimSize = len(nProfDim)
        nParamDimSize = len(nParamDim)
        nLevelsDimSize = len(nLevelsDim)
        string2DimSize = len(string2Dim)
        string4DimSize = len(string4Dim)
        string8DimSize = len(string8Dim)
        string16DimSize = len(string16Dim)
        string32DimSize = len(string32Dim)
        string64DimSize = len(string64Dim)
        string256DimSize = len(string256Dim)
        dateTimeDimSize = len(dateTimeDim)
        nHistoryDimSize = len(nHistoryDim)
        nCalibDimSize = len(nCalibDim)

        print(nProfDimSize)
        ##################################################################################################
        ###                                                                                             ##
        ###                                     Create Variables                                        ##
        ###                                                                                             ##
        ##################################################################################################

        file_cdf.setncattr('title','Argo float vertical profile')
        file_cdf.setncattr('institution','CORIOLIS')
        file_cdf.setncattr('source','Argo float')

        currentDate = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S");
        globalHistoryText = currentDate + ' creation; ';
        globalHistoryText += currentDate + ' last update (osean float converting raw data)'

        file_cdf.setncattr('history', globalHistoryText)
        file_cdf.setncattr('references', 'http://www.argodatamgt.org/Documentation')
        file_cdf.setncattr('user_manual_version', '3.1')
        file_cdf.setncattr('Conventions', 'Argo-3.1 CF-1.6')
        file_cdf.setncattr('featureType', 'trajectoryProfile')
        file_cdf.setncattr('decoder_version', "autoNetCdf_v{0}".format(init.SOFTWARE_VERSION))

        dataTypeVar = file_cdf.createVariable('DATA_TYPE','S1',('STRING16',),fill_value=' ')
        dataTypeVar.setncattr('long_name', 'Data type')
        dataTypeVar.setncattr('conventions', 'Argo reference table 1')

        formatVersionVar = file_cdf.createVariable('FORMAT_VERSION','S1',('STRING4',),fill_value=' ')
        formatVersionVar.setncattr('long_name', 'File format version')

        handbookVersionVar = file_cdf.createVariable('HANDBOOK_VERSION','S1',('STRING64',),fill_value=' ')
        handbookVersionVar.setncattr('long_name', 'Data handbook version')

        referenceDateTimeVar = file_cdf.createVariable('REFERENCE_DATE_TIME','S1',('DATE_TIME',),fill_value=' ')
        referenceDateTimeVar.setncattr('long_name', 'Date of reference for Julian days')
        referenceDateTimeVar.setncattr('conventions', 'YYYYMMDDHHMISS')

        dateCreationVar = file_cdf.createVariable('DATE_CREATION','S1',('DATE_TIME',),fill_value=' ')
        dateCreationVar.setncattr('long_name', 'Date of file creation')
        dateCreationVar.setncattr('conventions', 'YYYYMMDDHHMISS')

        dateUpdateVar = file_cdf.createVariable('DATE_UPDATE','S1',('DATE_TIME',),fill_value=' ')
        dateUpdateVar.setncattr('long_name', 'Date of update of this file');
        dateUpdateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

        # create profile variables
        platformNumberVar = file_cdf.createVariable('PLATFORM_NUMBER','S1',('N_PROF','STRING8'),fill_value=' ')
        platformNumberVar.setncattr('long_name', 'Float unique identifier');
        platformNumberVar.setncattr('conventions', 'WMO float identifier : A9IIIII');

        projectNameVar = file_cdf.createVariable('PROJECT_NAME','S1',('N_PROF','STRING64'),fill_value=' ')
        projectNameVar.setncattr('long_name', 'Name of the project');

        piNameVar = file_cdf.createVariable('PI_NAME','S1',('N_PROF','STRING64'),fill_value=' ')
        piNameVar.setncattr('long_name', 'Name of the principal investigator');

        stationParametersVar = file_cdf.createVariable('STATION_PARAMETERS','S1',('N_PROF','N_PARAM','STRING64'),fill_value=' ')
        stationParametersVar.setncattr('long_name', 'List of available parameters for the station');
        stationParametersVar.setncattr('conventions', 'Argo reference table 3');

        cycleNumberVar = file_cdf.createVariable('CYCLE_NUMBER','i4',('N_PROF',),fill_value=np.int32(99999))
        cycleNumberVar.setncattr('long_name', 'Float cycle number');
        cycleNumberVar.setncattr('conventions', '0...N, 0 : launch cycle (if exists), 1 : first complete cycle');

        directionVar = file_cdf.createVariable('DIRECTION','S1',('N_PROF',),fill_value=' ')
        directionVar.setncattr('long_name', 'Direction of the station profiles');
        directionVar.setncattr('conventions', 'A: ascending profiles, D: descending profiles');

        dataCentreVar = file_cdf.createVariable('DATA_CENTRE','S1',('N_PROF','STRING2'),fill_value=' ')
        dataCentreVar.setncattr('long_name', 'Data centre in charge of float data processing');
        dataCentreVar.setncattr('conventions', 'Argo reference table 4');

        dcReferenceVar = file_cdf.createVariable('DC_REFERENCE','S1',('N_PROF','STRING32'),fill_value=' ')
        dcReferenceVar.setncattr('long_name', 'Station unique identifier in data centre');
        dcReferenceVar.setncattr('conventions', 'Data centre convention');

        dataStateIndicatorVar = file_cdf.createVariable('DATA_STATE_INDICATOR','S1',('N_PROF','STRING4'),fill_value=' ')
        dataStateIndicatorVar.setncattr('long_name', 'Degree of processing the data have passed through');
        dataStateIndicatorVar.setncattr('conventions', 'Argo reference table 6');

        dataModeVar = file_cdf.createVariable('DATA_MODE','S1',('N_PROF',),fill_value=' ')
        dataModeVar.setncattr('long_name', 'Delayed mode or real time data');
        dataModeVar.setncattr('conventions', 'R : real time; D : delayed mode; A : real time with adjustment');

        platformTypeVar = file_cdf.createVariable('PLATFORM_TYPE','S1',('N_PROF','STRING32'),fill_value=' ')
        platformTypeVar.setncattr('long_name', 'Type of float');
        platformTypeVar.setncattr('conventions', 'Argo reference table 23');

        floatSerialNoVar = file_cdf.createVariable('FLOAT_SERIAL_NO','S1',('N_PROF','STRING32'),fill_value=' ')
        floatSerialNoVar.setncattr('long_name', 'Serial number of the float');

        firmwareVersionVar = file_cdf.createVariable('FIRMWARE_VERSION','S1',('N_PROF','STRING64'),fill_value=' ')
        firmwareVersionVar.setncattr('long_name', 'Instrument firmware version');

        wmoInstTypeVar = file_cdf.createVariable('WMO_INST_TYPE','S1',('N_PROF','STRING4'),fill_value=' ')
        wmoInstTypeVar.setncattr('long_name', 'Coded instrument type');
        wmoInstTypeVar.setncattr('conventions', 'Argo reference table 8');

        juldVar = file_cdf.createVariable('JULD','f8',('N_PROF',),fill_value=np.float64(99999.0))
        juldVar.setncattr('long_name', 'Julian day (UTC) of the station relative to REFERENCE_DATE_TIME');
        juldVar.setncattr('standard_name', 'time');
        juldVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
        juldVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
        juldVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution
        juldVar.setncattr('axis','T')
        if 0 :
            juldVar.setncattr('comment_on_resolution','resolution is 1s but when...')

        juldQcVar = file_cdf.createVariable('JULD_QC','S1',('N_PROF',),fill_value=' ')
        juldQcVar.setncattr('long_name', 'Quality on date and time');
        juldQcVar.setncattr('conventions', 'Argo reference table 2');

        juldLocationVar = file_cdf.createVariable('JULD_LOCATION','f8',('N_PROF',),fill_value=np.float64(99999.0))
        juldLocationVar.setncattr('long_name', 'Julian day (UTC) of the location relative to REFERENCE_DATE_TIME');
        juldLocationVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
        juldLocationVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
        juldLocationVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

        latitudeVar = file_cdf.createVariable('LATITUDE','f8',('N_PROF',),fill_value=np.float64(99999.0))
        latitudeVar.setncattr('long_name', 'Latitude of the station, best estimate');
        latitudeVar.setncattr('standard_name', 'latitude');
        latitudeVar.setncattr('units', 'degree_north');
        latitudeVar.setncattr('valid_min', np.float64(-90));
        latitudeVar.setncattr('valid_max', np.float64(90));
        latitudeVar.setncattr('axis', 'Y');

        longitudeVar = file_cdf.createVariable('LONGITUDE','f8',('N_PROF',),fill_value=np.float64(99999.0))
        longitudeVar.setncattr('long_name', 'Longitude of the station, best estimate');
        longitudeVar.setncattr('standard_name', 'longitude');
        longitudeVar.setncattr('units', 'degree_east');
        longitudeVar.setncattr('valid_min', np.float64(-180));
        longitudeVar.setncattr('valid_max', np.float64(180));
        longitudeVar.setncattr('axis', 'X');

        positionQcVar = file_cdf.createVariable('POSITION_QC','S1',('N_PROF',),fill_value=' ')
        positionQcVar.setncattr('long_name', 'Quality on position (latitude and longitude)');
        positionQcVar.setncattr('conventions', 'Argo reference table 2');

        positionSystemVar = file_cdf.createVariable('POSITIONING_SYSTEM','S1',('N_PROF','STRING8'),fill_value=' ')
        positionSystemVar.setncattr('long_name', 'Positioning system');

        profileGlobalParamQcVars = {}
        for param in ms41s.get_PARAMS() :
            ncParamName = "PROFILE_{0}_QC".format(param["PARAM_NAME"])
            profileGlobalParamQcVars[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_PROF',),fill_value=' ')
            profileGlobalParamQcVars[param["PARAM_NAME"]].setncattr('long_name',"Global quality flag of {0} profile".format(param["PARAM_NAME"]))
            profileGlobalParamQcVars[param["PARAM_NAME"]].setncattr('conventions','Argo reference table 2a')

        verticalSamplingSchemeVar = file_cdf.createVariable('VERTICAL_SAMPLING_SCHEME','S1',('N_PROF','STRING256'),fill_value=' ')
        verticalSamplingSchemeVar.setncattr('long_name', 'Vertical sampling scheme');
        verticalSamplingSchemeVar.setncattr('conventions', 'Argo reference table 16');

        configMissionNumberVar = file_cdf.createVariable('CONFIG_MISSION_NUMBER','i4',('N_PROF',),fill_value=np.int32(99999))
        configMissionNumberVar.setncattr('long_name', 'Unique number denoting the missions performed by the float');
        configMissionNumberVar.setncattr('conventions', '1...N, 1 : first complete mission');

        profParamVar = {}
        profParamQcVar = {}
        profParamAdjVar = {}
        profParamAdjQcVar = {}
        profParamAdjErrVar = {}
        for param in ms41s.get_PARAMS() :
            profParamVar[param["PARAM_NAME"]] = file_cdf.createVariable(param["PARAM_NAME"],param["NC_TYPE"],('N_PROF','N_LEVELS'),fill_value=param["FILL_VALUE"])
            profParamVar[param["PARAM_NAME"]].setncattr('long_name', param["LONG_NAME"]);
            profParamVar[param["PARAM_NAME"]].setncattr('standard_name', param["STANDARD_NAME"]);
            profParamVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
            profParamVar[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
            profParamVar[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
            profParamVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
            profParamVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
            profParamVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);
            profParamVar[param["PARAM_NAME"]].setncattr('axis', param["AXIS"]);

            ncParamName = "{0}_QC".format(param["PARAM_NAME"])
            profParamQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_PROF','N_LEVELS'),fill_value=' ')
            profParamQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
            profParamQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

            ncParamName = "{0}_ADJUSTED".format(param["PARAM_NAME"])
            profParamAdjVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_PROF','N_LEVELS'),fill_value=param["FILL_VALUE"])
            profParamAdjVar[param["PARAM_NAME"]].setncattr('long_name', param["LONG_NAME"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('standard_name', param["STANDARD_NAME"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);
            profParamAdjVar[param["PARAM_NAME"]].setncattr('axis', param["AXIS"]);

            ncParamName = "{0}_ADJUSTED_QC".format(param["PARAM_NAME"])
            profParamAdjQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_PROF','N_LEVELS'),fill_value=' ')
            profParamAdjQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
            profParamAdjQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

            ncParamName = "{0}_ADJUSTED_ERROR".format(param["PARAM_NAME"])
            profParamAdjErrVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_PROF','N_LEVELS'),fill_value=param["FILL_VALUE"])
            profParamAdjErrVar[param["PARAM_NAME"]].setncattr('long_name', "Contains the error on the adjusted values as determined by the delayed mode QC process");
            profParamAdjErrVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
            profParamAdjErrVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
            profParamAdjErrVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
            profParamAdjErrVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);

        parameterVar = file_cdf.createVariable('PARAMETER','S1',('N_PROF','N_CALIB','N_PARAM','STRING16'),fill_value=' ')
        parameterVar.setncattr('long_name','List of parameters with calibration information')
        parameterVar.setncattr('conventions','Argo reference table 3')

        scientificCalibEquationVar = file_cdf.createVariable('SCIENTIFIC_CALIB_EQUATION','S1',('N_PROF','N_CALIB','N_PARAM','STRING256'),fill_value=' ')
        scientificCalibEquationVar.setncattr('long_name','Calibration equation for this parameter')

        scientificCalibCoefficientVar = file_cdf.createVariable('SCIENTIFIC_CALIB_COEFFICIENT','S1',('N_PROF','N_CALIB','N_PARAM','STRING256'),fill_value=' ')
        scientificCalibCoefficientVar.setncattr('long_name','Calibration coefficients for this parameter')

        scientificCalibCommentVar = file_cdf.createVariable('SCIENTIFIC_CALIB_COMMENT','S1',('N_PROF','N_CALIB','N_PARAM','STRING256'),fill_value=' ')
        scientificCalibCommentVar.setncattr('long_name','Comment applying to this parameter calibration')

        scientificCalibDateVar = file_cdf.createVariable('SCIENTIFIC_CALIB_DATE','S1',('N_PROF','N_CALIB','N_PARAM','DATE_TIME'),fill_value=' ')
        scientificCalibDateVar.setncattr('long_name','Date of calibration')
        scientificCalibDateVar.setncattr('conventions','YYYYMMDDHHMISS')

        historyInstitutionVar = file_cdf.createVariable('HISTORY_INSTITUTION','S1',('N_HISTORY','N_PROF','STRING4'),fill_value=' ')
        historyInstitutionVar.setncattr('long_name','Institution which performed action')
        historyInstitutionVar.setncattr('conventions','Argo reference table 4')

        historyStepVar = file_cdf.createVariable('HISTORY_STEP','S1',('N_HISTORY','N_PROF','STRING4'),fill_value=' ')
        historyStepVar.setncattr('long_name','Step in data processing')
        historyStepVar.setncattr('conventions','Argo reference table 12')

        historySoftwareVar = file_cdf.createVariable('HISTORY_SOFTWARE','S1',('N_HISTORY','N_PROF','STRING4'),fill_value=' ')
        historySoftwareVar.setncattr('long_name','Name of software which performed action')
        historySoftwareVar.setncattr('conventions','Institution dependent')

        historySoftwareReleaseVar = file_cdf.createVariable('HISTORY_SOFTWARE_RELEASE','S1',('N_HISTORY','N_PROF','STRING4'),fill_value=' ')
        historySoftwareReleaseVar.setncattr('long_name','Version/release of software which performed action')
        historySoftwareReleaseVar.setncattr('conventions','Institution dependent')

        historyReferenceVar = file_cdf.createVariable('HISTORY_REFERENCE','S1',('N_HISTORY','N_PROF','STRING64'),fill_value=' ')
        historyReferenceVar.setncattr('long_name','Reference of database')
        historyReferenceVar.setncattr('conventions','Institution dependent')

        historyDateVar = file_cdf.createVariable('HISTORY_DATE','S1',('N_HISTORY','N_PROF','DATE_TIME'),fill_value=' ')
        historyDateVar.setncattr('long_name','Date the history record was created')
        historyDateVar.setncattr('conventions','YYYYMMDDHHMISS')

        historyActionVar = file_cdf.createVariable('HISTORY_ACTION','S1',('N_HISTORY','N_PROF','STRING4'),fill_value=' ')
        historyActionVar.setncattr('long_name','Action performed on data')
        historyActionVar.setncattr('conventions','Argo reference table 7')

        historyParameterVar = file_cdf.createVariable('HISTORY_PARAMETER','S1',('N_HISTORY','N_PROF','DATE_TIME'),fill_value=' ')
        historyParameterVar.setncattr('long_name','Station parameter action is performed on')
        historyParameterVar.setncattr('conventions','Argo reference table 3')

        historyStartPresVar = file_cdf.createVariable('HISTORY_START_PRES','f8',('N_HISTORY','N_PROF'),fill_value=99999)
        historyStartPresVar.setncattr('long_name','Start pressure action applied on')
        historyStartPresVar.setncattr('units','decibar')

        historyStopPresVar = file_cdf.createVariable('HISTORY_STOP_PRES','f8',('N_HISTORY','N_PROF'),fill_value=99999)
        historyStopPresVar.setncattr('long_name','Stop pressure action applied on')
        historyStopPresVar.setncattr('units','decibar')

        historyPreviousValueVar = file_cdf.createVariable('HISTORY_PREVIOUS_VALUE','f8',('N_HISTORY','N_PROF'),fill_value=99999)
        historyPreviousValueVar.setncattr('long_name','Parameter/Flag previous value before action')

        historyQcTestVar = file_cdf.createVariable('HISTORY_QCTEST','S1',('N_HISTORY','N_PROF','STRING16'),fill_value=' ')
        historyQcTestVar.setncattr('long_name','Documentation of tests performed, tests failed (in hex form)')
        historyQcTestVar.setncattr('conventions','Write tests performed when Load dataACTION=QCP$; tests failed when ACTION=QCF$')

        print('END OF DEFINITION');

        ##################################################################################################
        ###                                                                                             ##
        ###                                     Get data                                                ##
        ###                                                                                             ##
        ##################################################################################################

        # Profile data
        param_names = []
        for param in ms41s.get_PARAMS() :
            param_names.append(param["PARAM_NAME"])

        # Dive data
        press_data =[]
        salinity_data =[]
        temp_data = []
        station_number = []
        floatSerial = []
        firmwareVersion = []
        cyclesNb = []
        julianDay = []
        julianDayPosition = []
        latitude = []
        longitude = []
        verticalSamplingScheme = []
        configMissionNumber = []

        for cycle in mCycles.list :
            if cycle.sbe41ProfileFileName :
                for profile in cycle.sbe41Profiles :
                    if cycle.parameters.profile_sampling_method > 0:
                        verticalSamplingScheme.append("Primary sampling: averaged")
                    else :
                        verticalSamplingScheme.append("Primary sampling: discrete")
                    floatSerial.append(cycle.station_name)
                    station_number.append(cycle.station_number)
                    firmwareVersion.append(cycle.soft_version)
                    cyclesNb.append(cycle.cycleNb)
                    julianDay.append(utils.toJuld(cycle.ascentStartTime))
                    configMissionNumber.append(cycle.configMissionNumber)
                    dataPressureResized = []
                    dataSalinityResized = []
                    dataTemperatureResized = []
                    if profile.data_pressure:
                        dataPressureResized = profile.data_pressure[:]
                        for x in range(len(dataPressureResized),nLevelsDimSize):
                            dataPressureResized.append(np.float64(99999.0))
                        press_data.append(dataPressureResized)
                    if profile.data_salinity:
                        dataSalinityResized = profile.data_salinity[:]
                        for x in range(len(dataSalinityResized),nLevelsDimSize):
                            dataSalinityResized.append(np.float64(99999.0))
                        salinity_data.append(dataSalinityResized)
                    if profile.data_temperature:
                        dataTemperatureResized = profile.data_temperature[:]
                        for x in range(len(dataTemperatureResized),nLevelsDimSize):
                            dataTemperatureResized.append(np.float64(99999.0))
                        temp_data.append(dataTemperatureResized)
                    gps = cycle.locations[0]
                    julianDayPosition.append(utils.toJuld(UTCDateTime(gps.date)))
                    latitude.append(gps.latitude)
                    longitude.append(gps.longitude)

        ##################################################################################################
        ###                                                                                             ##
        ###                                     Load data                                               ##
        ###                                                                                             ##
        ##################################################################################################

        # 2.2.3 General information on the profile file

        putString(dataTypeVar,'Argo profile',string16DimSize)
        putString(formatVersionVar,'3.1',string4DimSize)
        putString(handbookVersionVar,'1.2',string64DimSize)
        putString(referenceDateTimeVar,'19500101000000',dateTimeDimSize)
        putString(dateCreationVar,currentDate,dateTimeDimSize)
        putString(dateUpdateVar,currentDate,dateTimeDimSize)

        # 2.2.4 General information for each profile

        putNString(platformNumberVar,'A9IIIII',nProfDimSize,string8DimSize)
        putNString(projectNameVar,'ARGOMermaid',nProfDimSize,string64DimSize)
        putNString(piNameVar,'Frederic Rocca',nProfDimSize,string64DimSize)
        putNString(stationParametersVar,param_names,nProfDimSize,string64DimSize)
        cycleNumberVar[:] = cyclesNb
        putString(directionVar,nProfDimSize*'A',nProfDimSize)
        putNString(dataCentreVar,cfg.history_institution,nProfDimSize,string2DimSize)
        putNString(dcReferenceVar,station_number,1,string32DimSize)
        putNString(dataStateIndicatorVar,'0A',nProfDimSize,string4DimSize)
        putString(dataModeVar,nProfDimSize*'R',nProfDimSize)
        putNString(platformTypeVar,'999',nProfDimSize,string32DimSize)
        putNString(floatSerialNoVar,floatSerial,1,string32DimSize)
        putNString(firmwareVersionVar,firmwareVersion,1,string64DimSize)
        putNString(wmoInstTypeVar,'999',nProfDimSize,string4DimSize)
        juldVar[:] = julianDay
        putString(juldQcVar,nProfDimSize*'0',nProfDimSize)
        juldLocationVar[:] = julianDayPosition
        latitudeVar[:] = latitude
        longitudeVar[:] = longitude
        putString(positionQcVar,nProfDimSize*'0',nProfDimSize)
        putNString(positionSystemVar,"GNSS",nProfDimSize,string8DimSize)
        putNString(verticalSamplingSchemeVar,verticalSamplingScheme,1,string256DimSize)
        # POSITION_ERROR_REPORTED (optional)
        # POSITION_ERROR_ESTIMATED (optional)
        # POSITION_ERROR_ESTIMATED_COMMENT (optional)
        configMissionNumberVar[:] = configMissionNumber

        # 2.2.5 Measurements for each profile

        for param in ms41s.get_PARAMS() :
            if param["PARAM_NAME"] == "PRES":
                profParamVar["PRES"][:] = press_data
                putNString(profParamQcVar["PRES"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjVar["PRES"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize
                putNString(profParamAdjQcVar["PRES"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjErrVar["PRES"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize
            if param["PARAM_NAME"] == "TEMP":
                profParamVar["TEMP"][:] = temp_data
                putNString(profParamQcVar["TEMP"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjVar["TEMP"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize
                putNString(profParamAdjQcVar["TEMP"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjErrVar["TEMP"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize
            if param["PARAM_NAME"] == "PSAL":
                profParamVar["PSAL"][:] = salinity_data
                putNString(profParamQcVar["PSAL"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjVar["PSAL"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize
                putNString(profParamAdjQcVar["PSAL"],nLevelsDimSize*'0',nProfDimSize,nLevelsDimSize)
                profParamAdjErrVar["PSAL"][:] = [[param["FILL_VALUE"]] * nLevelsDimSize] * nProfDimSize

        # 2.2.6 Calibration information for each profile
        # filled with default values

        # 2.2.7 History information for each profile
        putNString(historyInstitutionVar,[cfg.history_institution]*nHistoryDimSize,nProfDimSize,string4DimSize)
        putNString(historyStepVar,[cfg.history_step]*nHistoryDimSize,nProfDimSize,string4DimSize)
        #putNString(historySoftwareVar,[cfg.history_software]*nHistoryDimSize,nProfDimSize,string4DimSize)
        #putNString(historySoftwareReleaseVar,[cfg.history_software_release]*nHistoryDimSize,nProfDimSize,string4DimSize)
        #putNString(historyReferenceVar,[cfg.history_reference]*nHistoryDimSize,nProfDimSize,string64DimSize)
        putNString(historyDateVar,[currentDate]*nHistoryDimSize,nProfDimSize,dateTimeDimSize)
        putNString(historyActionVar,[cfg.history_action]*nHistoryDimSize,nProfDimSize,string4DimSize)
        # filled with default values
        file_cdf.close()
