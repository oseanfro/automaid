# @Author: Frédéric Rocca <fro>
# @Date:   2023-06-09T09:36:17+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: mermaid_to_metadata.py
# @Last modified by:   fro
# @Last modified time: 2023-07-03T14:26:28+02:00

import os
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
import mermaid_to_nc_cfg as cfg
import configuration
import json

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
    string128Dim = file_cdf.createDimension('STRING128', 128);
    string64Dim = file_cdf.createDimension('STRING64', 64);
    string32Dim = file_cdf.createDimension('STRING32', 32);
    string17Dim = file_cdf.createDimension('STRING17', 17);
    string16Dim = file_cdf.createDimension('STRING16', 16);
    string8Dim = file_cdf.createDimension('STRING8', 8);
    string4Dim = file_cdf.createDimension('STRING4', 4);
    string2Dim = file_cdf.createDimension('STRING2', 2);
    nParamDim = file_cdf.createDimension('N_PARAM', ms41s.get_N_PARAMS());
    nSensorDim = file_cdf.createDimension('N_SENSORS', ms41s.get_N_PARAMS());
    nConfigParamDim = file_cdf.createDimension('N_CONFIG_PARAM', mCycles.configurationParametersNb);
    nLaunchConfigParamDim = file_cdf.createDimension('N_LAUNCH_CONFIG_PARAM', mCycles.launchingParametersNb);
    nMissionDim = file_cdf.createDimension('N_MISSIONS',mCycles.missionsNb);
    nPositioningSystemDim = file_cdf.createDimension('N_POSITIONING_SYSTEM',1);
    ntransDim = file_cdf.createDimension('N_TRANS_SYSTEM',1);

    string2DimSize = len(string2Dim)
    string4DimSize = len(string4Dim)
    string8DimSize = len(string8Dim)
    string16DimSize = len(string16Dim)
    string17DimSize = len(string17Dim)
    string32DimSize = len(string32Dim)
    string64DimSize = len(string64Dim)
    string128DimSize = len(string128Dim)
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

    handbookVersionVar = file_cdf.createVariable('HANDBOOK_VERSION','S1',('STRING4',),fill_value=' ')
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

    tranSystemIdVar = file_cdf.createVariable('TRANS_SYSTEM_ID','S1',('N_TRANS_SYSTEM','STRING32'),fill_value=' ')
    tranSystemIdVar.setncattr('long_name', 'Program identifier used by the transmission system');

    transFrequencyVar = file_cdf.createVariable('TRANS_FREQUENCY','S1',('N_TRANS_SYSTEM','STRING16'),fill_value=' ')
    transFrequencyVar.setncattr('long_name', 'Frequency of transmission from the float');
    transFrequencyVar.setncattr('units', 'hertz');

    positioningSystemVar = file_cdf.createVariable('POSITIONING_SYSTEM','S1',('N_POSITIONING_SYSTEM','STRING8'),fill_value=' ')
    positioningSystemVar.setncattr('long_name', 'Positioning system');

    plateformFamilyVar = file_cdf.createVariable('PLATEFORM_FAMILY','S1',('STRING256',),fill_value=' ')
    plateformFamilyVar.setncattr('long_name', 'Category of instrument');

    plateformTypeVar = file_cdf.createVariable('PLATFORM_TYPE','S1',('STRING32',),fill_value=' ')
    plateformTypeVar.setncattr('long_name', 'Type of float');
    plateformTypeVar.setncattr('conventions', 'Argo reference table 23');

    plateformMakerVar = file_cdf.createVariable('PLATFORM_MAKER','S1',('STRING256',),fill_value=' ')
    plateformMakerVar.setncattr('long_name', 'Name of the manufacturer');
    plateformMakerVar.setncattr('conventions', 'Argo reference table 24');

    firmwareVersionVar = file_cdf.createVariable('FIRMWARE_VERSION','S1',('STRING64',),fill_value=' ')
    firmwareVersionVar.setncattr('long_name', 'Firmware version for the float');

    manualVersionVar = file_cdf.createVariable('MANUAL_VERSION','S1',('STRING16',),fill_value=' ')
    manualVersionVar.setncattr('long_name', 'Manual version for the float');

    floatSerialNoVar = file_cdf.createVariable('FLOAT_SERIAL_NO','S1',('STRING32',),fill_value=' ')
    floatSerialNoVar.setncattr('long_name', 'Serial number of the float');

    standardFormatIdVar = file_cdf.createVariable('STANDARD_FORMAT_ID','S1',('STRING16',),fill_value=' ')
    standardFormatIdVar.setncattr('long_name', 'Standard format number to describe the data format type for each float');

    dacFormatIdVar = file_cdf.createVariable('DAC_FORMAT_ID','S1',('STRING16',),fill_value=' ')
    dacFormatIdVar.setncattr('long_name', 'Format number used by the DAC to describe the data format type for each float');

    wmoInstTypeVar = file_cdf.createVariable('WMO_INST_TYPE','S1',('STRING4',),fill_value=' ')
    wmoInstTypeVar.setncattr('long_name', 'Coded instrument type');
    wmoInstTypeVar.setncattr('conventions', 'Argo reference table 8');

    projectNameVar = file_cdf.createVariable('PROJECT_NAME','S1',('STRING64',),fill_value=' ')
    projectNameVar.setncattr('long_name', 'Program under which the float was deployed');

    dataCenterVar = file_cdf.createVariable('DATA_CENTRE','S1',('STRING2',),fill_value=' ')
    dataCenterVar.setncattr('long_name', 'Data centre in charge of float real-time processing');
    dataCenterVar.setncattr('conventions', 'Argo reference table 4"');

    piNameVar = file_cdf.createVariable('PI_NAME','S1',('STRING64',),fill_value=' ')
    piNameVar.setncattr('long_name', 'Name of the principal investigator');

    anomalyVar = file_cdf.createVariable('ANOMALY','S1',('STRING256',),fill_value=' ')
    anomalyVar.setncattr('long_name', 'Describe any anomalies or problems the float may have had');

    batteryTypeVar = file_cdf.createVariable('BATTERY_TYPE','S1',('STRING64',),fill_value=' ')
    batteryTypeVar.setncattr('long_name', 'Type of battery packs in the float');

    batteryPacksVar = file_cdf.createVariable('BATTERY_PACKS','S1',('STRING64',),fill_value=' ')
    batteryPacksVar.setncattr('long_name', 'Configuration of battery packs in the float');

    controllerBoardTypePrimaryVar = file_cdf.createVariable('CONTROLLER_BOARD_TYPE_PRIMARY','S1',('STRING32',),fill_value=' ')
    controllerBoardTypePrimaryVar.setncattr('long_name', 'Type of primary controller board');

    controllerBoardTypeSecondaryVar = file_cdf.createVariable('CONTROLLER_BOARD_TYPE_SECONDARY','S1',('STRING32',),fill_value=' ')
    controllerBoardTypeSecondaryVar.setncattr('long_name', 'Type of secondary controller board');

    controllerBoardSerialNoPrimaryVar = file_cdf.createVariable('CONTROLLER_BOARD_SERIAL_NO_PRIMARY','S1',('STRING32',),fill_value=' ')
    controllerBoardSerialNoPrimaryVar.setncattr('long_name', 'Serial number of the primary controller board');

    controllerBoardSerialNoSecondaryVar = file_cdf.createVariable('CONTROLLER_BOARD_SERIAL_NO_SECONDARY','S1',('STRING32',),fill_value=' ')
    controllerBoardSerialNoSecondaryVar.setncattr('long_name', 'Serial number of the secondary controller board');

    specialFeatureVar = file_cdf.createVariable('SPECIAL_FEATURES','S1',('STRING1024',),fill_value=' ')
    specialFeatureVar.setncattr('long_name', 'Extra features of the float (algorithms, compressee etc.)');

    floatOwnerVar = file_cdf.createVariable('FLOAT_OWNER','S1',('STRING64',),fill_value=' ')
    floatOwnerVar.setncattr('long_name', 'Float owner');

    operatingInstitutionVar = file_cdf.createVariable('OPERATING_INSTITUTION','S1',('STRING64',),fill_value=' ')
    operatingInstitutionVar.setncattr('long_name', 'Operating institution of the float');

    customisationVar = file_cdf.createVariable('CUSTOMISATION','S1',('STRING1024',),fill_value=' ')
    customisationVar.setncattr('long_name', 'Float customisation, i.e. (institution and modifications)');

    #2.4.5 Float deployment and mission information
    launchDateVar = file_cdf.createVariable('LAUNCH_DATE','S1',('DATE_TIME',),fill_value=' ')
    launchDateVar.setncattr('long_name', 'Date (UTC) of the deployment');
    launchDateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    launchLatitudeVar = file_cdf.createVariable('LAUNCH_LATITUDE','f8',fill_value=np.float64(99999.0))
    launchLatitudeVar.setncattr('long_name', 'Latitude of the float when deployed');
    launchLatitudeVar.setncattr('standard_name', 'latitude');
    launchLatitudeVar.setncattr('units', 'degree_north');
    launchLatitudeVar.setncattr('valid_min', np.float64(-90));
    launchLatitudeVar.setncattr('valid_max', np.float64(90));

    launchLongitudeVar = file_cdf.createVariable('LAUNCH_LONGITUDE','f8',fill_value=np.float64(99999.0))
    launchLongitudeVar.setncattr('long_name', 'Longitude of the float when deployed');
    launchLongitudeVar.setncattr('standard_name', 'longitude');
    launchLongitudeVar.setncattr('units', 'degree_east');
    launchLongitudeVar.setncattr('valid_min', np.float64(-180));
    launchLongitudeVar.setncattr('valid_max', np.float64(180));

    launchQcVar = file_cdf.createVariable('LAUNCH_QC','S1',fill_value=' ')
    launchQcVar.setncattr('long_name', 'Quality on launch date, time and location');
    launchQcVar.setncattr('conventions', 'Argo reference table 2');

    startDateVar = file_cdf.createVariable('START_DATE','S1',('DATE_TIME',),fill_value=' ')
    startDateVar.setncattr('long_name', 'Date (UTC) of the first descent of the float');
    startDateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    startDateQcVar = file_cdf.createVariable('START_DATE_QC','S1',fill_value=' ')
    startDateQcVar.setncattr('long_name', 'Quality on start date');
    startDateQcVar.setncattr('conventions', 'Argo reference table 2');

    startUpDateVar = file_cdf.createVariable('STARTUP_DATE','S1',('DATE_TIME',),fill_value=' ')
    startUpDateVar.setncattr('long_name', 'Date (UTC) of the activation of the float');
    startUpDateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    startUpDateQcVar = file_cdf.createVariable('STARTUP_DATE_QC','S1',fill_value=' ')
    startUpDateQcVar.setncattr('long_name', 'Quality on startup date');
    startUpDateQcVar.setncattr('conventions', 'Argo reference table 2');

    deployementPlateformVar = file_cdf.createVariable('DEPLOYEMENT_PLATEFORM','S1',('STRING32',),fill_value=' ')
    deployementPlateformVar.setncattr('long_name', 'Identifier of the deployment platform');

    deployementCruiseIdVar = file_cdf.createVariable('DEPLOYEMENT_CRUISE_ID','S1',('STRING32',),fill_value=' ')
    deployementCruiseIdVar.setncattr('long_name', 'Identification number or reference number of the cruise used to deploy the float');

    deployementReferenceStationIdVar = file_cdf.createVariable('DEPLOYEMENT_REFERENCE_STATION_ID','S1',('STRING256',),fill_value=' ')
    deployementReferenceStationIdVar.setncattr('long_name', 'Identifier or reference number of co-located stations used to verify the first profile');

    endMissionDateVar = file_cdf.createVariable('END_MISSION_DATE','S1',('DATE_TIME',),fill_value=' ')
    endMissionDateVar.setncattr('long_name', 'Date (UTC) of the end of mission of the float');
    endMissionDateVar.setncattr('conventions', 'YYYYMMDDHHMISS');

    endMissionStatusVar = file_cdf.createVariable('END_MISSION_STATUS','S1',fill_value=' ')
    endMissionStatusVar.setncattr('long_name', 'Status of the end of mission of the float');
    endMissionStatusVar.setncattr('conventions', 'T:No more transmission received, R:Retrieved');

    #2.4.6 Configuration parameters
    launchConfigParameterNameVar = file_cdf.createVariable('LAUNCH_CONFIG_PARAMETER_NAME','S1',('N_LAUNCH_CONFIG_PARAM','STRING128'),fill_value=' ')
    launchConfigParameterNameVar.setncattr('long_name', 'Name of configuration parameter at launch');

    launchConfigParameterValueVar = file_cdf.createVariable('LAUNCH_CONFIG_PARAMETER_VALUE','f4',('N_LAUNCH_CONFIG_PARAM',),fill_value=np.float32(99999.0))
    launchConfigParameterValueVar.setncattr('long_name', 'Value of configuration parameter at launch');

    configParameterNameVar = file_cdf.createVariable('CONFIG_PARAMETER_NAME','S1',('N_CONFIG_PARAM','STRING128'),fill_value=' ')
    configParameterNameVar.setncattr('long_name', 'Name of configuration parameter');

    configParameterValueVar = file_cdf.createVariable('CONFIG_PARAMETER_VALUE','f4',('N_MISSIONS','N_CONFIG_PARAM'),fill_value=np.float32(99999.0))
    configParameterValueVar.setncattr('long_name', 'Value of configuration parameter');

    configMissionNumberVar = file_cdf.createVariable('CONFIG_MISSION_NUMBER','i4',('N_MISSIONS',),fill_value=np.int32(99999))
    configMissionNumberVar.setncattr('long_name', 'Unique number denoting the missions performed by the float');
    configMissionNumberVar.setncattr('conventions', '1...N, 1 : first complete mission');

    configMissionCommentVar = file_cdf.createVariable('CONFIG_MISSION_COMMENT','S1',('N_MISSIONS','STRING256'),fill_value=' ')
    configMissionCommentVar.setncattr('long_name', 'Comment on configuration');

    #2.4.7.1 Float sensor information
    sensorVar = file_cdf.createVariable('SENSOR','S1',('N_SENSORS','STRING32'),fill_value=' ')
    sensorVar.setncattr('long_name', 'Name of the sensor mounted on the float');
    sensorVar.setncattr('conventions', 'Argo reference table 25');

    sensorMakerVar = file_cdf.createVariable('SENSOR_MAKER','S1',('N_SENSORS','STRING256'),fill_value=' ')
    sensorMakerVar.setncattr('long_name', 'Name of the sensor manufacturer');
    sensorMakerVar.setncattr('conventions', 'Argo reference table 26');

    sensorModelVar = file_cdf.createVariable('SENSOR_MODEL','S1',('N_SENSORS','STRING256'),fill_value=' ')
    sensorModelVar.setncattr('long_name', 'Type of sensor');
    sensorModelVar.setncattr('conventions', 'Argo reference table 27');

    sensorSerialNoVar = file_cdf.createVariable('SENSOR_SERIAL_NO','S1',('N_SENSORS','STRING16'),fill_value=' ')
    sensorSerialNoVar.setncattr('long_name', 'Serial number of sensor');

    #2.4.7.2 Float parameter information
    parameterVar = file_cdf.createVariable('PARAMETER','S1',('N_PARAM','STRING64'),fill_value=' ')
    parameterVar.setncattr('long_name', 'Name of parameter computed from float measurements');
    parameterVar.setncattr('conventions', 'Argo reference table 3');

    parameterSensorVar = file_cdf.createVariable('PARAMETER_SENSOR','S1',('N_PARAM','STRING128'),fill_value=' ')
    parameterSensorVar.setncattr('long_name', 'Name of parameter computed from float measurements');
    parameterSensorVar.setncattr('conventions', 'Argo reference table 25');

    parameterUnitsVar = file_cdf.createVariable('PARAMETER_UNITS','S1',('N_PARAM','STRING32'),fill_value=' ')
    parameterUnitsVar.setncattr('long_name', 'Units of accuracy and resolution of the parameter');

    parameterAccuracyVar = file_cdf.createVariable('PARAMETER_ACCURACY','S1',('N_PARAM','STRING32'),fill_value=' ')
    parameterAccuracyVar.setncattr('long_name', 'Accuracy of the parameter');

    parameterresolutionVar = file_cdf.createVariable('PARAMETER_RESOLUTION','S1',('N_PARAM','STRING32'),fill_value=' ')
    parameterresolutionVar.setncattr('long_name', 'Resolution of the parameter');
    #2.4.8 Float calibration information

    predeployementCalibEquationVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_EQUATION','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeployementCalibEquationVar.setncattr('long_name', 'Calibration equation for this parameter');

    predeployementCalibCoefficientVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_COEFFICIENT','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeployementCalibCoefficientVar.setncattr('long_name', 'Calibration coefficients for this equation');

    predeployementCalibCommentVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_COMMENT','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeployementCalibCommentVar.setncattr('long_name', 'Comment applying to this parameter calibration');

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
    if len(softVersions) > 1 :
        print("!!!!!!!!!!!!!!!!!!!!! No unique software version !!!!!!!!!!!!!!!!!")
        file_cdf.close()
        return
    softVersion = softVersions[0]

    launchConfigParameterName = []
    launchConfigParameterValue = []
    configParameterName = []
    configParameterValue = []
    configMissionNumber =[]
    configMissionComment = []
    #launch parameters never change
    for parameter in mCycles.launchingParameters.list:
        launchConfigParameterName.append(parameter.name)
        launchConfigParameterValue.append(parameter.value)

    for parameter in mCycles.missions[-1].configurationParameters.list:
        configParameterName.append(parameter.name)

    commentFilePath = mfloat_nc_path  + "configMissionComment.json"
    if os.path.exists(commentFilePath):
        with open(commentFilePath,"r") as f:
            configMissionComment = json.loads(f.read())
    retreiveComments = True
    if len(configMissionComment) > 0 :
        retreiveComments = False

    for mission in mCycles.missions :
        if mission.missionNumber > 0 :
            missionParametersNames = []
            missionParametersValues = []
            configMissionNumber.append(mission.missionNumber)
            if retreiveComments :
                print(mission.missionNumber)
                print(mission.configurationParameters)
                comment = input("give comment on this mission\r\n")
                if comment != "" :
                    while (len(comment) > 256) :
                        print("!!!!!!!!!!!!!string is too long!!!!!!!!!!!!!!!!!")
                        print(mission.missionNumber)
                        print(mission.configurationParameters)
                        comment = input("give comment on this mission\r\n")
                    configMissionComment.append(comment)

            for parameter in mission.configurationParameters.list:
                missionParametersNames.append(parameter.name)
                missionParametersValues.append(parameter.value)
            configParameterValue.append(missionParametersValues)

    with open(commentFilePath,"w") as f:
        f.write(json.dumps(configMissionComment))



    ##################################################################################################
    ###                                                                                             ##
    ###                                     Load data                                               ##
    ###                                                                                             ##
    ##################################################################################################

    #2.4.3 General information on the metadata file
    putString(dataTypeVar,'Argo meta-data',string16DimSize)
    putString(formatVersionVar,'3.1',string4DimSize)
    putString(handbookVersionVar,'1.2',string4DimSize)
    putString(dateCreationVar,currentDate,dateTimeDimSize)
    putString(dateUpdateVar,currentDate,dateTimeDimSize)

    #2.4.4 Float characteristics
    putString(platformNumberVar,'A9IIIII',string8DimSize)
    putString(platformWigosIdVar,'0-22000-0-A9IIIII',string17DimSize)
    # numéro de SIM ?????
    putString(pttVar,'512424',string256DimSize)
    putNString(transSystemVar,'IRIDIUM',ntransDimSize,string16DimSize)
    putNString(tranSystemIdVar,'n/a',ntransDimSize,string32DimSize)
    putNString(transFrequencyVar,'n/a',ntransDimSize,string16DimSize)
    putNString(positioningSystemVar,'GPS',nPositioningSystemDimSize,string8DimSize)
    putString(plateformFamilyVar,'FLOAT',string256DimSize)
    putString(plateformTypeVar,'999',string32DimSize)
    putString(plateformMakerVar,'OSEAN',string256DimSize)
    putString(firmwareVersionVar,softVersion,string64DimSize)
    putString(manualVersionVar,'452000852V02',string16DimSize)
    putString(floatSerialNoVar,floatSerial,string32DimSize)
    putString(wmoInstTypeVar,'999',string4DimSize)
    putString(projectNameVar,'ARGOMermaid',string64DimSize)
    putString(dataCenterVar,cfg.history_institution,string2DimSize)
    putString(piNameVar,'Frederic Rocca',string64DimSize)
    putString(batteryTypeVar,'ELECTROCHEM Lithium 15V',string64DimSize)
    putString(controllerBoardTypePrimaryVar,'MERMAID_PILOT',string32DimSize)
    putString(controllerBoardSerialNoPrimaryVar,'452.020-P-0051',string32DimSize)
    putString(floatOwnerVar,'OSEAN',string64DimSize)
    putString(operatingInstitutionVar,'OSEAN',string64DimSize)

    #2.4.5 Float deployment and mission information
    putString(launchDateVar,'20200708070435',dateTimeDimSize)
    launchLatitudeVar[:] = np.float64(43.3899500)
    launchLongitudeVar[:] = np.float64(7.8623500)
    launchQcVar[:] = '0'
    putString(startDateVar,'20200708123857',dateTimeDimSize)
    startDateQcVar[:] = '0'
    putString(startUpDateVar,'20200708065659',dateTimeDimSize)
    startUpDateQcVar[:] = '0'
    putString(deployementPlateformVar,'n/a',string32DimSize)
    putString(deployementCruiseIdVar,'n/a',string32DimSize)
    putString(deployementReferenceStationIdVar,'n/a',string256DimSize)
    putString(endMissionDateVar,'20201106083949',dateTimeDimSize)
    endMissionStatusVar[:] = 'R'

    #2.4.6 Configuration parameters
    putStringArray(launchConfigParameterNameVar,launchConfigParameterName,string128DimSize)
    launchConfigParameterValueVar[:] = launchConfigParameterValue
    putStringArray(configParameterNameVar,configParameterName,string128DimSize)
    configParameterValueVar[:] = configParameterValue
    configMissionNumberVar[:] = configMissionNumber
    putStringArray(configMissionCommentVar,configMissionComment,string256DimSize)

    #2.4.7 float sensor and parameter information
    putStringArray(sensorVar,["CTD_PRES","CTD_TEMP","CTD_CNDC"],string32DimSize)
    putStringArray(sensorMakerVar,["SBE","SBE","SBE"],string256DimSize)
    putStringArray(sensorModelVar,["SBE41CP_V7.2.5","SBE41CP_V7.2.5","SBE41CP_V7.2.5"],string256DimSize)
    putStringArray(sensorSerialNoVar,["09396","09396","09396"],string16DimSize)
    putStringArray(parameterVar,param_names,string64DimSize)
    putStringArray(parameterSensorVar,["CTD_PRES","CTD_TEMP","CTD_CNDC"],string128DimSize)
    putStringArray(parameterUnitsVar,["decibar","degree","psu"],string32DimSize)
    putStringArray(parameterAccuracyVar,["2","0.002","0.005"],string32DimSize)
    putStringArray(parameterresolutionVar,["1","0.001","0.001"],string32DimSize)
    putStringArray(predeployementCalibEquationVar,["none","none","none"],string1024DimSize)
    putStringArray(predeployementCalibCoefficientVar,["none","none","none"],string1024DimSize)

    file_cdf.close()
