import matplotlib.pyplot as plt
import numpy as np
import os
from natsort import natsorted


#set the folder to be searched
folderName = input("Enter name of the folder with the data: ")
print("The folder is: " + folderName)

#count the number of files
fileCount = 0

#find the files from the current folder
localFolderName = "./" + folderName

#collect all the lines from all the files
lineList = list()
timestampList = list()
currentList = list()
pinList = list()

#Sort the files in the folder, get all the lines, and store in timestamp and current lists
for path in natsorted(os.listdir(localFolderName)):
    #check if current path is a file
    if os.path.isfile(os.path.join(localFolderName, path)):
        fileCount += 1
        print(path)
        File_object = open(os.path.join(localFolderName, path), "r")
        #lineList += File_object.readlines()
        #get all lines
        while True:
            next_line = File_object.readline()
            if not next_line:
                break
            timestamp, current, pins = next_line.split(",", 3)
            #lineList.append(next_line)
            if timestamp != "Timestamp(ms)":
                timestampList.append(float(timestamp))
                currentList.append(float(current))
                pinList.append(pins)
        File_object.close()
        #print("Finished: " + os.path.join(localFolderName, path))

#print the number of files
print("Number of files is: " + str(fileCount))

#make a pretty picture
plt.plot(timestampList, currentList)
plt.xlabel('Time (ms)')
plt.ylabel('Current (uA)')
plt.suptitle('Current Over Time of the NRF9160')
plt.show()

