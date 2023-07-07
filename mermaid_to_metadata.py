# @Author: Frédéric Rocca <fro>
# @Date:   2023-06-09T09:36:17+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: mermaid_to_metadata.py
# @Last modified by:   fro
# @Last modified time: 2023-07-07T12:15:26+02:00

import os
import json
import shutil
import sys
import glob
import re
from obspy import UTCDateTime
from netCDF4 import Dataset
from netCDF4 import stringtochar
from datetime import datetime,timezone
import numpy as np

try:
    import configuration
    import utils
    import argo_metadata
    import decrypt
    import dives
    import events
except:
    import automaid.configuration as configuration
    import automaid.utils as utils
    import automaid.argo_metadata as argo_metadata
    import automaid.decrypt as decrypt
    import automaid.dives as dives
    import automaid.events as events

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

def create_nc_metadata_3_1(FloatWmoID,mfloat_nc_path,mCycles,metadata):
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
    nParamDim = file_cdf.createDimension('N_PARAM', len(metadata["PARAMETERS"]));
    nSensorDim = file_cdf.createDimension('N_SENSORS', len(metadata["SENSORS"]));
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
    globalHistoryText = metadata["DATE_CREATION"] + ' creation; ';
    globalHistoryText += currentDate + ' last update (osean float converting raw data)'

    file_cdf.setncattr('history', globalHistoryText)
    file_cdf.setncattr('references', 'http://www.argodatamgt.org/Documentation')
    file_cdf.setncattr('user_manual_version', '3.41.1')
    file_cdf.setncattr('Conventions', 'Argo-3.1 CF-1.6')

    dataTypeVar = file_cdf.createVariable('DATA_TYPE','S1',('STRING32',),fill_value=' ')
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

    platformFamilyVar = file_cdf.createVariable('PLATFORM_FAMILY','S1',('STRING256',),fill_value=' ')
    platformFamilyVar.setncattr('long_name', 'Category of instrument');

    platformTypeVar = file_cdf.createVariable('PLATFORM_TYPE','S1',('STRING32',),fill_value=' ')
    platformTypeVar.setncattr('long_name', 'Type of float');
    platformTypeVar.setncattr('conventions', 'Argo reference table 23');

    platformMakerVar = file_cdf.createVariable('PLATFORM_MAKER','S1',('STRING256',),fill_value=' ')
    platformMakerVar.setncattr('long_name', 'Name of the manufacturer');
    platformMakerVar.setncattr('conventions', 'Argo reference table 24');

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

    deploymentPlatformVar = file_cdf.createVariable('DEPLOYMENT_PLATFORM','S1',('STRING32',),fill_value=' ')
    deploymentPlatformVar.setncattr('long_name', 'Identifier of the deployment platform');

    deploymentCruiseIdVar = file_cdf.createVariable('DEPLOYMENT_CRUISE_ID','S1',('STRING32',),fill_value=' ')
    deploymentCruiseIdVar.setncattr('long_name', 'Identification number or reference number of the cruise used to deploy the float');

    deploymentReferenceStationIdVar = file_cdf.createVariable('DEPLOYMENT_REFERENCE_STATION_ID','S1',('STRING256',),fill_value=' ')
    deploymentReferenceStationIdVar.setncattr('long_name', 'Identifier or reference number of co-located stations used to verify the first profile');

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

    predeploymentCalibEquationVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_EQUATION','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeploymentCalibEquationVar.setncattr('long_name', 'Calibration equation for this parameter');

    predeploymentCalibCoefficientVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_COEFFICIENT','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeploymentCalibCoefficientVar.setncattr('long_name', 'Calibration coefficients for this equation');

    predeploymentCalibCommentVar = file_cdf.createVariable('PREDEPLOYMENT_CALIB_COMMENT','S1',('N_PARAM','STRING1024'),fill_value=' ')
    predeploymentCalibCommentVar.setncattr('long_name', 'Comment applying to this parameter calibration');

    ##################################################################################################
    ###                                                                                             ##
    ###                                     Get data                                                ##
    ###                                                                                             ##
    ##################################################################################################
    # Profile data
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
    for mission in mCycles.missions :
        if mission.missionNumber > 0 :
            missionParametersValues = []
            configMissionNumber.append(mission.missionNumber)
            for parameter in mission.configurationParameters.list:
                missionParametersValues.append(parameter.value)
            configParameterValue.append(missionParametersValues)
    missions = []
    for mission in mCycles.missions:
        if mission.missionNumber > 0 :
            mission_params = {}
            for parameter in mission.configurationParameters.list:
                if parameter.value:
                    mission_params.setdefault(parameter.name,str(parameter.value))
                else :
                    mission_params.setdefault(parameter.name,"---")
            mission_params["comment"] = ""
            mission_params["id"] = str(mission.missionNumber)
            missions.append(mission_params)

    if "MISSIONS" in metadata:
        for meta_mission in metadata["MISSIONS"]:
            for mission in missions:
                if meta_mission['id'] == mission['id']:
                    mission['comment'] = meta_mission['comment']

    metadata["MISSIONS"] = missions
    json_object = json.dumps(metadata, indent=4)

    metadata_file_path = os.path.join(mfloat_nc_path, "metadata.json")
    # Writing to metadata.json
    with open(metadata_file_path, "w") as outfile:
        outfile.write(json_object)
    ##################################################################################################
    ###                                                                                             ##
    ###                                     Load data                                               ##
    ###                                                                                             ##
    ##################################################################################################

    #2.4.3 General information on the metadata file
    putString(dataTypeVar,'Argo meta-data',string32DimSize)
    putString(formatVersionVar,'3.1',string4DimSize)
    putString(handbookVersionVar,'1.2',string4DimSize)
    putString(dateCreationVar,metadata["DATE_CREATION"],dateTimeDimSize)
    putString(dateUpdateVar,currentDate,dateTimeDimSize)

    #2.4.4 Float characteristics
    putString(platformNumberVar,metadata["PLATFORM_NUMBER"],string8DimSize)
    putString(platformWigosIdVar,metadata["PLATFORM_WIGOS_ID"],string17DimSize)
    # numéro de SIM ?????
    putString(pttVar,metadata["PTT"],string256DimSize)
    putNString(transSystemVar,metadata["TRANS_SYSTEM"],ntransDimSize,string16DimSize)
    putNString(tranSystemIdVar,metadata["TRANS_SYSTEM_ID"],ntransDimSize,string32DimSize)
    putNString(transFrequencyVar,metadata["TRANS_FREQUENCY"],ntransDimSize,string16DimSize)
    putNString(positioningSystemVar,metadata["POSITIONING_SYSTEM"],nPositioningSystemDimSize,string8DimSize)
    putString(platformFamilyVar,metadata["PLATFORM_FAMILY"],string256DimSize)
    putString(platformTypeVar,metadata["PLATFORM_TYPE"],string32DimSize)
    putString(platformMakerVar,metadata["PLATFORM_MAKER"],string256DimSize)
    putString(firmwareVersionVar,softVersion,string64DimSize)
    putString(manualVersionVar,metadata["MANUAL_VERSION"],string16DimSize)
    putString(floatSerialNoVar,floatSerial,string32DimSize)
    putString(standardFormatIdVar,metadata["STANDARD_FORMAT_ID"],string16DimSize)
    putString(dacFormatIdVar,metadata["DAC_FORMAT_ID"],string16DimSize)
    putString(wmoInstTypeVar,metadata["WMO_INST_TYPE"],string4DimSize)
    putString(projectNameVar,metadata["PROJECT_NAME"],string64DimSize)
    putString(dataCenterVar,metadata["DATA_CENTRE"],string2DimSize)
    putString(piNameVar,metadata["PI_NAME"],string64DimSize)
    putString(anomalyVar,metadata["ANOMALY"],string256DimSize)
    putString(batteryTypeVar,metadata["BATTERY_TYPE"],string64DimSize)
    putString(batteryPacksVar,metadata["BATTERY_PACKS"],string64DimSize)
    putString(controllerBoardTypePrimaryVar,metadata["CONTROLLER_BOARD_TYPE_PRIMARY"],string32DimSize)
    putString(controllerBoardSerialNoPrimaryVar,metadata["CONTROLLER_BOARD_SERIAL_NO_PRIMARY"],string32DimSize)
    putString(specialFeatureVar,metadata["SPECIAL_FEATURES"],string1024DimSize)
    putString(floatOwnerVar,metadata["FLOAT_OWNER"],string64DimSize)
    putString(operatingInstitutionVar,metadata["OPERATING_INSTITUTION"],string64DimSize)
    putString(customisationVar,metadata["CUSTOMISATION"],string1024DimSize)

    #2.4.5 Float deployment and mission information
    putString(launchDateVar,metadata["LAUNCH_DATE"],dateTimeDimSize)
    launchLatitudeVar[:] = np.float64(metadata["LAUNCH_LATITUDE"])
    launchLongitudeVar[:] = np.float64(metadata["LAUNCH_LONGITUDE"])
    launchQcVar[:] = metadata["LAUNCH_QC"]
    putString(startDateVar,metadata["START_DATE"],dateTimeDimSize)
    startDateQcVar[:] = metadata["START_DATE_QC"]
    putString(startUpDateVar,metadata["STARTUP_DATE"],dateTimeDimSize)
    startUpDateQcVar[:] = metadata["STARTUP_DATE_QC"]
    putString(deploymentPlatformVar,metadata["DEPLOYMENT_PLATFORM"],string32DimSize)
    putString(deploymentCruiseIdVar,metadata["DEPLOYMENT_CRUISE_ID"],string32DimSize)
    putString(deploymentReferenceStationIdVar,metadata["DEPLOYMENT_REFERENCE_STATION_ID"],string256DimSize)
    putString(endMissionDateVar,metadata["END_MISSION_DATE"],dateTimeDimSize)
    endMissionStatusVar[:] = metadata["END_MISSION_STATUS"]

    #2.4.6 Configuration parameters

    comment_list = []
    for meta_mission in metadata["MISSIONS"]:
        comment_list.append(meta_mission["comment"])

    putStringArray(launchConfigParameterNameVar,launchConfigParameterName,string128DimSize)
    launchConfigParameterValueVar[:] = launchConfigParameterValue
    putStringArray(configParameterNameVar,configParameterName,string128DimSize)
    configParameterValueVar[:] = configParameterValue
    configMissionNumberVar[:] = configMissionNumber
    putStringArray(configMissionCommentVar,comment_list,string256DimSize)

    #2.4.7 float sensor and parameter information

    sensor_list = []
    sensor_maker_list = []
    sensor_model_list = []
    sensor_serialno_list = []
    for meta_sensor in metadata["SENSORS"]:
        sensor_list.append(meta_sensor["SENSOR"])
        sensor_maker_list.append(meta_sensor["SENSOR_MAKER"])
        sensor_model_list.append(meta_sensor["SENSOR_MODEL"])
        sensor_serialno_list.append(meta_sensor["SENSOR_SERIAL_NO"])


    putStringArray(sensorVar,sensor_list,string32DimSize)
    putStringArray(sensorMakerVar,sensor_maker_list,string256DimSize)
    putStringArray(sensorModelVar,sensor_model_list,string256DimSize)
    putStringArray(sensorSerialNoVar,sensor_serialno_list,string16DimSize)

    params_list = []
    params_sensor_list = []
    params_units_list = []
    params_accuracy_list = []
    params_resolution_list = []
    params_pre_calib_eq_list = []
    params_pre_calib_coeff_list = []
    params_pre_calib_comment_list = []
    for meta_params in metadata["PARAMETERS"]:
        params_list.append(meta_params["PARAM_NAME"])
        params_sensor_list.append(meta_params["PARAMETER_SENSOR"])
        params_units_list.append(meta_params["PARAMETER_UNITS"])
        params_accuracy_list.append(meta_params["PARAMETER_ACCURACY"])
        params_resolution_list.append(meta_params["PARAMETER_RESOLUTION"])
        params_pre_calib_eq_list.append(meta_params["PREDEPLOYMENT_CALIB_EQUATION"])
        params_pre_calib_coeff_list.append(meta_params["PREDEPLOYMENT_CALIB_COEFFICIENT"])
        params_pre_calib_comment_list.append(meta_params["PREDEPLOYMENT_CALIB_COMMENT"])

    putStringArray(parameterVar,params_list,string64DimSize)
    putStringArray(parameterSensorVar,params_sensor_list,string128DimSize)
    putStringArray(parameterUnitsVar,params_units_list,string32DimSize)
    putStringArray(parameterAccuracyVar,params_accuracy_list,string32DimSize)
    putStringArray(parameterresolutionVar,params_resolution_list,string32DimSize)
    putStringArray(predeploymentCalibEquationVar,params_pre_calib_eq_list,string1024DimSize)
    putStringArray(predeploymentCalibCoefficientVar,params_pre_calib_coeff_list,string1024DimSize)
    putStringArray(predeploymentCalibCommentVar,params_pre_calib_comment_list,string1024DimSize)

    file_cdf.close()
