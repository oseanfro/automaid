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
import configuration

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

def create_nc_trajectory_file_3_2(FloatWmoID,mfloat_nc_path,mCycles,ms41s):
    trajectoryFilePath = mfloat_nc_path + FloatWmoID + "_Rtraj.nc"
    if os.path.exists(trajectoryFilePath):
        os.remove(trajectoryFilePath)

    file_cdf = Dataset(trajectoryFilePath, "w", format="NETCDF3_CLASSIC")
    print(trajectoryFilePath)
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
    nParamDim = file_cdf.createDimension('N_PARAM', ms41s.get_N_PARAMS());
    nCycleDim = file_cdf.createDimension('N_CYCLE', mCycles.get_N_CYCLE());
    nMeasurementDim = file_cdf.createDimension('N_MEASUREMENT', mCycles.get_N_MEASUREMENTS());
    nCalibDim = file_cdf.createDimension('N_CALIB',1);
    nHistoryDim = file_cdf.createDimension('N_HISTORY',1);

    nParamDimSize = len(nParamDim)
    nMeasurementDimSize = len(nMeasurementDim)
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
    nCycleDimSize = len(nCycleDim)
    ##################################################################################################
    ###                                                                                             ##
    ###                                     Create Variables                                        ##
    ###                                                                                             ##
    ##################################################################################################
    file_cdf.setncattr('title','Argo float trajectory file')
    file_cdf.setncattr('institution','CORIOLIS')
    file_cdf.setncattr('source','Argo float')

    currentDate = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S");
    globalHistoryText = currentDate + ' creation; ';
    globalHistoryText += currentDate + ' last update (osean float converting raw data)'

    file_cdf.setncattr('history', globalHistoryText)
    file_cdf.setncattr('references', 'http://www.argodatamgt.org/Documentation')
    file_cdf.setncattr('user_manual_version', '3.4')
    file_cdf.setncattr('Conventions', 'Argo-3.2 CF-1.6')
    file_cdf.setncattr('featureType', 'trajectory')

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
    platformNumberVar = file_cdf.createVariable('PLATFORM_NUMBER','S1',('STRING8',),fill_value=' ')
    platformNumberVar.setncattr('long_name', 'Float unique identifier');
    platformNumberVar.setncattr('conventions', 'WMO float identifier : A9IIIII');

    projectNameVar = file_cdf.createVariable('PROJECT_NAME','S1',('STRING64',),fill_value=' ')
    projectNameVar.setncattr('long_name', 'Name of the project');

    piNameVar = file_cdf.createVariable('PI_NAME','S1',('STRING64',),fill_value=' ')
    piNameVar.setncattr('long_name', 'Name of the principal investigator');

    trajectoryParametersVar = file_cdf.createVariable('TRAJECTORY_PARAMETERS','S1',('N_PARAM','STRING64'),fill_value=' ')
    trajectoryParametersVar.setncattr('long_name', 'List of available parameters for the station');
    trajectoryParametersVar.setncattr('conventions', 'Argo reference table 3');

    dataCentreVar = file_cdf.createVariable('DATA_CENTRE','S1',('STRING2',),fill_value=' ')
    dataCentreVar.setncattr('long_name', 'Data centre in charge of float data processing');
    dataCentreVar.setncattr('conventions', 'Argo reference table 4');

    dataStateIndicatorVar = file_cdf.createVariable('DATA_STATE_INDICATOR','S1',('STRING4',),fill_value=' ')
    dataStateIndicatorVar.setncattr('long_name', 'Degree of processing the data have passed through');
    dataStateIndicatorVar.setncattr('conventions', 'Argo reference table 6');

    platformTypeVar = file_cdf.createVariable('PLATFORM_TYPE','S1',('STRING32',),fill_value=' ')
    platformTypeVar.setncattr('long_name', 'Type of float');
    platformTypeVar.setncattr('conventions', 'Argo reference table 23');

    floatSerialNoVar = file_cdf.createVariable('FLOAT_SERIAL_NO','S1',('STRING32',),fill_value=' ')
    floatSerialNoVar.setncattr('long_name', 'Serial number of the float');

    firmwareVersionVar = file_cdf.createVariable('FIRMWARE_VERSION','S1',('STRING64',),fill_value=' ')
    firmwareVersionVar.setncattr('long_name', 'Instrument firmware version');

    wmoInstTypeVar = file_cdf.createVariable('WMO_INST_TYPE','S1',('STRING4',),fill_value=' ')
    wmoInstTypeVar.setncattr('long_name', 'Coded instrument type');
    wmoInstTypeVar.setncattr('conventions', 'Argo reference table 8');

    positionSystemVar = file_cdf.createVariable('POSITIONING_SYSTEM','S1',('STRING8'),fill_value=' ')
    positionSystemVar.setncattr('long_name', 'Positioning system');

    juldVar = file_cdf.createVariable('JULD','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    juldVar.setncattr('long_name', 'Julian day (UTC) of each measurement relative to REFERENCE_DATE_TIME');
    juldVar.setncattr('standard_name', 'time');
    juldVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution
    juldVar.setncattr('axis','T')

    juldStatusVar = file_cdf.createVariable('JULD_STATUS','S1',('N_MEASUREMENT',),fill_value=' ')
    juldStatusVar.setncattr('long_name', 'Status of the date and time');
    juldStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldQcVar = file_cdf.createVariable('JULD_QC','S1',('N_MEASUREMENT',),fill_value=' ')
    juldQcVar.setncattr('long_name', 'Quality on date and time');
    juldQcVar.setncattr('conventions', 'Argo reference table 2');

    juldAdjustedVar = file_cdf.createVariable('JULD_ADJUSTED','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    juldAdjustedVar.setncattr('long_name', 'Adjusted julian day (UTC) of each measurement relative to REFERENCE_DATE_TIME');
    juldAdjustedVar.setncattr('standard_name', 'time');
    juldAdjustedVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldAdjustedVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldAdjustedVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution
    juldAdjustedVar.setncattr('axis','T')

    juldAdjustedStatusVar = file_cdf.createVariable('JULD_ADJUSTED_STATUS','S1',('N_MEASUREMENT',),fill_value=' ')
    juldAdjustedStatusVar.setncattr('long_name', 'Status of the JULD_ADJUSTED date');
    juldAdjustedStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldAdjustedQcVar = file_cdf.createVariable('JULD_ADJUSTED_QC','S1',('N_MEASUREMENT',),fill_value=' ')
    juldAdjustedQcVar.setncattr('long_name', 'Qualityon adjusted date and time');
    juldAdjustedQcVar.setncattr('conventions', 'Argo reference table 2');

    latitudeVar = file_cdf.createVariable('LATITUDE','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    latitudeVar.setncattr('long_name', 'Latitude of each location');
    latitudeVar.setncattr('standard_name', 'latitude');
    latitudeVar.setncattr('units', 'degree_north');
    latitudeVar.setncattr('valid_min', np.float64(-90));
    latitudeVar.setncattr('valid_max', np.float64(90));
    latitudeVar.setncattr('axis', 'Y');

    longitudeVar = file_cdf.createVariable('LONGITUDE','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    longitudeVar.setncattr('long_name', 'Longitude of each location');
    longitudeVar.setncattr('standard_name', 'longitude');
    longitudeVar.setncattr('units', 'degree_east');
    longitudeVar.setncattr('valid_min', np.float64(-180));
    longitudeVar.setncattr('valid_max', np.float64(180));
    longitudeVar.setncattr('axis', 'X');

    positionAccuracyVar = file_cdf.createVariable('POSITION_ACCURACY','S1',('N_MEASUREMENT',),fill_value=' ')
    positionAccuracyVar.setncattr('long_name', 'Estimated accuracy in latitude and longitude');
    positionAccuracyVar.setncattr('conventions', 'Argo reference table 5');

    positionQcVar = file_cdf.createVariable('POSITION_QC','S1',('N_MEASUREMENT',),fill_value=' ')
    positionQcVar.setncattr('long_name', 'Quality on position');
    positionQcVar.setncattr('conventions', 'Argo reference table 2');

    cycleNumberVar = file_cdf.createVariable('CYCLE_NUMBER','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    cycleNumberVar.setncattr('long_name', 'Float cycle number of the measurement');
    cycleNumberVar.setncattr('conventions', '0...N, 0 :launch cycle, 1 : first complete cycle');

    cycleNumberAdjustedVar = file_cdf.createVariable('CYCLE_NUMBER_ADJUSTED','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    cycleNumberAdjustedVar.setncattr('long_name', 'Adjusted float cycle number of the measurement');
    cycleNumberAdjustedVar.setncattr('conventions', '0...N, 0 :launch cycle, 1 : first complete cycle');

    measurementCodeVar = file_cdf.createVariable('MEASUREMENT_CODE','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    measurementCodeVar.setncattr('long_name', 'Flag referring to a measurement event in the cycle"');
    measurementCodeVar.setncattr('conventions', 'Argo reference table 15');

    paramVar = {}
    paramQcVar = {}
    paramAdjVar = {}
    paramAdjQcVar = {}
    paramAdjErrVar = {}
    paramMed = {}
    paramStd = {}
    for param in ms41s.get_PARAMS() :
        paramVar[param["PARAM_NAME"]] = file_cdf.createVariable(param["PARAM_NAME"],param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        paramVar[param["PARAM_NAME"]].setncattr('long_name', param["LONG_NAME"]);
        paramVar[param["PARAM_NAME"]].setncattr('standard_name', param["STANDARD_NAME"]);
        paramVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        paramVar[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
        paramVar[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
        paramVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        paramVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        paramVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);
        paramVar[param["PARAM_NAME"]].setncattr('axis', param["AXIS"]);

        ncParamName = "{0}_QC".format(param["PARAM_NAME"])
        paramQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_MEASUREMENT',),fill_value=' ')
        paramQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
        paramQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

        ncParamName = "{0}_ADJUSTED".format(param["PARAM_NAME"])
        paramAdjVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        paramAdjVar[param["PARAM_NAME"]].setncattr('long_name', param["LONG_NAME"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('standard_name', param["STANDARD_NAME"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);
        paramAdjVar[param["PARAM_NAME"]].setncattr('axis', param["AXIS"]);

        ncParamName = "{0}_ADJUSTED_QC".format(param["PARAM_NAME"])
        paramAdjQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_MEASUREMENT',),fill_value=' ')
        paramAdjQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
        paramAdjQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

        ncParamName = "{0}_ADJUSTED_ERROR".format(param["PARAM_NAME"])
        paramAdjErrVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        paramAdjErrVar[param["PARAM_NAME"]].setncattr('long_name', "Contains the error on the adjusted values as determined by the delayed mode QC process");
        paramAdjErrVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        paramAdjErrVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        paramAdjErrVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        paramAdjErrVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);

        ncParamName = "{0}_MED".format(param["PARAM_NAME"])
        paramMed[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        paramMed[param["PARAM_NAME"]].setncattr('long_name', "Median value of the set of measurements used to compute " + param["PARAM_NAME"]+"(N_MEASUREMENT) averaged value");
        paramMed[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        paramMed[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
        paramMed[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
        paramMed[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        paramMed[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        paramMed[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);

        ncParamName = "{0}_STD".format(param["PARAM_NAME"])
        paramStd[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        paramStd[param["PARAM_NAME"]].setncattr('long_name', "Standard deviation of the set of measurements used to compute " + param["PARAM_NAME"]+"(N_MEASUREMENT) averaged value");
        paramStd[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        paramStd[param["PARAM_NAME"]].setncattr('valid_min', param["VALID_MIN"]);
        paramStd[param["PARAM_NAME"]].setncattr('valid_max', param["VALID_MAX"]);
        paramStd[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        paramStd[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        paramStd[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);


    axesErrorEllipsedMajorVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_MAJOR','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    axesErrorEllipsedMajorVar.setncattr('long_name', 'Major axis of error ellipse from positioning system');
    axesErrorEllipsedMajorVar.setncattr('units', "meters");

    axesErrorEllipsedMinorVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_MINOR','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    axesErrorEllipsedMinorVar.setncattr('long_name', 'Minor axis of error ellipse from positioning system');
    axesErrorEllipsedMinorVar.setncattr('units', "meters");

    axesErrorEllipsedAngleVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_ANGLE','f8',('N_MEASUREMENT',),fill_value=np.float64(99999.0))
    axesErrorEllipsedAngleVar.setncattr('long_name', 'Angle of error ellipse from positioning system');
    axesErrorEllipsedAngleVar.setncattr('units', "Degrees (from North when heading East)");

    satelliteNameVar = file_cdf.createVariable('SATELLITE_NAME','S1',('N_MEASUREMENT',),fill_value=' ')
    satelliteNameVar.setncattr('long_name', 'Satellite name from positioning system');

    trajectoryParameterDataModeVar = file_cdf.createVariable('TRAJECTORY_PARAMETER_DATA_MODE','S1',('N_MEASUREMENT','N_PARAM'),fill_value=' ')
    trajectoryParameterDataModeVar.setncattr('long_name', 'Delayed mode or real time data');
    trajectoryParameterDataModeVar.setncattr('conventions', 'R : real time; D : delayed mode; A : real time with adjustment');

    juldDataModeVar = file_cdf.createVariable('JULD_DATA_MODE','S1',('N_MEASUREMENT',),fill_value=' ')
    juldDataModeVar.setncattr('long_name', 'Delayed mode or real time data');
    juldDataModeVar.setncattr('conventions', 'R : real time; D : delayed mode; A : real time with adjustment');

    juldDescentStartVar = file_cdf.createVariable('JULD_DESCENT_START','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldDescentStartVar.setncattr('long_name', 'Descent start date of the cycle');
    juldDescentStartVar.setncattr('standard_name', 'time');
    juldDescentStartVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldDescentStartVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldDescentStartVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldDescentStartStatusVar = file_cdf.createVariable('JULD_DESCENT_START_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldDescentStartStatusVar.setncattr('long_name', 'Status of descent start date of the cycle');
    juldDescentStartStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldFirstStabilizationVar = file_cdf.createVariable('JULD_FIRST_STABILIZATION','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldFirstStabilizationVar.setncattr('long_name', 'Time when a float first becomes water-neutral');
    juldFirstStabilizationVar.setncattr('standard_name', 'time');
    juldFirstStabilizationVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldFirstStabilizationVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldFirstStabilizationVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldFirstStabilizationStatusVar = file_cdf.createVariable('JULD_FIRST_STABILIZATION_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldFirstStabilizationStatusVar.setncattr('long_name', 'Status of time when a float first becomes water-neutral');
    juldFirstStabilizationStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldDescentEndVar = file_cdf.createVariable('JULD_DESCENT_END','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldDescentEndVar.setncattr('long_name', 'Descent end date of the cycle');
    juldDescentEndVar.setncattr('standard_name', 'time');
    juldDescentEndVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldDescentEndVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldDescentEndVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldDescentEndStatusVar = file_cdf.createVariable('JULD_DESCENT_END_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldDescentEndStatusVar.setncattr('long_name', 'Status of descent end date of the cycle');
    juldDescentEndStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldParkStartVar = file_cdf.createVariable('JULD_PARK_START','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldParkStartVar.setncattr('long_name', 'Drift start date of the cycle');
    juldParkStartVar.setncattr('standard_name', 'time');
    juldParkStartVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldParkStartVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldParkStartVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldParkStartStatusVar = file_cdf.createVariable('JULD_PARK_START_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldParkStartStatusVar.setncattr('long_name', 'Status of drift start date of the cycle');
    juldParkStartStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldParkEndVar = file_cdf.createVariable('JULD_PARK_END','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldParkEndVar.setncattr('long_name', 'Drift end date of the cycle');
    juldParkEndVar.setncattr('standard_name', 'time');
    juldParkEndVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldParkEndVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldParkEndVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldParkEndStatusVar = file_cdf.createVariable('JULD_PARK_END_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldParkEndStatusVar.setncattr('long_name', 'Status of drift end date of the cycle');
    juldParkEndStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldDeepDescentEndVar = file_cdf.createVariable('JULD_DEEP_DESCENT_END','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldDeepDescentEndVar.setncattr('long_name', 'Deep descent end date of the cycle');
    juldDeepDescentEndVar.setncattr('standard_name', 'time');
    juldDeepDescentEndVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldDeepDescentEndVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldDeepDescentEndVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldDeepDescentEndStatusVar = file_cdf.createVariable('JULD_DEEP_DESCENT_END_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldDeepDescentEndStatusVar.setncattr('long_name', 'Status of deep descent end date of the cycle');
    juldDeepDescentEndStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldDeepParkStartVar = file_cdf.createVariable('JULD_DEEP_PARK_START','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldDeepParkStartVar.setncattr('long_name', 'Deep park start date of the cycle');
    juldDeepParkStartVar.setncattr('standard_name', 'time');
    juldDeepParkStartVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldDeepParkStartVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldDeepParkStartVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldDeepParkStartStatusVar = file_cdf.createVariable('JULD_DEEP_PARK_START_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldDeepParkStartStatusVar.setncattr('long_name', 'Status of deep park start date of the cycle');
    juldDeepParkStartStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldAscentStartVar = file_cdf.createVariable('JULD_ASCENT_START','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldAscentStartVar.setncattr('long_name', 'Start date of the ascent to the surface');
    juldAscentStartVar.setncattr('standard_name', 'time');
    juldAscentStartVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldAscentStartVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldAscentStartVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldAscentStartStatusVar = file_cdf.createVariable('JULD_ASCENT_START_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldAscentStartStatusVar.setncattr('long_name', 'Status of start date of the ascent to the surface');
    juldAscentStartStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldAscentEndVar = file_cdf.createVariable('JULD_ASCENT_END','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldAscentEndVar.setncattr('long_name', 'End date of ascent to the surface');
    juldAscentEndVar.setncattr('standard_name', 'time');
    juldAscentEndVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldAscentEndVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldAscentEndVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldAscentEndStatusVar = file_cdf.createVariable('JULD_ASCENT_END_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldAscentEndStatusVar.setncattr('long_name', 'Status of end date of ascent to the surface');
    juldAscentEndStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldTransmissionStartVar = file_cdf.createVariable('JULD_TRANSMISSION_START','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldTransmissionStartVar.setncattr('long_name', 'Start date of transmission');
    juldTransmissionStartVar.setncattr('standard_name', 'time');
    juldTransmissionStartVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldTransmissionStartVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldTransmissionStartVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldTransmissionStartStatusVar = file_cdf.createVariable('JULD_TRANSMISSION_START_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldTransmissionStartStatusVar.setncattr('long_name', 'Status of start date of transmission');
    juldTransmissionStartStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldFirstMessageVar = file_cdf.createVariable('JULD_FIRST_MESSAGE','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldFirstMessageVar.setncattr('long_name', 'Date of earliest float message received');
    juldFirstMessageVar.setncattr('standard_name', 'time');
    juldFirstMessageVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldFirstMessageVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldFirstMessageVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldFirstMessageStatusVar = file_cdf.createVariable('JULD_FIRST_MESSAGE_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldFirstMessageStatusVar.setncattr('long_name', 'Status of date of earliest float message received');
    juldFirstMessageStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldFirstLocationVar = file_cdf.createVariable('JULD_FIRST_LOCATION','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldFirstLocationVar.setncattr('long_name', 'Date of earliest location');
    juldFirstLocationVar.setncattr('standard_name', 'time');
    juldFirstLocationVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldFirstLocationVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldFirstLocationVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldFirstLocationStatusVar = file_cdf.createVariable('JULD_FIRST_LOCATION_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldFirstLocationStatusVar.setncattr('long_name', 'Status of date of earliest location');
    juldFirstLocationStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldLastLocationVar = file_cdf.createVariable('JULD_LAST_LOCATION','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldLastLocationVar.setncattr('long_name', 'Date of latest location');
    juldLastLocationVar.setncattr('standard_name', 'time');
    juldLastLocationVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldLastLocationVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldLastLocationVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldLastLocationStatusVar = file_cdf.createVariable('JULD_LAST_LOCATION_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldLastLocationStatusVar.setncattr('long_name', 'Status of date of latest location');
    juldLastLocationStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldLastMessageVar = file_cdf.createVariable('JULD_LAST_MESSAGE','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldLastMessageVar.setncattr('long_name', 'Date of latest float message received');
    juldLastMessageVar.setncattr('standard_name', 'time');
    juldLastMessageVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldLastMessageVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldLastMessageVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldLastMessageStatusVar = file_cdf.createVariable('JULD_LAST_MESSAGE_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldLastMessageStatusVar.setncattr('long_name', 'Status of date of latest float message received');
    juldLastMessageStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldTransmissionEndVar = file_cdf.createVariable('JULD_TRANSMISSION_END','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    juldTransmissionEndVar.setncattr('long_name', 'Transmission end date');
    juldTransmissionEndVar.setncattr('standard_name', 'time');
    juldTransmissionEndVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldTransmissionEndVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldTransmissionEndVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution

    juldTransmissionEndStatusVar = file_cdf.createVariable('JULD_TRANSMISSION_END_STATUS','S1',('N_CYCLE',),fill_value=' ')
    juldTransmissionEndStatusVar.setncattr('long_name', 'Status of transmission end date');
    juldTransmissionEndStatusVar.setncattr('conventions', 'Argo reference table 19');

    clockOffsetVar = file_cdf.createVariable('CLOCK_OFFSET','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    clockOffsetVar.setncattr('long_name', 'Time of float clock drift');
    clockOffsetVar.setncattr('units', 'days');
    clockOffsetVar.setncattr('conventions', 'Days with decimal part (as parts of day)');

    groundedVar = file_cdf.createVariable('GROUNDED','S1',('N_CYCLE',),fill_value=' ')
    groundedVar.setncattr('long_name', 'Did the profiler touch the ground for that cycle?');
    groundedVar.setncattr('conventions', 'Argo reference table 20');

    representativeParkPressureVar = file_cdf.createVariable('REPRESENTATIVE_PARK_PRESSURE','f8',('N_CYCLE',),fill_value=np.float64(99999.0))
    representativeParkPressureVar.setncattr('long_name', 'Best pressure value during park phase');
    representativeParkPressureVar.setncattr('units', 'decibar');

    representativeParkPressureStatusVar = file_cdf.createVariable('REPRESENTATIVE_PARK_PRESSURE_STATUS','S1',('N_CYCLE',),fill_value=' ')
    representativeParkPressureStatusVar.setncattr('long_name', 'Status of best pressure value during park phase');
    representativeParkPressureStatusVar.setncattr('conventions', 'Argo reference table 21');

    configMissionNumberVar = file_cdf.createVariable('CONFIG_MISSION_NUMBER','i4',('N_CYCLE',),fill_value=np.int32(99999))
    configMissionNumberVar.setncattr('long_name', 'Unique number denoting the missions performed by the float');
    configMissionNumberVar.setncattr('conventions', '1...N, 1 : first complete mission');

    cycleNumberIndexVar = file_cdf.createVariable('CYCLE_NUMBER_INDEX','i4',('N_CYCLE',),fill_value=np.int32(99999))
    cycleNumberIndexVar.setncattr('long_name', 'Cycle number that corresponds to the current index');
    cycleNumberIndexVar.setncattr('conventions', '0...N, 0 : launch cycle, 1 : first complete cycle');

    cycleNumberIndexAdjustedVar = file_cdf.createVariable('CYCLE_NUMBER_INDEX_ADJUSTED','i4',('N_CYCLE',),fill_value=np.int32(99999))
    cycleNumberIndexAdjustedVar.setncattr('long_name', 'Adjusted cycle number that corresponds to the current index');
    cycleNumberIndexAdjustedVar.setncattr('conventions', '0...N, 0 : launch cycle, 1 : first complete cycle');

    dataModeVar = file_cdf.createVariable('DATA_MODE','S1',('N_CYCLE',),fill_value=' ')
    dataModeVar.setncattr('long_name', 'Delayed mode or real time data');
    dataModeVar.setncattr('conventions', 'R : real time; D : delayed mode; A : real time with adjustment');

    scientificCalibParameterVar = file_cdf.createVariable('PARAMETER','S1',('N_CALIB','N_PARAM','STRING256'),fill_value=' ')
    scientificCalibParameterVar.setncattr('long_name','List of parameters with calibration information')
    scientificCalibParameterVar.setncattr('conventions','Argo reference table 3')

    scientificCalibEquationVar = file_cdf.createVariable('SCIENTIFIC_CALIB_EQUATION','S1',('N_CALIB','N_PARAM','STRING256'),fill_value=' ')
    scientificCalibEquationVar.setncattr('long_name','Calibration equation for this parameter')

    scientificCalibCoefficientVar = file_cdf.createVariable('SCIENTIFIC_CALIB_COEFFICIENT','S1',('N_CALIB','N_PARAM','STRING256'),fill_value=' ')
    scientificCalibCoefficientVar.setncattr('long_name','Calibration coefficients for this parameter')

    scientificCalibCommentVar = file_cdf.createVariable('SCIENTIFIC_CALIB_COMMENT','S1',('N_CALIB','N_PARAM','STRING256'),fill_value=' ')
    scientificCalibCommentVar.setncattr('long_name','Comment applying to this parameter calibration')

    scientificCalibDateVar = file_cdf.createVariable('SCIENTIFIC_CALIB_DATE','S1',('N_CALIB','N_PARAM','DATE_TIME'),fill_value=' ')
    scientificCalibDateVar.setncattr('long_name','Date of calibration')
    scientificCalibDateVar.setncattr('conventions','YYYYMMDDHHMISS')

    historyInstitutionVar = file_cdf.createVariable('HISTORY_INSTITUTION','S1',('N_HISTORY','STRING4'),fill_value=' ')
    historyInstitutionVar.setncattr('long_name','Institution which performed action')
    historyInstitutionVar.setncattr('conventions','Argo reference table 4')

    historyStepVar = file_cdf.createVariable('HISTORY_STEP','S1',('N_HISTORY','STRING4'),fill_value=' ')
    historyStepVar.setncattr('long_name','Step in data processing')
    historyStepVar.setncattr('conventions','Argo reference table 12')

    historySoftwareVar = file_cdf.createVariable('HISTORY_SOFTWARE','S1',('N_HISTORY','STRING4'),fill_value=' ')
    historySoftwareVar.setncattr('long_name','Name of software which performed action')
    historySoftwareVar.setncattr('conventions','Institution dependent')

    historySoftwareReleaseVar = file_cdf.createVariable('HISTORY_SOFTWARE_RELEASE','S1',('N_HISTORY','STRING4'),fill_value=' ')
    historySoftwareReleaseVar.setncattr('long_name','Version/release of software which performed action')
    historySoftwareReleaseVar.setncattr('conventions','Institution dependent')

    historyReferenceVar = file_cdf.createVariable('HISTORY_REFERENCE','S1',('N_HISTORY','STRING64'),fill_value=' ')
    historyReferenceVar.setncattr('long_name','Reference of database')
    historyReferenceVar.setncattr('conventions','Institution dependent')

    historyDateVar = file_cdf.createVariable('HISTORY_DATE','S1',('N_HISTORY','DATE_TIME'),fill_value=' ')
    historyDateVar.setncattr('long_name','Date the history record was created')
    historyDateVar.setncattr('conventions','YYYYMMDDHHMISS')

    historyActionVar = file_cdf.createVariable('HISTORY_ACTION','S1',('N_HISTORY','STRING4'),fill_value=' ')
    historyActionVar.setncattr('long_name','Action performed on data')
    historyActionVar.setncattr('conventions','Argo reference table 7')

    historyParameterVar = file_cdf.createVariable('HISTORY_PARAMETER','S1',('N_HISTORY','STRING64'),fill_value=' ')
    historyParameterVar.setncattr('long_name','Station parameter action is performed on')
    historyParameterVar.setncattr('conventions','Argo reference table 3')

    historyPreviousValueVar = file_cdf.createVariable('HISTORY_PREVIOUS_VALUE','f8',('N_HISTORY',),fill_value=np.float64(99999.0))
    historyPreviousValueVar.setncattr('long_name','Parameter/Flag previous value before action')

    historyIndexDimensionVar = file_cdf.createVariable('HISTORY_INDEX_DIMENSION','S1',('N_HISTORY',),fill_value=' ')
    historyIndexDimensionVar.setncattr('long_name','Name of dimension to which HISTORY_START_INDEX and HISTORY_STOP_INDEX correspond')
    historyIndexDimensionVar.setncattr('conventions','C: N_CYCLE, M:N_MEASUREMENT')

    historyStartIndexVar = file_cdf.createVariable('HISTORY_START_INDEX','i4',('N_HISTORY',),fill_value=np.int32(99999))
    historyStartIndexVar.setncattr('long_name', 'Start index action applied on');

    historyStopIndexVar = file_cdf.createVariable('HISTORY_STOP_INDEX','i4',('N_HISTORY',),fill_value=np.int32(99999))
    historyStopIndexVar.setncattr('long_name', 'Stop index action applied on');

    historyQcTestVar = file_cdf.createVariable('HISTORY_QCTEST','S1',('N_HISTORY','STRING16'),fill_value=' ')
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
    floatSerial = mCycles.get_station_nb()
    softVersions = mCycles.get_software_versions()
    print (softVersions)
    if len(softVersions) > 1 :
        print("!!!!!!!!!!!!!!!!!!!!! No unique software version !!!!!!!!!!!!!!!!!")
        file_cdf.close()
        return
    softVersion = softVersions[0]

    # N_MEASUREMENT dimension
    juld = []
    juldStatus = ""
    juldQc = ""
    juldAdjusted = []
    juldAdjustedStatus = ""
    juldAdjustedQc = ""
    latitude = []
    longitude = []
    positionAccuracy = ""
    positionQc = ""
    cycleNumber = []
    cycleNumberAdjusted = []
    measurementCode = []
    pressure = []
    pressureQc = ""
    pressureAjusted = []
    pressureAjustedQc = ""
    pressureAjustedError = []
    pressureMed = []
    pressureStd = []
    temperature = []
    temperatureQc = ""
    temperatureAjusted = []
    temperatureAjustedQc = ""
    temperatureAjustedError = []
    temperatureMed = []
    temperatureStd = []
    salinity = []
    salinityQc = ""
    salinityAjusted = []
    salinityAjustedQc = ""
    salinityAjustedError = []
    salinityMed = []
    salinityStd = []
    trajectoryParameterDataMode = []
    juldDataMode = ""

    # N_CYCLE dimension
    juldDescentStart = []
    juldDescentStartStatus = ""
    juldFirstStabilization = []
    juldFirstStabilizationStatus = ""
    juldDescentEnd = []
    juldDescentEndStatus = ""
    juldParkStart = []
    juldParkStartStatus = ""
    juldParkEnd = []
    juldParkEndStatus = ""
    juldDeepDescentEnd = []
    juldDeepDescentEndStatus = ""
    juldDeepParkStart = []
    juldDeepParkStartStatus = ""
    juldAscentStart = []
    juldAscentStartStatus = ""
    juldAscentEnd = []
    juldAscentEndStatus = ""
    juldTransmissionStart = []
    juldTransmissionStartStatus = ""
    juldFirstMessage = []
    juldFirstMessageStatus = ""
    juldFirstLocation = []
    juldFirstLocationStatus = ""
    juldLastLocation = []
    juldLastLocationStatus = ""
    juldLastMessage = []
    juldLastMessageStatus = ""
    juldTransmissionEnd = []
    juldTransmissionEndStatus = ""
    clockOffset = []
    grounded = ""
    representativeParkPressure = []
    representativeParkPressureStatus = ""
    configMissionNumber = []
    cycleNumberIndex = []
    cycleNumberIndexAdjusted = []
    dataMode = ""

    for cycle in mCycles.list :
        # Get all measurements
        for measure in cycle.measures:
            juld.append(utils.toJuld(measure.date))
            juldStatus += '2'
            juldQc += '0'
            juldAdjusted.append(np.float64(99999.0))
            juldAdjustedStatus += '2'
            latitude.append(measure.latitude)
            longitude.append(measure.longitude)
            positionAccuracy += 'H'
            positionQc += '0'
            cycleNumber.append(measure.cycle)
            cycleNumberAdjusted.append(np.int32(99999))
            measurementCode.append(measure.code)
            pressure.append(measure.pressure)
            pressureQc += '0'
            pressureAjusted.append(np.float64(99999.0))
            pressureAjustedQc += '0'
            pressureAjustedError.append(np.float64(99999.0))
            pressureMed.append(np.float64(99999.0))
            pressureStd.append(np.float64(99999.0))
            temperature.append(measure.temperature)
            temperatureQc += '0'
            temperatureAjusted.append(np.float64(99999.0))
            temperatureAjustedQc += '0'
            temperatureAjustedError.append(np.float64(99999.0))
            temperatureMed.append(np.float64(99999.0))
            temperatureStd.append(np.float64(99999.0))
            salinity.append(measure.salinity)
            salinityQc += '0'
            salinityAjusted.append(np.float64(99999.0))
            salinityAjustedQc += '0'
            salinityAjustedError.append(np.float64(99999.0))
            salinityMed.append(np.float64(99999.0))
            salinityStd.append(np.float64(99999.0))
            trajectoryParameterDataMode.append(ms41s.get_N_PARAMS() * 'R')
            juldDataMode += 'R'
        if cycle.descentStartTime :
            juldDescentStart.append(utils.toJuld(cycle.descentStartTime))
            juldDescentStartStatus += '2'
        else :
            juldDescentStart.append(np.float64(99999.0))
        if cycle.descentEndTime :
            juldDescentEnd.append(utils.toJuld(cycle.descentEndTime))
            juldDescentEndStatus += '2'
        else :
            juldDescentEnd.append(np.float64(99999.0))
        if cycle.parkEndTime :
            juldParkEnd.append(utils.toJuld(cycle.parkEndTime))
            juldParkEndStatus += '2'
        else :
            juldParkEnd.append(np.float64(99999.0))
        if cycle.deepDescentEndTime :
            juldDeepDescentEnd.append(utils.toJuld(cycle.deepDescentEndTime))
            juldDeepDescentEndStatus += '2'
        else :
            juldDeepDescentEnd.append(np.float64(99999.0))
        if cycle.ascentStartTime :
            juldAscentStart.append(utils.toJuld(cycle.ascentStartTime))
            juldAscentStartStatus += '2'
        else :
            juldAscentStart.append(np.float64(99999.0))
        if cycle.ascentEndTime :
            juldAscentEnd.append(utils.toJuld(cycle.ascentStartTime))
            juldAscentEndStatus += '2'
        else :
            juldAscentEnd.append(np.float64(99999.0))
        if cycle.transmissionStartTime :
            juldTransmissionStart.append(utils.toJuld(cycle.transmissionStartTime))
            juldTransmissionStartStatus += '2'
        else :
            juldTransmissionStart.append(np.float64(99999.0))
        if cycle.firstMessageTime :
            juldFirstMessage.append(utils.toJuld(cycle.firstMessageTime))
            juldFirstMessageStatus += '2'
        else :
            juldFirstMessage.append(np.float64(99999.0))
        if cycle.firstLocationTime :
            juldFirstLocation.append(utils.toJuld(cycle.firstLocationTime))
            juldFirstLocationStatus += '2'
        else :
            juldFirstLocation.append(np.float64(99999.0))
        if cycle.lastLocationTime :
            juldLastLocation.append(utils.toJuld(cycle.lastLocationTime))
            juldLastLocationStatus += '2'
        else :
            juldLastLocation.append(np.float64(99999.0))
        if cycle.lastMessageTime :
            juldLastMessage.append(utils.toJuld(cycle.lastMessageTime))
            juldLastMessageStatus += '2'
        else :
            juldLastMessage.append(np.float64(99999.0))
        if cycle.transmissionEndTime :
            juldTransmissionEnd.append(utils.toJuld(cycle.transmissionEndTime))
            juldTransmissionEndStatus += '2'
        else :
            juldTransmissionEnd.append(np.float64(99999.0))
        if cycle.clockOffset :
            clockOffset.append(cycle.clockOffset)
        grounded += 'N'
        representativeParkPressure.append(cycle.park_pressure_dbar)
        representativeParkPressureStatus += cycle.park_pressure_status
        configMissionNumber.append(cycle.configMissionNumber)
        cycleNumberIndex.append(cycle.cycleNb)
        cycleNumberIndexAdjusted.append(np.int32(99999))
        dataMode += 'R'

    ##################################################################################################
    ###                                                                                             ##
    ###                                     Load data                                               ##
    ###                                                                                             ##
    ##################################################################################################
    # 2.3.3 General information on the trajectory file
    putString(dataTypeVar,'Argo trajectory',string16DimSize)
    putString(formatVersionVar,'3.2',string4DimSize)
    putString(handbookVersionVar,'1.2',string64DimSize)
    putString(referenceDateTimeVar,'19500101000000',dateTimeDimSize)
    putString(dateCreationVar,currentDate,dateTimeDimSize)
    putString(dateUpdateVar,currentDate,dateTimeDimSize)

    # 2.3.4 General information on the float
    putString(platformNumberVar,'A9IIIII',string8DimSize)
    putString(projectNameVar,'ARGOMermaid',string64DimSize)
    putString(piNameVar,'Frederic Rocca',string64DimSize)
    putString(trajectoryParametersVar,param_names,string64DimSize)
    putString(dataCentreVar,cfg.history_institution,string2DimSize)
    putString(dataStateIndicatorVar,'0A',string4DimSize)
    putString(platformTypeVar,'999',string32DimSize)
    putString(floatSerialNoVar,floatSerial,string32DimSize)
    putString(firmwareVersionVar,softVersion,string64DimSize)
    putString(wmoInstTypeVar,'999',string4DimSize)
    putString(positionSystemVar,"GNSS",string8DimSize)

    # 2.3.5 N_MEASUREMENT dimension variable group
    juldVar[:] = juld
    putString(juldStatusVar,juldStatus,nMeasurementDimSize)
    putString(juldQcVar,juldQc,nMeasurementDimSize)
    juldAdjustedVar[:] = juldAdjusted
    putString(juldAdjustedStatusVar,juldAdjustedStatus,nMeasurementDimSize)
    putString(juldAdjustedQcVar,juldAdjustedQc,nMeasurementDimSize)
    latitudeVar[:] = latitude
    longitudeVar[:] = longitude
    putString(positionAccuracyVar,positionAccuracy,nMeasurementDimSize)
    putString(positionQcVar,positionQc,nMeasurementDimSize)
    cycleNumberVar[:] = cycleNumber
    cycleNumberAdjusted[:] = cycleNumberAdjusted
    measurementCodeVar[:] = measurementCode
    for param in ms41s.get_PARAMS() :
        if param["PARAM_NAME"] == "PRES":
            paramVar["PRES"][:] = pressure
            putString(paramQcVar["PRES"],pressureQc,nMeasurementDimSize)
            paramAdjVar["PRES"][:] = pressureAjusted
            putString(paramAdjQcVar["PRES"],pressureAjustedQc,nMeasurementDimSize)
            paramAdjErrVar["PRES"][:] = pressureAjustedError
            paramMed["PRES"][:] = pressureMed
            paramStd["PRES"][:] = pressureStd
        if param["PARAM_NAME"] == "TEMP":
            paramVar["TEMP"][:] = temperature
            putString(paramQcVar["TEMP"],temperatureQc,nMeasurementDimSize)
            paramAdjVar["TEMP"][:] = temperatureAjusted
            putString(paramAdjQcVar["TEMP"],temperatureAjustedQc,nMeasurementDimSize)
            paramAdjErrVar["TEMP"][:] = temperatureAjustedError
            paramMed["TEMP"][:] = temperatureMed
            paramStd["TEMP"][:] = temperatureStd
        if param["PARAM_NAME"] == "PSAL":
            paramVar["PSAL"][:] = salinity
            putString(paramQcVar["PSAL"],salinityQc,nMeasurementDimSize)
            paramAdjVar["PSAL"][:] = salinityAjusted
            putString(paramAdjQcVar["PSAL"],salinityAjustedQc,nMeasurementDimSize)
            paramAdjErrVar["PSAL"][:] = salinityAjustedError
            paramMed["PSAL"][:] = salinityMed
            paramStd["PSAL"][:] = salinityStd
    putNString(trajectoryParameterDataModeVar,trajectoryParameterDataMode,1,nParamDimSize)
    putString(juldDataModeVar,juldDataMode,nMeasurementDimSize)
    # 2.3.6 N_CYCLE dimension variable group
    juldDescentStartVar[:] = juldDescentStart
    putString(juldDescentStartStatusVar,juldDescentStartStatus,nCycleDimSize)
    juldDescentEndVar[:] = juldDescentEnd
    putString(juldDescentEndStatusVar,juldDescentEndStatus,nCycleDimSize)
    juldParkEndVar[:] = juldParkEnd
    putString(juldParkEndStatusVar,juldParkEndStatus,nCycleDimSize)
    juldDeepDescentEndVar[:] = juldDeepDescentEnd
    putString(juldDeepDescentEndStatusVar,juldDeepDescentEndStatus,nCycleDimSize)
    juldAscentStartVar[:] = juldAscentStart
    putString(juldAscentStartStatusVar,juldAscentStartStatus,nCycleDimSize)
    juldAscentEndVar[:] = juldAscentEnd
    putString(juldAscentEndStatusVar,juldAscentEndStatus,nCycleDimSize)
    juldTransmissionStartVar[:] = juldTransmissionStart
    putString(juldTransmissionStartStatusVar,juldTransmissionStartStatus,nCycleDimSize)
    juldFirstMessageVar[:] = juldFirstMessage
    putString(juldFirstMessageStatusVar,juldFirstMessageStatus,nCycleDimSize)
    juldFirstLocationVar[:] = juldFirstLocation
    putString(juldFirstLocationStatusVar,juldFirstLocationStatus,nCycleDimSize)
    juldLastLocationVar[:] = juldLastLocation
    putString(juldLastLocationStatusVar,juldLastLocationStatus,nCycleDimSize)
    juldLastMessageVar[:] = juldLastMessage
    putString(juldLastMessageStatusVar,juldLastMessageStatus,nCycleDimSize)
    juldTransmissionEndVar[:] = juldTransmissionEnd
    putString(juldTransmissionEndStatusVar,juldTransmissionEndStatus,nCycleDimSize)
    clockOffsetVar[:] = clockOffset
    putString(groundedVar,grounded,nCycleDimSize)
    representativeParkPressureVar[:] = representativeParkPressure
    putString(representativeParkPressureStatusVar,representativeParkPressureStatus,nCycleDimSize)
    configMissionNumberVar[:] = configMissionNumber
    cycleNumberIndexVar[:] = cycleNumberIndex
    cycleNumberIndexAdjustedVar[:] = cycleNumberIndexAdjusted
    putString(dataModeVar,dataMode,nCycleDimSize)
    # 2.3.7 Scientific calibration section
    # filled with default values
    # 2.3.8 History information
    # filled with default values
    file_cdf.close()
