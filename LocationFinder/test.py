def convertToMeters(TA):
        
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

test = convertToMeters(160)

print(test)