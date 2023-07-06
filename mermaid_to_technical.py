# @Author: Frédéric Rocca <fro>
# @Date:   2023-06-28T14:18:43+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: mermaid_to_technical.py
# @Last modified by:   fro
# @Last modified time: 2023-07-06T15:37:48+02:00

import os
import json
import shutil
import sys
import decrypt
import glob
import dives
import events
import sbe41
import re
import utils
from obspy import UTCDateTime
from netCDF4 import Dataset
from netCDF4 import stringtochar
from datetime import datetime,timezone
import numpy as np
import configuration
import argo_metadata


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


def create_nc_technical_file_3_2(FloatWmoID,mfloat_nc_path,mCycles,metadata):
    technicalFilePath = mfloat_nc_path + FloatWmoID + "_tech.nc"
    if os.path.exists(technicalFilePath):
        os.remove(technicalFilePath)

    file_cdf = Dataset(technicalFilePath, "w", format="NETCDF3_CLASSIC")
    print(technicalFilePath)
    ##################################################################################################
    ###                                                                                             ##
    ###                                     Create Dimensions                                       ##
    ###                                                                                             ##
    ##################################################################################################
    dateTimeDim = file_cdf.createDimension('DATE_TIME', 14);
    string128Dim = file_cdf.createDimension('STRING128', 128);
    string32Dim = file_cdf.createDimension('STRING32', 32);
    string8Dim = file_cdf.createDimension('STRING8', 8);
    string4Dim = file_cdf.createDimension('STRING4', 4);
    string2Dim = file_cdf.createDimension('STRING2', 2);
    nTechParamDim = file_cdf.createDimension('N_TECH_PARAM', mCycles.get_N_TECHNICAL());
    nTechMeasurementDim = file_cdf.createDimension('N_TECH_MEASUREMENT', 0);

    nTechParamDimSize = len(nTechParamDim)
    nTechMeasurementDimSize = len(nTechMeasurementDim)
    string2DimSize = len(string2Dim)
    string4DimSize = len(string4Dim)
    string8DimSize = len(string8Dim)
    string32DimSize = len(string32Dim)
    string128DimSize = len(string128Dim)
    dateTimeDimSize = len(dateTimeDim)
    ##################################################################################################
    ###                                                                                             ##
    ###                                     Create Variables                                        ##
    ###                                                                                             ##
    ##################################################################################################
    file_cdf.setncattr('title','Argo float technical data file')
    file_cdf.setncattr('institution','CORIOLIS')
    file_cdf.setncattr('source','Argo float')

    currentDate = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S");
    globalHistoryText = metadata["DATE_CREATION"] + ' creation; ';
    globalHistoryText += currentDate + ' last update (osean float converting raw data)'

    file_cdf.setncattr('history', globalHistoryText)
    file_cdf.setncattr('references', 'http://www.argodatamgt.org/Documentation')
    file_cdf.setncattr('comment', '')
    file_cdf.setncattr('user_manual_version', '3.41.1')
    file_cdf.setncattr('Conventions', 'Argo-3.1 CF-1.6')

    dataTypeVar = file_cdf.createVariable('DATA_TYPE','S1',('STRING32',),fill_value=' ')
    dataTypeVar.setncattr('long_name', 'Data type')
    dataTypeVar.setncattr('conventions', 'Argo reference table 1')

    platformNumberVar = file_cdf.createVariable('PLATFORM_NUMBER','S1',('STRING8',),fill_value=' ')
    platformNumberVar.setncattr('long_name', 'Float unique identifier');
    platformNumberVar.setncattr('conventions', 'WMO float identifier : A9IIIII');

    formatVersionVar = file_cdf.createVariable('FORMAT_VERSION','S1',('STRING4',),fill_value=' ')
    formatVersionVar.setncattr('long_name', 'File format version')

    handbookVersionVar = file_cdf.createVariable('HANDBOOK_VERSION','S1',('STRING4',),fill_value=' ')
    handbookVersionVar.setncattr('long_name', 'Data handbook version')

    dataCentreVar = file_cdf.createVariable('DATA_CENTRE','S1',('STRING2',),fill_value=' ')
    dataCentreVar.setncattr('long_name', 'Data centre in charge of float data processing');
    dataCentreVar.setncattr('conventions', 'Argo reference table 4');

    dateCreationVar = file_cdf.createVariable('DATE_CREATION','S1',('DATE_TIME',),fill_value=' ')
    dateCreationVar.setncattr('long_name', 'Date of file creation')
    dateCreationVar.setncattr('conventions', 'YYYYMMDDHHMISS')

    dateUpdateVar = file_cdf.createVariable('DATE_UPDATE','S1',('DATE_TIME',),fill_value=' ')
    dateUpdateVar.setncattr('long_name', 'Date of update of this file');
    dateUpdateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    technicalParamNameVar = file_cdf.createVariable('TECHNICAL_PARAMETER_NAME','S1',('N_TECH_PARAM','STRING128'),fill_value=' ')
    technicalParamNameVar.setncattr('long_name', 'Name of technical parameter');

    technicalParamValueVar = file_cdf.createVariable('TECHNICAL_PARAMETER_VALUE','S1',('N_TECH_PARAM','STRING128'),fill_value=' ')
    technicalParamValueVar.setncattr('long_name', 'Value of technical parameter');

    cycleNumberVar = file_cdf.createVariable('CYCLE_NUMBER','i4',('N_TECH_PARAM',),fill_value=np.int32(99999))
    cycleNumberVar.setncattr('long_name', 'Float cycle number');
    cycleNumberVar.setncattr('conventions', '0...N, 0 : launch cycle (if exists), 1 : first complete cycle');

    juldVar = file_cdf.createVariable('JULD','f8',('N_TECH_MEASUREMENT',),fill_value=np.float64(99999.0))
    juldVar.setncattr('long_name', 'Julian day (UTC) of each measurement');
    juldVar.setncattr('standard_name', 'time');
    juldVar.setncattr('units', 'days since 1950-01-01 00:00:00 UTC');
    juldVar.setncattr('conventions', 'Relative julian days with decimal part (as parts of day)');
    juldVar.setncattr('resolution', np.float64(1/86400)); # 1 second of resolution
    juldVar.setncattr('axis','T')

    cycleNumberMeasVar = file_cdf.createVariable('CYCLE_NUMBER_MEAS','i4',('N_TECH_MEASUREMENT',),fill_value=np.int32(99999))
    cycleNumberMeasVar.setncattr('long_name', 'Float cycle number');
    cycleNumberMeasVar.setncattr('conventions', '0...N, 0 : launch cycle (if exists), 1 : first complete cycle');

    measurementCodeVar = file_cdf.createVariable('MEASUREMENT_CODE','i4',('N_TECH_MEASUREMENT',),fill_value=np.int32(99999))
    measurementCodeVar.setncattr('long_name', 'Flag referring to a measurement event in the cycle');
    measurementCodeVar.setncattr('conventions', 'Argo reference table 15');

    ##################################################################################################
    ###                                                                                             ##
    ###                                     Get data                                                ##
    ###                                                                                             ##
    ##################################################################################################
    technicalNames = []
    technicalValues = []
    technicalCycleNb = []

    for cycle in mCycles.list :
        # Get all measurements
        for parameter in cycle.technicalParameters:
            technicalNames.append(parameter.description)
            technicalValues.append(str(parameter.technical_value))
            technicalCycleNb.append(cycle.cycleNb)

    # 2.5.3 General information on the technical data file
    putString(platformNumberVar,metadata["PLATFORM_NUMBER"],string8DimSize)
    putString(dataTypeVar,'Argo technical data',string32DimSize)
    putString(formatVersionVar,'3.1',string4DimSize)
    putString(handbookVersionVar,'1.2',string4DimSize)
    putString(dataCentreVar,metadata["DATA_CENTRE"],string2DimSize)
    putString(dateCreationVar,metadata["DATE_CREATION"],dateTimeDimSize)
    putString(dateUpdateVar,currentDate,dateTimeDimSize)

    # 2.5.4 Technical data
    cycleNumberVar[:] = technicalCycleNb
    putString(technicalParamNameVar,technicalNames,string128DimSize)
    putString(technicalParamValueVar,technicalValues,string128DimSize)
    # 2.5.4 Timeseries of technical data (optional)
    file_cdf.close()
