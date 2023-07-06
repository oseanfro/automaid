# @Author: Frédéric Rocca <fro>
# @Date:   2023-07-05T09:32:38+02:00
# @Email:  frederic.rocca@osean.fr
# @Filename: argo_metadata.py
# @Last modified by:   fro
# @Last modified time: 2023-07-06T14:31:39+02:00

import json
import os
from datetime import datetime,timezone

def generate(path):
    metadata = {}
    currentDate = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S");

    metadata["DATE_CREATION"] = currentDate
    metadata["PLATFORM_NUMBER"] = "A9IIIII"
    metadata["PLATFORM_WIGOS_ID"] = "0-22000-0-A9IIIII"
    metadata["PTT"] = "512424"
    metadata["TRANS_SYSTEM"] = "IRIDIUM"
    metadata["TRANS_SYSTEM_ID"] = "N/A"
    metadata["TRANS_FREQUENCY"] = "N/A"
    metadata["POSITIONING_SYSTEM"] = "GPS"
    metadata["PLATFORM_FAMILY"]= "FLOAT_DEEP"
    metadata["PLATFORM_TYPE"] = "MOBY"
    metadata["PLATFORM_MAKER"] = "OSEAN"
    metadata["MANUAL_VERSION"] = "467.000.852V00"
    metadata["STANDARD_FORMAT_ID"] = "999999"
    metadata["DAC_FORMAT_ID"] = "FF"
    metadata["WMO_INST_TYPE"] = "999"
    metadata["PROJECT_NAME"] = "ARGO Mermaid"
    metadata["DATA_CENTRE"] = "JM"
    metadata["PI_NAME"] = ""
    metadata["ANOMALY"] = ""
    metadata["BATTERY_TYPE"] = "ELECTROCHEM Lithium 15V"
    metadata["BATTERY_PACKS"] = "2DD Li"
    metadata["CONTROLLER_BOARD_TYPE_PRIMARY"] = ""
    metadata["CONTROLLER_BOARD_SERIAL_NO_PRIMARY"] = ""
    metadata["SPECIAL_FEATURES"]= "Seismic detection (mermaid)"
    metadata["FLOAT_OWNER"]= ""
    metadata["OPERATING_INSTITUTION"]= ""
    metadata["CUSTOMISATION"] = ""
    metadata["LAUNCH_DATE"] = "YYYYMMDDHHMISS"
    metadata["LAUNCH_LATITUDE"] = "44.4991"
    metadata["LAUNCH_LONGITUDE"] = "16.7222"
    metadata["LAUNCH_QC"] = "0"
    metadata["START_DATE"] = "YYYYMMDDHHMISS"
    metadata["START_DATE_QC"]= "0"
    metadata["STARTUP_DATE"] = "YYYYMMDDHHMISS"
    metadata["STARTUP_DATE_QC"] = "0"
    metadata["DEPLOYMENT_PLATFORM"] = ""
    metadata["DEPLOYMENT_CRUISE_ID"] = ""
    metadata["DEPLOYMENT_REFERENCE_STATION_ID"] = ""
    metadata["END_MISSION_DATE"] = ""
    metadata["END_MISSION_STATUS"] = ""
    metadata["SENSORS"] = []
    # sensor_nb = input("How many sensor is embedded on the float ?\r\n")
    sensor_nb = 3
    for x in range(int(sensor_nb)):
        sensor = {}
        if x == 0 :
            sensor["SENSOR"] = "CTD_PRES"
            sensor["SENSOR_MAKER"]= "SBE"
            sensor["SENSOR_MODEL"] = "SBE61_V5.0.3"
            sensor["SENSOR_SERIAL_NO"]= ""
        elif x == 1 :
            sensor["SENSOR"] = "CTD_TEMP"
            sensor["SENSOR_MAKER"] = "SBE"
            sensor["SENSOR_MODEL"] = "SBE61_V5.0.3"
            sensor["SENSOR_SERIAL_NO"] = ""
        elif x == 2 :
            sensor["SENSOR"] = "CTD_CNDC"
            sensor["SENSOR_MAKER"] = "SBE"
            sensor["SENSOR_MODEL"] = "SBE61_V5.0.3"
            sensor["SENSOR_SERIAL_NO"] = ""
        else :
            sensor["SENSOR"] = ""
            sensor["SENSOR_MAKER"] = ""
            sensor["SENSOR_MODEL"] = ""
            sensor["SENSOR_SERIAL_NO"] = ""
        metadata["SENSORS"].append(sensor)

    metadata["PARAMETERS"] = []
    #parameters_nb = input("How many paramaters are mesured by the float ?\r\n")
    parameters_nb = 3
    for x in range(int(parameters_nb)):
        parameter = {}
        if x == 0 :
            parameter["PARAM_NAME"] = "PRES"
            parameter["LONG_NAME"] = "Sea water pressure, equals 0 at sea-level"
            parameter["STANDARD_NAME"] = "sea_water_pressure"
            parameter["NC_TYPE"] = "f4"
            parameter["FILL_VALUE"] = "99999.0"
            parameter["VALID_MIN"] = "0.0"
            parameter["VALID_MAX"] = "12000.0"
            parameter["C_FORMAT"] = "%5.1f"
            parameter["FORTRAN_FORMAT"] = "F5.1"
            parameter["AXIS"] = "X"
            parameter["PARAMETER_SENSOR"] = "CTD_PRES"
            parameter["PARAMETER_UNITS"] = "decibar"
            parameter["PARAMETER_ACCURACY"] = ""
            parameter["PARAMETER_RESOLUTION"] = "0.1"
            parameter["PREDEPLOYMENT_CALIB_EQUATION"] = ""
            parameter["PREDEPLOYMENT_CALIB_COEFFICIENT"] = ""
            parameter["PREDEPLOYMENT_CALIB_COMMENT"] = ""
        elif x == 1 :
            parameter["PARAM_NAME"] = "TEMP"
            parameter["LONG_NAME"] = "Sea temperature in-situ ITS-90 scale"
            parameter["STANDARD_NAME"] = "sea_water_temperature"
            parameter["NC_TYPE"] = "f4"
            parameter["FILL_VALUE"] = "99999.0"
            parameter["VALID_MIN"] = "-2.5"
            parameter["VALID_MAX"] = "40.0"
            parameter["C_FORMAT"] = "%3.4f"
            parameter["FORTRAN_FORMAT"] = "F3.4"
            parameter["AXIS"] = "Y"
            parameter["PARAMETER_SENSOR"] = "CTD_TEMP"
            parameter["PARAMETER_UNITS"] = "degree_Celsius"
            parameter["PARAMETER_ACCURACY"] = ""
            parameter["PARAMETER_RESOLUTION"] = "0.0001"
            parameter["PREDEPLOYMENT_CALIB_EQUATION"] = ""
            parameter["PREDEPLOYMENT_CALIB_COEFFICIENT"] = ""
            parameter["PREDEPLOYMENT_CALIB_COMMENT"] = ""
        elif x == 2 :
            parameter["PARAM_NAME"] = "PSAL"
            parameter["LONG_NAME"] = "Practical salinity"
            parameter["STANDARD_NAME"] = "sea_water_salinity"
            parameter["NC_TYPE"] = "f4"
            parameter["FILL_VALUE"] = "99999.0"
            parameter["VALID_MIN"] = "2.0"
            parameter["VALID_MAX"] = "41.0"
            parameter["C_FORMAT"] = "%3.4f"
            parameter["FORTRAN_FORMAT"] = "F3.4"
            parameter["AXIS"] = "Y"
            parameter["PARAMETER_SENSOR"] = "CTD_CNDC"
            parameter["PARAMETER_UNITS"] = "psu"
            parameter["PARAMETER_ACCURACY"] = ""
            parameter["PARAMETER_RESOLUTION"] = "0.0001"
            parameter["PREDEPLOYMENT_CALIB_EQUATION"] = ""
            parameter["PREDEPLOYMENT_CALIB_COEFFICIENT"] = ""
            parameter["PREDEPLOYMENT_CALIB_COMMENT"] = ""
        else :
            parameter["PARAM_NAME"] = ""
            parameter["LONG_NAME"] = ""
            parameter["STANDARD_NAME"] = ""
            parameter["NC_TYPE"] = ""
            parameter["FILL_VALUE"] = ""
            parameter["UNITS"] = ""
            parameter["VALID_MIN"] = ""
            parameter["VALID_MAX"] = ""
            parameter["C_FORMAT"] = ""
            parameter["FORTRAN_FORMAT"] = ""
            parameter["RESOLUTION"] = ""
            parameter["AXIS"] = ""
            parameter["PARAMETER_SENSOR"] = ""
            parameter["PARAMETER_UNITS"] = ""
            parameter["PARAMETER_ACCURACY"] = ""
            parameter["PARAMETER_RESOLUTION"] = ""
            parameter["PREDEPLOYMENT_CALIB_EQUATION"] = ""
            parameter["PREDEPLOYMENT_CALIB_COEFFICIENT"] = ""
            parameter["PREDEPLOYMENT_CALIB_COMMENT"] = ""

        metadata["PARAMETERS"].append(parameter)

    # Serializing json
    json_object = json.dumps(metadata, indent=4)
    # Writing to metadata.json
    with open(path, "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    generate("./metadata.json")
