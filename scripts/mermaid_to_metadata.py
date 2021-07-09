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

def create_nc_metadata_3_1(FloatWmoID,mfloat_nc_path,mCycles,ms41s):
    metadataFilePath = mfloat_nc_path + FloatWmoID + "_meta.nc"
    print(metadataFilePath)
    if os.path.exists(metadataFilePath):
        os.remove(metadataFilePath)
    file_cdf = Dataset(metadataFilePath, "w", format="NETCDF3_CLASSIC")
    ##################################################################################################
    ###                                                                                             ##
    ###                                     Create Dimensions                                       ##
    ###                                                                                             ##
    ##################################################################################################
    dateTimeDim = file_cdf.createDimension('DATE_TIME', 14);
    string1024Dim = file_cdf.createDimension('STRING1024', 1024);
    string256Dim = file_cdf.createDimension('STRING256', 256);
    string64Dim = file_cdf.createDimension('STRING64', 64);
    string32Dim = file_cdf.createDimension('STRING32', 32);
    string17Dim = file_cdf.createDimension('STRING17', 17);
    string16Dim = file_cdf.createDimension('STRING16', 16);
    string8Dim = file_cdf.createDimension('STRING8', 8);
    string4Dim = file_cdf.createDimension('STRING4', 4);
    string2Dim = file_cdf.createDimension('STRING2', 2);
    nParamDim = file_cdf.createDimension('N_PARAM', ms41s.get_N_PARAMS());
    nSensorDim = file_cdf.createDimension('N_SENSOR', ms41s.get_N_PARAMS());
    nConfigParamDim = file_cdf.createDimension('N_CONFIG_PARAM', mCycles.configurationParametersNb);
    nLaunchConfigParamDim = file_cdf.createDimension('N_LAUNCH_CONFIG_PARAM', mCycles.launchParametersNb);
    nMissionDim = file_cdf.createDimension('N_MISSION',len(mCycles.missionsConfigurationParameters));
    nPositioningSystemDim = file_cdf.createDimension('N_POSITIONING_SYSTEM',1);
    ntransDim = file_cdf.createDimension('N_TRANS_SYSTEM',1);

    string2DimSize = len(string2Dim)
    string4DimSize = len(string4Dim)
    string8DimSize = len(string8Dim)
    string16DimSize = len(string16Dim)
    string17DimSize = len(string17Dim)
    string32DimSize = len(string32Dim)
    string64DimSize = len(string64Dim)
    string256DimSize = len(string256Dim)
    string1024DimSize = len(string1024Dim)
    dateTimeDimSize = len(dateTimeDim)
    nParamDimSize = len(nParamDim)
    nSensorDimSize = len(nSensorDim)
    nConfigParamDimSize = len(nConfigParamDim)
    nLaunchConfigParamDimSize = len(nLaunchConfigParamDim)
    nMissionDimSize = len(nMissionDim)
    nPositioningSystemDimSize = len(nPositioningSystemDim)
    ntransDimSize = len(ntransDim)

    ##################################################################################################
    ###                                                                                             ##
    ###                                     Create Variables                                        ##
    ###                                                                                             ##
    ##################################################################################################

    file_cdf.setncattr('title','Argo float metadata file')
    file_cdf.setncattr('institution','CORIOLIS')
    file_cdf.setncattr('source','Argo float')

    currentDate = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S");
    globalHistoryText = currentDate + ' creation; ';
    globalHistoryText += currentDate + ' last update (osean float converting raw data)'

    file_cdf.setncattr('history', globalHistoryText)
    file_cdf.setncattr('references', 'http://www.argodatamgt.org/Documentation')
    file_cdf.setncattr('user_manual_version', '3.4')
    file_cdf.setncattr('Conventions', 'Argo-3.1 CF-1.6')

    dataTypeVar = file_cdf.createVariable('DATA_TYPE','S1',('STRING16',),fill_value=' ')
    dataTypeVar.setncattr('long_name', 'Data type')
    dataTypeVar.setncattr('conventions', 'Argo reference table 1')

    formatVersionVar = file_cdf.createVariable('FORMAT_VERSION','S1',('STRING4',),fill_value=' ')
    formatVersionVar.setncattr('long_name', 'File format version')

    handbookVersionVar = file_cdf.createVariable('HANDBOOK_VERSION','S1',('STRING64',),fill_value=' ')
    handbookVersionVar.setncattr('long_name', 'Data handbook version')

    dateCreationVar = file_cdf.createVariable('DATE_CREATION','S1',('DATE_TIME',),fill_value=' ')
    dateCreationVar.setncattr('long_name', 'Date of file creation')
    dateCreationVar.setncattr('conventions', 'YYYYMMDDHHMISS')

    dateUpdateVar = file_cdf.createVariable('DATE_UPDATE','S1',('DATE_TIME',),fill_value=' ')
    dateUpdateVar.setncattr('long_name', 'Date of update of this file');
    dateUpdateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    platformNumberVar = file_cdf.createVariable('PLATFORM_NUMBER','S1',('STRING8',),fill_value=' ')
    platformNumberVar.setncattr('long_name', 'Float unique identifier');
    platformNumberVar.setncattr('conventions', 'WMO float identifier : A9IIIII');

    platformWigosIdVar = file_cdf.createVariable('PLATFORM_WIGOS_ID','S1',('STRING17',),fill_value=' ')
    platformWigosIdVar.setncattr('long_name', 'Float unique identifier');
    platformWigosIdVar.setncattr('conventions', 'WMO WIGOS float identifier: 0-22000-0-A9IIIII');

    pttVar = file_cdf.createVariable('PTT','S1',('STRING256',),fill_value=' ')
    pttVar.setncattr('long_name', 'Transmission identifier (ARGOS, ORBCOMM, etc.)');

    transSystemVar = file_cdf.createVariable('TRANS_SYSTEM','S1',('N_TRANS_SYSTEM','STRING16'),fill_value=' ')
    transSystemVar.setncattr('long_name', 'Telecommunication system used');

    tranSystemIdVar = file_cdf.createVariable('TRANS_SYSTEM','S1',('N_TRANS_SYSTEM','STRING32'),fill_value=' ')
    transSystemVar.setncattr('long_name', 'Program identifier used by the transmission system');

    transFrequencyVar = file_cdf.createVariable('TRANS_FREQUENCY','S1',('N_TRANS_SYSTEM','STRING16'),fill_value=' ')
    transFrequencyVar.setncattr('long_name', 'Frequency of transmission from the float');
    transFrequencyVar.setncattr('units', 'hertz');
