#import things
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'tri_algo'))

#import libraries
import math
import numpy
import datetime
import os

#import internal modules
import tri_algo.geo2d as geo2d
import tri_algo.device as device
import tri_algo.tower as tower

#assuming elevation = 0
class triangulate:

    '''
    def find(self, lat1, long1, dist1, lat2, long2, dist2, lat3, long3, dist3):
        
        earthR = 6371

        
        print(dist1)
        print(dist2)
        print(dist3)
        
        
        
        lat1 = 37.418436
        long1 = -121.963477
        #dist1 = 0.265710701754
        lat2 = 37.417243
        long2 = -121.961889
        #dist2 = 0.234592423446
        lat3 = 37.418692
        long3 = -121.960194
        #dist3 = 0.0548954278262
        

        #using authalic sphere
        #if using an ellipsoid this step is slightly different
        #Convert geodetic Lat/Long to ECEF xyz
        #   1. Convert Lat/Long to radians
        #   2. Convert Lat/Long(radians) to ECEF
        xA = earthR *(math.cos(math.radians(lat1)) * math.cos(math.radians(long1)))
        yA = earthR *(math.cos(math.radians(lat1)) * math.sin(math.radians(long1)))
        zA = earthR *(math.sin(math.radians(lat1)))

        xB = earthR *(math.cos(math.radians(lat2)) * math.cos(math.radians(long2)))
        yB = earthR *(math.cos(math.radians(lat2)) * math.sin(math.radians(long2)))
        zB = earthR *(math.sin(math.radians(lat2)))

        xC = earthR *(math.cos(math.radians(lat3)) * math.cos(math.radians(long3)))
        yC = earthR *(math.cos(math.radians(lat3)) * math.sin(math.radians(long3)))
        zC = earthR *(math.sin(math.radians(lat3)))

        P1 = numpy.array([xA, yA, zA])
        P2 = numpy.array([xB, yB, zB])
        P3 = numpy.array([xC, yC, zC])

        #from wikipedia
        #transform to get circle 1 at origin
        #transform to get circle 2 on x axis
        ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
        i = numpy.dot(ex, P3 - P1)
        ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
        ez = numpy.cross(ex,ey)
        d = numpy.linalg.norm(P2 - P1)
        j = numpy.dot(ey, P3 - P1)

        #from wikipedia
        #plug and chug using above values
        x = (pow(dist1,2) - pow(dist2,2) + pow(d,2))/(2*d)
        y = ((pow(dist1,2) - pow(dist3,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

        
        print("x: " + str(x))
        print("y: " + str(y))

        print("pow x: " + str(pow(x,2)))
        print("pow y: " + str(pow(y,2)))
        

        # only one case shown here
        #f = pow(dist1,2) - pow(x,2) - pow(y,2)
        #print(f)
        z = numpy.sqrt(abs(pow(dist1,2) - pow(x,2) - pow(y,2)))
        

        #triPt is an array with ECEF x,y,z of trilateration point
        triPt = P1 + x*ex + y*ey + z*ez

        #convert back to lat/long from ECEF
        #convert to degrees
        lat = math.degrees(math.asin(triPt[2] / earthR))
        long = math.degrees(math.atan2(triPt[1],triPt[0]))

        print("lat: " + str(lat) + " \n" + "long: " + str(long))
        return lat, long
    '''

    def find(self, lat1, long1, t1, rsrp1, lat2, long2, t2, rsrp2, lat3, long3, t3, rsrp3, method:device.DistMethod=device.DistMethod.ta):

        dev = device.Device()

        tow1 = tower.Tower(latitude=lat1, longitude=long1)
        tow2 = tower.Tower(latitude=lat2, longitude=long2)
        tow3 = tower.Tower(latitude=lat3, longitude=long3)

        dev.addTower(tow1, timeAdvance=t1, rsrp=rsrp1)
        dev.addTower(tow2, timeAdvance=t2, rsrp=rsrp2)
        dev.addTower(tow3, timeAdvance=t3, rsrp=rsrp3)

        my_lat, my_long = dev.ellipsoidal2DPos(method)

        return my_lat, my_long
    
    def convertToDegrees(self, distance):

        degrees = 0

        #define the nautical mile
        #one degree is 111111 meters
        degMeterDef = 111111

        #convert to degrees
        degrees = distance / degMeterDef
        #print(degrees)

        return degrees
    
    def convertToMeters(self, TA):
        
        meters = 0

        #convert the timing advance to meters

        #set the value of Ts which is a constant, I think
        Ts = 1 / (2048 * 15000)
        #print(Ts)

        #set the value of Nta which is the timing offset between uplink and downlink radio frames
        
        #this was from a website calculator
        #Nta = 16 * TA * Ts

        #This is the value we will use since the nrf9160 automatically includes the "times 16"
        #nordic stores Timing Advance as "Basic Time units" or Ts
        Nta = TA * Ts
        #print(Nta)

        #determine the number of meters
        meters = (3 * pow(10,8) * Nta) / 2
        #print(meters)

        return meters
    
    def detAction(self, history):
        #figure out whether to run the 3 tower version, 2 tower, or 1 tower

        item = 0

        #break at end of list
        #if item == len(history):
        #   break

        #create smaller list to store current 3 towers
        #skip the parts of the list that separatefloat
        towerCount = 0
        towerList = list()
        locationList = list()
        #while str(history[item][0]) != "***********************************************************************************************":
        while item < len(history):
            #print(towerCount)
            
            #increment the number of towers until asteriks
            if str(history[item][0]) == "***********************************************************************************************":
                if towerCount == 3:
                    #convert timing advances
                    #changed due to disable of SNR
                    ''''
                    lat1 = float(towerList[0][8])
                    long1 = float(towerList[0][9])
                    t1 = int(towerList[0][4])
                    rsrp1 = int(towerList[0][5])

                    lat2 = float(towerList[0][8])
                    long2 = float(towerList[0][9])
                    t2 = int(towerList[0][4])
                    rsrp2 = int(towerList[0][5])

                    lat3 = float(towerList[0][8])
                    long3 = float(towerList[0][9])
                    t3 = int(towerList[0][4])
                    rsrp3 = int(towerList[0][5])
                    '''

                    lat1 = float(towerList[0][7])
                    long1 = float(towerList[0][8])
                    t1 = int(towerList[0][4])
                    rsrp1 = int(towerList[0][5])

                    lat2 = float(towerList[0][7])
                    long2 = float(towerList[0][8])
                    t2 = int(towerList[0][4])
                    rsrp2 = int(towerList[0][5])

                    lat3 = float(towerList[0][7])
                    long3 = float(towerList[0][8])
                    t3 = int(towerList[0][4])
                    rsrp3 = int(towerList[0][5])

                    #triangulate
                    lat, long = self.find(lat1, long1, t1, rsrp1, lat2, long2, t2, rsrp2, lat3, long3, t3, rsrp3)
                    locationList.append([str(towerCount), str(lat), str(long), history[item - 1][1], history[item - 1][2], history[item - 1][3]], )
                    #print(locationList)

                    #clear tower count
                    towerCount = 0
                    towerList.clear()
                
                elif towerCount == 2:
                    print("only two towers!")

                    #do two tower action
                    

                    #clear tower count
                    towerCount = 0
                    towerList.clear()
                
                elif towerCount == 1:
                    print("only one tower!")

                    #do one tower action

                    #get the distance from the tower
                    t1 = self.convertToMeters(int(towerList[0][4]))
                    radius = self.convertToDegrees(t1)

                    #store the lat and long of the tower as well as the distance away from it
                    #sort of like a radius, but would look like a ring
                    #changed for disabling of SNR
                    lat = towerList[0][7]
                    long = towerList[0][8]
                    locationList.append([str(towerCount), str(lat), str(long), radius, history[item - 1][1], history[item - 1][2], history[item - 1][3]])
                    
                    #clear tower count
                    towerCount = 0
                    towerList.clear()
                
                #print the line of asteriks to make things look pretty
                print(history[item][0])
            
            #ignore lines we don't need
            elif str(history[item][0]) == "" or history[item][0] == "" or history[item][0] == '' or str(history[item][0]) == "empty":
                derp = 0


            else:
                print(history[item][0])
                towerList.append(history[item])
                towerCount = towerCount + 1


            item = item + 1
        return locationList
    
    #stores locations and times to a file in the locations folder
    def storeLocations(self, locationList):

        time = datetime.datetime.now()

        #set the name of the output file to history and the current time
        year = time.year
        month = time.month
        day = time.day
        hour = time.hour
        minute = time.minute
        second = time.second
        curTime = "_" + str(year) + "-" + str(month) + "-" + str(day) + "_" + str(hour) + "-" + str(minute) + "-" + str(second) + ".txt"
        fileName = "positions"
        fName = fileName + str(curTime) 

        #ensure output directory exists
        path = "./locations"
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        #create file
        fName = path + "/" + fileName + str(curTime)
        open(fName, 'a+').close()

        #write to file
        file = open(fName, "w")

        #print each location and time
        for item in locationList:
            for x in item:
                t = ''.join(str(x))
                file.write(t)
                file.write(" ")
            file.write("\n")
        
        #close and finish
        file.close()
        print("Finished writing!")




def main():

    #timing advances
    TA1 = 272
    TA2 = 176
    TA3 = 112

    #positions
    
    lat1 = 28.064621
    long1 = -82.422188 
    
    lat2 = 28.064032
    long2 = -82.423559 
    
    lat3 = 28.060566
    long3 = -82.413114

    TAList = {TA1, TA2, TA3}
    meterList = list()

    t = triangulate()

    #convert TA to Meters
    for ta in TAList:
        meter = t.convertToMeters(ta)
        meterList.append(meter)
    #print(meterList)

    #convert Meters to degrees
    #currently assuming everything takes place at equator
    degreeList = list()
    for met in meterList:
        deg = t.convertToDegrees(met)
        degreeList.append(deg)
    #print(degreeList)

    #find the bloody thing
    '''
    defDist1 = 0.265710701754
    defDist2 = 0.234592423446
    defDist3 = 0.0548954278262
    '''
    #defaultDist = {defDist1, defDist2, defDist3}
    t.find(lat1, long1, degreeList[0], lat2, long2, degreeList[1], lat3, long3, degreeList[2])
    #t.find(lat1, long1, defaultDist[0], lat2, long2, defaultDist[1], lat3, long3, defaultDist[2])
    #t.find(lat1, long1, defDist1, lat2, long2, defDist2, lat3, long3, defDist3)


# Using the special variable 
# __name__
if __name__=="__main__":
    main()
