#import useful things
#from os import *
import os
from Cryptodome.Cipher import AES
from natsort import natsorted
import datetime
from request import *

#This class reads the collected Tower data or the Location Data
class Reader:
    
    def hello(self):
        print("Hello from Reader!")

    def selectData(self):
        print("Are you reading the collected data or location data?")
        while True:
            dataType = input("Press 'c' for collected or 'l' for location or 'q' to quit: ")
            if dataType == "c":
                print("Reading Collected Tower Data!")

                towerType = input("Please enter LTE or NBIOT for the associated tower type: ")
                if towerType == "LTE":
                    return "c", "lte"
                elif towerType == "NBIOT":
                    return "c", "nbiot"
                else:
                    return "c", "NONE"
            elif dataType == "l":
                print("Reading Tower Location Data!")
                return "l", "NONE"
            elif dataType == "q":
                return "q", "NONE"
            else:
                print("Wrong character was entered!")
        

    def getDataFileName(self):
        
        while True:
            fileName = input("Enter the name of the file containing the collected Tower Data: ")
            #print("The name of the file is: " + fileName)
            
            path = "./data"
            basedir = os.path.dirname(path)
            #print(basedir)
            if not os.path.exists(basedir):
                os.makedirs(basedir)

            #create file
            #fName = path + "/" + fileName
            os.listdir(basedir)
            if os.path.isfile(os.path.join(path, fileName)):
                break
            else:
                print("File not found.")
                print("You may need to specify directory!")
        fName = path + "/" + fileName
        return fName
    
    #probably won't use
    
    def readLocationFolder(self):
        locationFolderName = input("Enter the name of the folder containing the location of the Towers: ")
        #print("The name of the folder is: " + locationFolderName)
        #print("File not found.")
        #print("You may need to specify directory!")
        #locationFolderName = "./history"

        #make the program work for linux
        locationFolderName = "./" + locationFolderName

        #create the list of towers and their locations
        towerDataList = list()

        for path in natsorted(os.listdir(locationFolderName)):
            #check if current path is a file
            if os.path.isfile(os.path.join(locationFolderName, path)):
                #fileCount += 1
                #print(path)
                File_object = open(os.path.join(locationFolderName, path), "r")
                #get all lines
                while True:
                    next_line = File_object.readline().rstrip()
                    if not next_line:
                        break
                    towerData = next_line.split(" ", 10)
                    #print(towerData)
                    towerDataList.append(towerData)
        return towerDataList
    

    def cleanTowerClock(self, time):
        if "+CCLK:__" in time:
            newTime = time.replace("_", " ")
            newTimeList = newTime.split(" ", 4)
            '''
            for x in newTimeList:
                print(x)
            '''
            #fix time zone
            #tz = int(newTimeList[4]) / 4
            #tz = int(tz)

            #hard code United States since I doubt this device will leave it
            #newTimeList = newTimeList[1], newTimeList[2], newTimeList[3], str(tz)
            newTimeList = newTimeList[1], newTimeList[2], newTimeList[3], "GMT"
            newTime = ' '.join(newTimeList)
            time = newTime

        return time


    def readDataLines(self, fileName):

        key = "6a37f086da5a422347b42bac2f651f91"
        #read info from data file
        file = open(fileName, "r")

        while True:
            encryptedFileFlag = input("Enter 'd' to decrypt an encrypted file, "
                                      "or enter 'n' to read an unencrypted file: ")
            if encryptedFileFlag == 'd':
                decryptFlag = True
                break
            elif encryptedFileFlag == 'n':
                decryptFlag = False
                break
            else:
                print("Please enter a valid choice.\n")

        #list of all towers
        towerList = list()

        #search every line
        while True:
            #get the next line
            next_line = file.readline()
            #print(next_line)
            #if the next line does not exist, end search
            if not next_line:
                break

            #if the next line is the top of the file
            if "*****" == next_line:
                derp = 1
            if "Cell ID:" in next_line:
                derp = 2
            if "MCC:" in next_line:
                derp = 3
            if "MNC:" in next_line:
                derp = 4
            if "TAC" in next_line:
                derp = 5
            if "Timing Advance:" in next_line:
                derp = 6
            if "RSRP" in next_line:
                derp = 7
            if "RSRQ" in next_line:
                derp = 8
            
            #if the next line is in the actual content
            if "*****************************************" in next_line:
                #cycle through lines below

                #tower 1
                tower1ID = file.readline().rstrip().replace("\x00", "")
                loop = 0
                if "empty" in tower1ID:
                    tower1MCC = file.readline().rstrip().replace("\x00", "")
                    tower1MNC = file.readline().rstrip().replace("\x00", "")
                    tower1TAC = file.readline().rstrip().replace("\x00", "")
                    tower1TA = file.readline().rstrip().replace("\x00", "")
                    tower1RSRP = file.readline().rstrip().replace("\x00", "")
                    tower1RSRQ = file.readline().rstrip().replace("\x00", "")
                    blank = file.readline().rstrip().replace("\x00", "")
                    tower1SNR = file.readline().rstrip().replace("\x00", "")
                    tower1SECT = self.getAntennaSector(tower1ID, tower1MNC)
                    tower1 = [tower1ID, tower1MCC, tower1MNC, tower1TAC, tower1TA, tower1RSRP, tower1RSRQ, tower1SNR,
                              tower1SECT]
                    if decryptFlag:
                        encryptedTower1 = tower1
                        encryptedTower1.pop()
                        decryptedTower1 = self.decryptTower(encryptedTower1, key, AES.MODE_GCM)
                else:
                    tower1MCC = file.readline().rstrip().replace("\x00", "")
                    tower1MNC = file.readline().rstrip().replace("\x00", "")
                    tower1TAC = file.readline().rstrip().replace("\x00", "")
                    tower1TA = file.readline().rstrip().replace("\x00", "")
                    tower1RSRP = file.readline().rstrip().replace("\x00", "")
                    tower1RSRQ = file.readline().rstrip().replace("\x00", "")
                    tower1SNR = file.readline().rstrip().replace("\x00", "")
                    tower1SECT = self.getAntennaSector(tower1ID, tower1MNC)
                    tower1 = [tower1ID, tower1MCC, tower1MNC, tower1TAC, tower1TA, tower1RSRP, tower1RSRQ, tower1SNR,
                              tower1SECT]
                    if decryptFlag:
                        encryptedTower1 = tower1
                        encryptedTower1.pop()
                        decryptedTower1 = self.decryptTower(encryptedTower1, key, AES.MODE_GCM)
                #tower 2
                tower2ID = file.readline().rstrip().replace("\x00", "")
                loop = 0
                if "empty" in tower2ID:
                    tower2MCC = file.readline().rstrip().replace("\x00", "")
                    tower2MNC = file.readline().rstrip().replace("\x00", "")
                    tower2TAC = file.readline().rstrip().replace("\x00", "")
                    tower2TA = file.readline().rstrip().replace("\x00", "")
                    tower2RSRP = file.readline().rstrip().replace("\x00", "")
                    tower2RSRQ = file.readline().rstrip().replace("\x00", "")
                    blank = file.readline().rstrip().replace("\x00", "")
                    tower2SNR = file.readline().rstrip().replace("\x00", "")
                    tower2SECT = self.getAntennaSector(tower1ID, tower1MNC)
                    tower2 = [tower2ID, tower2MCC, tower2MNC, tower2TAC, tower2TA, tower2RSRP, tower2RSRQ, tower2SNR,
                              tower2SECT]
                    if decryptFlag:
                        encryptedTower2 = tower2
                        encryptedTower2.pop()
                        decryptedTower2 = self.decryptTower(encryptedTower2, key, AES.MODE_GCM)
                else:
                    tower2MCC = file.readline().rstrip().replace("\x00", "")
                    tower2MNC = file.readline().rstrip().replace("\x00", "")
                    tower2TAC = file.readline().rstrip().replace("\x00", "")
                    tower2TA = file.readline().rstrip().replace("\x00", "")
                    tower2RSRP = file.readline().rstrip().replace("\x00", "")
                    tower2RSRQ = file.readline().rstrip().replace("\x00", "")
                    tower2SNR = file.readline().rstrip().replace("\x00", "")
                    tower2SECT = self.getAntennaSector(tower1ID, tower1MNC)
                    tower2 = [tower2ID, tower2MCC, tower2MNC, tower2TAC, tower2TA, tower2RSRP, tower2RSRQ, tower2SNR,
                              tower2SECT]
                    if decryptFlag:
                        encryptedTower2 = tower2
                        encryptedTower2.pop()
                        decryptedTower2 = self.decryptTower(encryptedTower2, key, AES.MODE_GCM)
                #tower 3
                tower3ID = file.readline().rstrip().replace("\x00", "")
                if "empty" in tower3ID:
                    tower3MCC = file.readline().rstrip().replace("\x00", "")
                    tower3MNC = file.readline().rstrip().replace("\x00", "")
                    tower3TAC = file.readline().rstrip().replace("\x00", "")
                    tower3TA = file.readline().rstrip().replace("\x00", "")
                    tower3RSRP = file.readline().rstrip().replace("\x00", "")
                    tower3RSRQ = file.readline().rstrip().replace("\x00", "")
                    blank = file.readline().rstrip().replace("\x00", "")
                    tower3SNR = file.readline().rstrip().replace("\x00", "")
                    tower3SECT = self.getAntennaSector(tower3ID, tower3MNC)
                    tower3 = [tower3ID, tower3MCC, tower3MNC, tower3TAC, tower3TA, tower3RSRP, tower3RSRQ, tower3SNR,
                              tower3SECT]
                    if decryptFlag:
                        encryptedTower3 = tower3
                        encryptedTower3.pop()
                        decryptedTower3 = self.decryptTower(encryptedTower3, key, AES.MODE_GCM)
                else:
                    tower3MCC = file.readline().rstrip().replace("\x00", "")
                    tower3MNC = file.readline().rstrip().replace("\x00", "")
                    tower3TAC = file.readline().rstrip().replace("\x00", "")
                    tower3TA = file.readline().rstrip().replace("\x00", "")
                    tower3RSRP = file.readline().rstrip().replace("\x00", "")
                    tower3RSRQ = file.readline().rstrip().replace("\x00", "")
                    tower3SNR = file.readline().rstrip().replace("\x00", "")
                    tower3SECT = self.getAntennaSector(tower3ID, tower3MNC)
                    tower3 = [tower3ID, tower3MCC, tower3MNC, tower3TAC, tower3TA, tower3RSRP, tower3RSRQ, tower3SNR,
                              tower3SECT]
                    if decryptFlag:
                        encryptedTower3 = tower3
                        encryptedTower3.pop()
                        decryptedTower3 = self.decryptTower(encryptedTower3, key, AES.MODE_GCM)
                #clock
                time = file.readline().rstrip().replace("\x00", "")
                time = self.cleanTowerClock(time)
                #print(time)
                #ok_
                ok = file.readline().rstrip().replace("\x00", "")
                #sepatator
                sep = file.readline().rstrip().replace("\x00", "")

                #sepatator
                #sep = file.readline().rstrip().replace("\x00", "")
                #list of towers and time

                if decryptFlag:
                    towerList.append([decryptedTower1, decryptedTower2, decryptedTower3, time])
                else:
                    towerList.append([tower1, tower2, tower3, time])

            #end tower section
        #end while loop to search the file

        #return the list of towers
        return towerList
        
    def compareIDtoDatabase(self, MCC, MNC, TAC, ID):
        #search the database for a matching ID
        #set folder name to "towerLocations"
        locationFolderName = "towerLocations"
        lat = ""
        long = ""
        fileCount = 0
        #Sort the files in the folder
        for path in natsorted(os.listdir(locationFolderName)):
            #check if current path is a file
            if os.path.isfile(os.path.join(locationFolderName, path)):
                fileCount += 1
                #print(path)
                File_object = open(os.path.join(locationFolderName, path), "r")
                #get all lines
                while True:
                    if "empty" in str(ID):
                        break
                    next_line = File_object.readline().rstrip()
                    if not next_line:
                        break
                    towerValuesList = next_line.split(" ", 6)
                    if str(MCC) == towerValuesList[1] and str(MNC) == towerValuesList[2] and str(TAC) == towerValuesList[3] and str(ID) == towerValuesList[4]:
                        #print("Found Match!")
                        long = towerValuesList[5]
                        lat = towerValuesList[6]
        return lat, long

    def storeToFile(self, fileName, data, time):
        #set the name of the output file to history and the current time
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        minute = time.minute
        second = time.second
        curTime = "_" + str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hour) + "-" + str(minute) + "-" + str(second) + ".txt"
        fName = fileName + str(curTime)
        #ensure output directory exists
        path = "./history"
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        #create file
        fName = path + "/" + fileName + str(curTime)
        open(fName, 'a').close()

        #write info from data file
        file = open(fName, "w")

        #write to the file
        out = ""
        for group in data:
            
            count = 0
            for tower in group:
                for item in tower:
                    if count < 30:
                        t = ''.join(str(item))
                        file.write(t)
                        file.write(" ")
                    else:
                        t = ''.join(str(item))
                        file.write(t)
                    count = count + 1
                file.write("\n")
            asterik = "***********************************************************************************************\n"
            file.write(asterik)
        #file.write(out)
        print("Finished writing!")

    def getAntennaSector(self, cid, mnc):
        # get the cid in binary
        # print(cid)
        if type(cid) == str:
            return -1

        # print(int(cid))
        cidBin = bin(int(cid))

        # use only the last 8 bits -- LTE Base Transceiver Station Numbering Code
        sector = int(cidBin[-8::])

        # sector documentation for GSM
        # 1 - N to NE from device
        # 2 - 120 deg cw from sect 1 - Approx. SE to S
        # 3 - 120 deg cw from sect 2 -- Approx. W

        # sector documentation for LTE
        # 1 - S to SW from device
        # 2 - W to NW to N (from device?)
        # 3 - E (from device?)

        # if the sector is not from 0 to 3, return negative 1
        if sector != 0 and sector != 1 and sector != 2 and sector != 3:
            return -1
        # return sector otherwise
        else:
            return sector

    def decryptTower(self, encryptedTower, key, mode):
        decryptedTower = list()
        for cipher in encryptedTower:
            (ciphertext, authTag, nonce) = cipher
            encobj = AES.new(key, mode, nonce)
            decryptedTower.append(encobj)
        return decryptedTower
