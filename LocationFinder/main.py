#import useful libraries

#import other files
from reader import *
from triangulate import *

#run main function
def main():
    while True:
        #create a reader object
        info = Reader()
        req = requestLocationAPI()
        tri = triangulate()

        #determine whether to read from the collected tower information or from the tower location file
        selectChar, towerType = info.selectData()
        if  selectChar == "c":
            #do things
            #print(selectChar)
            selectChar = ""
            fileName = info.getDataFileName()
            towerDataList = info.readDataLines(fileName)
            
            #print data from the text file
            '''
            for x in towerDataList:
                print(towerDataList)
                #derp = 0
            '''

            #compare tower id to database
            #towerGroup = 0
            tower = 0
            #towerID = 0
            locationList = list()
            locationListGroup = list()
            for towerGroup in towerDataList:
                
                #select a group of three towers
                #tower = 0
                for tower in towerGroup:

                    #select tower ID from data collected from a single tower, if it exists
                    ID = tower[0]
                    MCC = tower[1]
                    MNC = tower[2]
                    TAC = tower[3]
                    TA = tower[4]
                    RSRP = tower[5]
                    RSRQ = tower[6]
                    SNR = tower[7]
                    SECT = tower[8]

                    #print(ID)
                    #lat, long = info.compareIDtoDatabase(MCC, MNC, TAC, ID)
                    lat, long = req.request(ID, MCC, MNC, TAC, towerType)
                    
                    #for some reason extra values are but in between real towers
                    locationListGroup.append([ID, MCC, MNC, TAC, TA, RSRP, RSRQ, SNR, lat, long, SECT])
                
                #append location to tower lists
                timeList = list()
                #timeListList = list()
                timeList.append(towerGroup[3])
                #timeListList.append(timeList)
                #locationList.append([locationListGroup[0:3], timeListList])
                locationList.append([locationListGroup[0], locationListGroup[1], locationListGroup[2], towerGroup[3]])
                #locationList.append([locationListGroup[0],locationListGroup[1], locationListGroup[2], timeList])
                #print(locationList)
                locationListGroup.clear()
                timeList.clear()
                #timeListList.clear()

            #store tower lists to output file
            time = datetime.datetime.now()
            info.storeToFile("history", locationList, time)
            #should be done with location finding

        #get a list of all towers, their locations, and the timestamp of the collection
        elif selectChar == "l":
            selectChar = ""
            
            #store all the towers to a big list
            towerDataList = info.readLocationFolder()
            #print(towerDataList)
            locationList = tri.detAction(towerDataList)
            tri.storeLocations(locationList)

        elif selectChar == "q":
            selectChar = ""
            #quit
            print("Now exiting the program")
            break
        
        else:
            #something went wrong
            print("Something went wrong and I don't know why!")


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
