import requests
import json
import os
import datetime

class requestLocationAPI:
    #make a request to unwired labs location api

    def requestFromAPI(self, CID, MCC, MNC, LAC, TYPE):
        group = 0
        # print("Current Cell: " + str(CID))
        url = "https://us1.unwiredlabs.com/v2/process"

        # data to be searched
        payload = {
            "token": "Your Key Here",
            "cells": [{
                "radio": TYPE,
                "cid": CID,
                "mcc": MCC,
                "mnc": MNC,
                "lac": LAC
            }],
            "address": 1
        }
        message = json.dumps(payload)
        response = requests.request("POST", url, data=message)
        # print(response.text)
        responseList = response.text.split(",")
        # print(responseList)
        if responseList[0] == '{"status":"ok"':
            # print("OK!")

            # print the current amount of calls left to the api
            balance = str(responseList[1])
            balance = balance[10:]

            # print the lat
            lat = str(responseList[2])
            lat = lat[6:]

            # print the long
            long = str(responseList[3])
            long = long[6:]

            # put the date added to database
            currentTime = datetime.datetime.now()
            time = str(currentTime)

            # print to screen and file
            print("Requests Left: " + balance)
            towerData = str(CID) + " " + str(MCC) + " " + str(MNC) + " " + str(
                LAC) + " " + lat + " " + long + " " + time
            group = group + 1
            self.storeToFile("towerSearch", towerData, (group % 3))
            if not lat or not long:
                return None, None
            else:
                return lat, long

    def checkStored(self, fileName, CID, MCC, MNC):
        #open the folder and file
        path = "./towerDB"
        basedir = os.path.dirname(path)
        fName = path + "/" + fileName
        
        file = open(fName, "r")

        while True:
            #read line by line searching for towers
            next_line = file.readline()
            if not next_line:
                #add new tower
                return False, -1, -1

            towerData = next_line.split(" ")
            print(towerData)
            string1 = str(towerData[0])
            if type(towerData[0]) == int:
                # print(towerData[0])
                # check if tower exists in tower database and ignore if it does
                if str(CID) == str(towerData[0]) and str(MCC) == str(towerData[1]) and str(MNC) == str(towerData[2]):
                    # add the new tower
                    # print("Match Found!")
                    return True, str(towerData[4]), str(towerData[5])
            else:
                towerData[:] = towerData[1:]

        return ""
                

    def storeToFile(self, fileName, data, group):
        #set the name of the output file to history and the current time
        #ensure output directory exists
        path = "./towerDB"
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        #create file
        fName = path + "/" + fileName
        open(fName, 'a').close()

        #read info from data file
        # = open(fName, "w")
        file = open(fName, "a+")

        #write to the file
        file.write(data)
        file.write("\n")
        if group == 0:
            file.write("*****************************************\n")
        #file.write(out)

        print("Finished writing!")

    def request(self, CID, MCC, MNC, LAC, TYPE):
        
        if str(CID) != "empty" and str(CID) != "" and str(CID) != " ":
            #check database for tower
            inDatabase, lat, long = self.checkStored("towerSearch", CID, MCC, MNC)
            if not inDatabase:
                #make a request based on tower type
                if TYPE == "lte" or TYPE == "nbiot":
                    lat, long = self.requestFromAPI(CID, MCC, MNC, LAC, TYPE)
                else:
                    print("Tower Type Not Specified")
                return lat, long
            elif inDatabase:
                #say in database
                print("In database already!")
                return lat, long
            else:
                print("Something went wrong while performing the API request!")
                return -1, -1
        else:
            lat = ""
            long = ""
            return lat, long
