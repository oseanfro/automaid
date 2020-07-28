import os
import shutil
from string import maketrans
import sys
import glob
import json
import re
import time
from bitarray import bitarray

def _byte2int(list,reversed):
    if reversed:
        list.reverse()
    return int("".join(list),16)
def _byte2hex(list,reversed):
    if reversed:
        list.reverse()
    return "".join(list)

def main(argv):
    #if(len(argv) < 3):
        #sys.exit("not enough argument, need to call script with: python decrypt.py inputpathfile outputpathfile decryptcardpath")
    inputpathfile = argv[0]
    index = 0
    argumentindex = 0
    logs = []
    dict = {"id":[],"timestamp":[],"info":{"string":"","arguments":"","type":"","unused":""},"data":{}}

    #parse data
    with open(inputpathfile, "rb") as f:
        byte = f.read(1)
        while byte != "":
            if(index < 4):
                dict["id"].append(byte.encode('hex'))
            elif(index < 8):
                dict["timestamp"].append(byte.encode('hex'))
            elif(index < 9):
                binaryinfo = "{0:08b}".format(int(byte.encode('hex'),16))
                dict["info"]["string"] = binaryinfo[-1]
                dict["info"]["arguments"] = binaryinfo[-2]
                dict["info"]["type"] = "".join(reversed(binaryinfo[-4:-2]))
                dict["info"]["unused"] = "".join(reversed(binaryinfo[-8:-4]))
            elif(dict["info"]["string"] != "" and dict["info"]["arguments"] != ""):
                if(dict["info"]["string"] == "1" and dict["info"]["arguments"] == "0"):
                    if(index < 10):
                        dict["data"]["datasize"] = byte.encode('hex')
                        dict["data"]["string"] = []
                    elif(index < (10 + int(dict["data"]["datasize"],16))):
                        dict["data"]["string"].append(byte.encode('utf8'))
                    else:
                        #string end
                        logs.append(dict)
                        dict = {"id":[],"timestamp":[],"info":{"string":"","arguments":"","type":"","unused":""},"data":{}}
                        index = 0
                        dict["id"].append(byte.encode('hex'))
                elif(dict["info"]["arguments"] == "1" and dict["info"]["string"] == "0"):
                    if(index < 10):
                        dict["data"]["datasize"] = byte.encode('hex')
                        dict["data"]["arguments"] = []
                    elif (argumentindex >= int(dict["data"]["datasize"],16)):
                        # end arguments
                        logs.append(dict)
                        dict = {"id":[],"timestamp":[],"info":{"string":"","arguments":"","type":"","unused":""},"data":{}}
                        index = 0
                        argumentindex =0
                        dict["id"].append(byte.encode('hex'))
                    elif(index < (10+argumentindex+1)):
                        dictargument = {}
                        dictargument["size"] = byte.encode('hex')
                        dictargument["data"] = []
                    elif(index < (10+argumentindex+int(dictargument["size"],16)+1)):
                        dictargument["data"].append(byte.encode('hex'))
                        if(index == (10+argumentindex+int(dictargument["size"],16))):
                            dict["data"]["arguments"].append(dictargument)
                            argumentindex = argumentindex + int(dictargument["size"],16) + 1
                    else:
                        print "error 0x01"
                        sys.exit(1)
                elif(dict["info"]["arguments"] == "0" and dict["info"]["string"] == "0"):
                    if(index < 10):
                        dict["data"]["datasize"] = byte.encode('hex')
                    elif (int(dict["data"]["datasize"],16) == 0):
                        # end arguments
                        logs.append(dict)
                        dict = {"id":[],"timestamp":[],"info":{"string":"","arguments":"","type":"","unused":""},"data":{}}
                        index = 0
                        dict["id"].append(byte.encode('hex'))
                else :
                    print "error 0x02"
                    sys.exit(2)
            else :
                print "error 0x03"
                sys.exit(3)
            index = index+1
            byte = f.read(1)
        printed = json.dumps(logs, indent=4)

        #open decrypt cards
        with open("../decrypt/card.json","r") as f:
            decryptlist = json.loads(f.read())
        for decryptcard in decryptlist:
            if decryptcard["type"] == "LOG":
                LOGcard = decryptcard["decryptCard"]
            elif decryptcard["type"] == "WARN":
                WARNcard = decryptcard["decryptCard"]
            elif decryptcard["type"] == "ERR":
                ERRcard = decryptcard["decryptCard"]

        #{"id":[],"timestamp":[],"info":{"string":"","arguments":"","type":"","unused":""},"data":{}}
        for log in logs:
            timestamp = _byte2int(log["timestamp"],True)
            id = "0x"+_byte2hex(log["id"],True)[-4:]+"UL"
            if log["info"]["type"] == "00":
                begin = "(LOG)"
                cards = LOGcard
            elif log["info"]["type"] == "01":
                begin = "(WARN)"
                cards = WARNcard
            elif log["info"]["type"] == "11":
                begin = "(ERR)"
                cards = ERRcard
            if(log["info"]["arguments"] == "1" and log["info"]["string"] == "0"):
                for card in cards:
                    if card["ID"] == id:
                        values = ()
                        for argument in log["data"]["arguments"]:
                            values+=(_byte2int(argument["data"],True),)
                        logged = card["Format"] % values
                        print begin + str(timestamp) + " : " + logged
            elif(log["info"]["arguments"] == "0" and log["info"]["string"] == "1"):
                for card in cards:
                    if card["ID"] == id:
                        if "%.*s" in card["Format"]:
                            formated = card["Format"] % (int(log["data"]["datasize"],16),"".join(log["data"]["string"]))
                        else:
                            formated = card["Format"] % "".join(log["data"]["string"])
                        break
                print begin + str(timestamp) + " : " + formated
            elif(log["info"]["arguments"] == "0" and log["info"]["string"] == "0"):
                for card in cards:
                    if card["ID"] == id:
                        print begin + str(timestamp) + " : " + card["Format"]

if __name__ == "__main__":
   main(sys.argv[1:])
