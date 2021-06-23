import os
import shutil
import sys
import decrypt
import glob
import dives
import events
import profile
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
    var._Encoding = 'ascii' # this enables automatic conversion

def putString(var,string,varlen):
    putStringArray(var,[string],varlen)

def putNString(var,string,nb,varlen):
    putStringArray(var,[string]*nb,varlen)

def create_nc_trajectory_file_3_2(FloatWmoID,mfloat_nc_path,mdives,mevents,ms41s):
    trajectoryFilePath = mfloat_nc_path + FloatWmoID + "_Rtraj.nc"
    if os.path.exists(trajectoryFilePath):
        os.remove(trajectoryFilePath)

    file_cdf = Dataset(trajectoryFilePath, "w", format="NETCDF3_CLASSIC")
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
    nCycleDim = file_cdf.createDimension('N_CYCLE', mdives.get_cycle_nb());
    nMeasurementDim = file_cdf.createDimension('N_MEASUREMENT', mdives.get_position_nb());
    nCalibDim = file_cdf.createDimension('N_CALIB',1);
    nHistoryDim = file_cdf.createDimension('N_HISTORY',1);

    nProfDimSize = len(nProfDim)
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

    print(nMeasurementDimSize)
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

    juldVar = file_cdf.createVariable('JULD','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
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

    juldAdjustedVar = file_cdf.createVariable('JULD_ADJUSTED','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    juldVar.setncattr('long_name', 'Adjusted julian day (UTC) of each measurement relative to REFERENCE_DATE_TIME');
    juldVar.setncattr('standard_name', 'time');
    juldVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution
    juldVar.setncattr('axis','T')

    juldAdjustedStatusVar = file_cdf.createVariable('JULD_ADJUSTED_STATUS','S1',('N_MEASUREMENT',),fill_value=' ')
    juldAdjustedStatusVar.setncattr('long_name', 'Status of the JULD_ADJUSTED date');
    juldAdjustedStatusVar.setncattr('conventions', 'Argo reference table 19');

    juldAdjustedQcVar = file_cdf.createVariable('JULD_ADJUSTED_QC','S1',('N_MEASUREMENT',),fill_value=' ')
    juldAdjustedQcVar.setncattr('long_name', 'Qualityon adjusted date and time');
    juldAdjustedQcVar.setncattr('conventions', 'Argo reference table 2');

    latitudeVar = file_cdf.createVariable('LATITUDE','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    latitudeVar.setncattr('long_name', 'Latitude of each location');
    latitudeVar.setncattr('standard_name', 'latitude');
    latitudeVar.setncattr('units', 'degree_north');
    latitudeVar.setncattr('valid_min', np.float64(-90));
    latitudeVar.setncattr('valid_max', np.float64(90));
    latitudeVar.setncattr('axis', 'Y');

    longitudeVar = file_cdf.createVariable('LONGITUDE','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    longitudeVar.setncattr('long_name', 'Longitude of each location');
    longitudeVar.setncattr('standard_name', 'longitude');
    longitudeVar.setncattr('units', 'degree_east');
    longitudeVar.setncattr('valid_min', np.float64(-180));
    longitudeVar.setncattr('valid_max', np.float64(180));
    longitudeVar.setncattr('axis', 'X');

    positionAccuracy = file_cdf.createVariable('POSITION_ACCURACY','S1',('N_MEASUREMENT',),fill_value=' ')
    positionAccuracy.setncattr('long_name', 'Estimated accuracy in latitude and longitude');
    positionAccuracy.setncattr('conventions', 'Argo reference table 5');

    positionQc = file_cdf.createVariable('POSITION_QC','S1',('N_MEASUREMENT',),fill_value=' ')
    positionQc.setncattr('long_name', 'Quality on position');
    positionQc.setncattr('conventions', 'Argo reference table 2');

    cycleNumberVar = file_cdf.createVariable('CYCLE_NUMBER','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    cycleNumberVar.setncattr('long_name', 'Float cycle number of the measurement');
    cycleNumberVar.setncattr('conventions', '0...N, 0 :launch cycle, 1 : first complete cycle');

    cycleNumberAdjustedVar = file_cdf.createVariable('CYCLE_NUMBER_ADJUSTED','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    cycleNumberAdjustedVar.setncattr('long_name', 'Adjusted float cycle number of the measurement');
    cycleNumberAdjustedVar.setncattr('conventions', '0...N, 0 :launch cycle, 1 : first complete cycle');

    measurementCodeVar = file_cdf.createVariable('MEASUREMENT_CODE','i4',('N_MEASUREMENT',),fill_value=np.int32(99999))
    measurementCodeVar.setncattr('long_name', 'Flag referring to a measurement event in the cycle"');
    measurementCodeVar.setncattr('conventions', 'Argo reference table 15');

    profParamVar = {}
    profParamQcVar = {}
    profParamAdjVar = {}
    profParamAdjQcVar = {}
    profParamAdjErrVar = {}
    for param in ms41s.get_PARAMS() :
        profParamVar[param["PARAM_NAME"]] = file_cdf.createVariable(param["PARAM_NAME"],param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
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
        profParamQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_MEASUREMENT',),fill_value=' ')
        profParamQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
        profParamQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

        ncParamName = "{0}_ADJUSTED".format(param["PARAM_NAME"])
        profParamAdjVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
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
        profParamAdjQcVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,'S1',('N_MEASUREMENT',),fill_value=' ')
        profParamAdjQcVar[param["PARAM_NAME"]].setncattr('long_name', 'quality flag');
        profParamAdjQcVar[param["PARAM_NAME"]].setncattr('conventions', 'Argo reference table 2');

        ncParamName = "{0}_ADJUSTED_ERROR".format(param["PARAM_NAME"])
        profParamAdjErrVar[param["PARAM_NAME"]] = file_cdf.createVariable(ncParamName,param["NC_TYPE"],('N_MEASUREMENT',),fill_value=param["FILL_VALUE"])
        profParamAdjErrVar[param["PARAM_NAME"]].setncattr('long_name', "Contains the error on the adjusted values as determined by the delayed mode QC process");
        profParamAdjErrVar[param["PARAM_NAME"]].setncattr('units', param["UNITS"]);
        profParamAdjErrVar[param["PARAM_NAME"]].setncattr('C_format', param["C_FORMAT"]);
        profParamAdjErrVar[param["PARAM_NAME"]].setncattr('FORTRAN_format', param["FORTRAN_FORMAT"]);
        profParamAdjErrVar[param["PARAM_NAME"]].setncattr('resolution', param["RESOLUTION"]);

    axesErrorEllipsedMajorVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_MAJOR','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    axesErrorEllipsedMajorVar.setncattr('long_name', 'Major axis of error ellipse from positioning system');
    axesErrorEllipsedMajorVar.setncattr('units', "meters");

    axesErrorEllipsedMinorVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_MINOR','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    axesErrorEllipsedMinorVar.setncattr('long_name', 'Minor axis of error ellipse from positioning system');
    axesErrorEllipsedMinorVar.setncattr('units', "meters");

    axesErrorEllipsedAngleVar = file_cdf.createVariable('AXES_ERROR_ELLIPSE_ANGLE','f8',('N_MEASUREMENT',),fill_value=np.float64(999999.0))
    axesErrorEllipsedAngleVar.setncattr('long_name', 'Angle of error ellipse from positioning system');
    axesErrorEllipsedAngleVar.setncattr('units', "Degrees (from North when heading East)");

    satelliteNameVar = file_cdf.createVariable('SATELLITE_NAME','S1',('N_MEASUREMENT',),fill_value=' ')
    satelliteNameVar.setncattr('long_name', 'Satellite name from positioning system');
