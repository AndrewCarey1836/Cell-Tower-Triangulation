#from machine import Pin, I2C
from machine import *
#from time import sleep
from time import *
from _thread import *
from ds3231 import *
from imu import MPU6050
from ssd1306 import *
import framebuf



def toggle_lights():
        
    #Output going to the nrf9160
    PIN_POWER_BUTTON = 18
    PIN_COLLECT_TOWERS = 19
    PIN_STORE_TOWERS = 20
    PIN_OUTPUT_OTHER = 21
    
    #Output
    Power_Button = Pin(PIN_POWER_BUTTON, Pin.OUT)
    Collect_Towers = Pin(PIN_COLLECT_TOWERS, Pin.OUT)
    Store_Towers = Pin(PIN_STORE_TOWERS, Pin.OUT)
    Output_Other = Pin(PIN_OUTPUT_OTHER, Pin.OUT)
    
    
    Power_Button.value(1)
    sleep(0.1)
    Collect_Towers.value(1)
    sleep(0.1)
    Store_Towers.value(1)
    sleep(0.1)
    Output_Other.value(1)
    sleep(0.1)
    sleep(5)
    Power_Button.value(0)
    sleep(0.1)
    Collect_Towers.value(0)
    sleep(0.1)
    Store_Towers.value(0)
    sleep(0.1)
    Output_Other.value(0)
    sleep(5)
    
def test_lights():
    High = 1
    Low = 0

    #Input from the nrf9160
    PIN_TOWER_READ_SUCCESS = 10
    PIN_TOWER_READ_FAIL = 11
    PIN_TOWER_BUFFER_FULL = 12
    PIN_CONNECTED = 13

    #Output going to the nrf9160
    PIN_POWER_BUTTON = 18
    PIN_COLLECT_TOWERS = 19
    PIN_STORE_TOWERS = 20
    PIN_OUTPUT_OTHER = 21

    #Input
    Tower_Read_Success = Pin(PIN_TOWER_READ_SUCCESS, Pin.IN) #green
    Tower_Read_Fail = Pin(PIN_TOWER_READ_FAIL, Pin.IN) #red
    Tower_Buffer_Full = Pin(PIN_TOWER_BUFFER_FULL, Pin.IN) #yellow
    Tower_Connected = Pin(PIN_CONNECTED, Pin.IN) #blue

    #Output
    Power_Button = Pin(PIN_POWER_BUTTON, Pin.OUT) #green
    Collect_Towers = Pin(PIN_COLLECT_TOWERS, Pin.OUT) #yellow
    Store_Towers = Pin(PIN_STORE_TOWERS, Pin.OUT) #red
    Output_Other = Pin(PIN_OUTPUT_OTHER, Pin.OUT) #blue
    
    Power_Button.value(Low)
    sleep(0.1)
    Collect_Towers.value(Low)
    sleep(0.1)
    Store_Towers.value(Low)
    sleep(0.1)
    Output_Other.value(Low)
    print("Low")
    sleep(2)
    Power_Button.value(High)
    sleep(0.1)
    Collect_Towers.value(High)
    sleep(0.1)
    Store_Towers.value(High)
    sleep(0.1)
    Output_Other.value(High)
    print("High")
    sleep(2)

def get_input():
    #Input from the nrf9160
    PIN_TOWER_READ_SUCCESS = 10
    PIN_TOWER_READ_FAIL = 11
    PIN_TOWER_BUFFER_FULL = 12
    PIN_CONNECTED = 13
    
    #Output going to the nrf9160
    PIN_POWER_BUTTON = 18
    PIN_COLLECT_TOWERS = 19
    PIN_STORE_TOWERS = 20
    PIN_OUTPUT_OTHER = 21
    
    #Output
    Power_Button = Pin(PIN_POWER_BUTTON, Pin.OUT)
    Collect_Towers = Pin(PIN_COLLECT_TOWERS, Pin.OUT)
    Store_Towers = Pin(PIN_STORE_TOWERS, Pin.OUT)
    Output_Other = Pin(PIN_OUTPUT_OTHER, Pin.OUT)

    #Input
    Tower_Read_Success = Pin(PIN_TOWER_READ_SUCCESS, Pin.IN) #green
    Tower_Read_Fail = Pin(PIN_TOWER_READ_FAIL, Pin.IN) #red
    Tower_Buffer_Full = Pin(PIN_TOWER_BUFFER_FULL, Pin.IN) #yellow
    Input_Other = Pin(PIN_CONNECTED, Pin.IN) #blue
    
    while True:
        if Tower_Read_Success.value() == 1:
            #print("Read Success High")
            Power_Button.value(1)
            sleep(1)
            Power_Button.value(0)
        if Tower_Read_Fail.value() == 1:
            #print("Read Fail High")
            Store_Towers.value(1)
            sleep(1)
            Store_Towers.value(0)
        if Tower_Buffer_Full.value() == 1:
            #print("Buffer High")
            Collect_Towers.value(1)
            sleep(1)
            Collect_Towers.value(0)
        if Input_Other.value() == 1:
            #print("Other High")
            Output_Other.value(1)
            sleep(1)
            Output_Other.value(0)
        
    
def print_Andrew():
    
    i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    #set up display
    
    display = SSD1306_I2C(128, 32, i2c0)
    display.poweroff()
    sleep(0.5)
    display.poweron()
    display.fill(0)
    display.text("Andrew Carey!", 0, 16, 1)
    display.show()
    sleep(0.5)
    
def print_acl():
    print("DERP!")

#user this if multi threading
def acl_turn_on():
    
    #turn the device on if 
    on = 0
    print(str(on))
    


def main():
    #i2c pins for the MPU6050, SDD1306
    i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    #i2c pins for the RTC, SDD1306
    i2c1 = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
    
    #Set up RTC
    rtcList = i2c1.scan()
    rtc = rtcList[0]
    ds = DS3231(i2c1)
    
    #Set up MPU6050
    acl = MPU6050(i2c0)
    
    #test display
    print_Andrew()
    
    #set up display
    #i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    #set up display
    display = SSD1306_I2C(128, 32, i2c0)
    display_clock = SSD1306_I2C(128, 32, i2c1)
    display.poweroff()
    display_clock.poweroff()
    sleep(0.5)
    
    #hard code time
    '''
    year = 2023 # Can be yyyy or yy format
    month = 04
    mday = 05
    hour = 13 # 24 hour format only
    minute = 04
    second = 00 # Optional
    #weekday = 6 # Optional

    #datetime = (year, month, mday, hour, minute, second, weekday)
    datetime = (year, month, mday, hour, minute, second)
    ds.datetime(datetime)
    '''

    #get information from the RTC
    #print(ds.datetime())
    '''
    year = ds.datetime()[0]
    month = ds.datetime()[1]
    day = ds.datetime()[2]
    hour = ds.datetime()[4]
    minute = ds.datetime()[5]
    second = ds.datetime()[6]
    '''
    #print the values for sanity

    '''
    print(year)
    print(month)
    print(day)
    print(hour)
    print(minute)
    print(second)
    '''

    '''
    Define all the connections for the nrf9160 and raspberry pi pico!

    Inputs are defined as signals from the nrf9160 to the pico
    Outputs are defined as signals from the pico to the nrf9160

    Inputs:
    Tower Read Success: a valid tower was found and stored in a tower buffer
    Tower Read Fail: a valid tower was not found
    Tower Buffer Full: The number of towers found is at the maximum supported

    Outputs:
    Power Button: Wake the board up from a powered down state
    Collect Towers: Ping towers and store valid results to the buffer
    Store Towers: Store all the found towers to the storage medium
    
    '''
    #set pico side things high and low
    High = 1
    Low = 0

    #Input from the nrf9160
    PIN_TOWER_READ_SUCCESS = 10
    PIN_TOWER_READ_FAIL = 11
    PIN_TOWER_BUFFER_FULL = 12
    PIN_CONNECTED = 13

    #Output going to the nrf9160
    PIN_POWER_BUTTON = 18
    PIN_COLLECT_TOWERS = 19
    PIN_STORE_TOWERS = 20
    PIN_OUTPUT_OTHER = 21

    #Input
    Tower_Read_Success = Pin(PIN_TOWER_READ_SUCCESS, Pin.IN) #green
    Tower_Read_Fail = Pin(PIN_TOWER_READ_FAIL, Pin.IN) #red
    Tower_Buffer_Full = Pin(PIN_TOWER_BUFFER_FULL, Pin.IN) #yellow
    Tower_Connected = Pin(PIN_CONNECTED, Pin.IN) #blue

    #Output
    Power_Button = Pin(PIN_POWER_BUTTON, Pin.OUT) #green
    Collect_Towers = Pin(PIN_COLLECT_TOWERS, Pin.OUT) #yellow
    Store_Towers = Pin(PIN_STORE_TOWERS, Pin.OUT) #red
    Output_Other = Pin(PIN_OUTPUT_OTHER, Pin.OUT) #blue
    
    #Power the board back up
    Collect_Towers.value(Low)
     
    
    #Power Button Behavior
    #Turn the board on after an hour of idling
    #get information from the RTC
    
    while True:
        #get information from the RTC
        
        #print the current Time
        print(ds.datetime())
        
        year_start = ds.datetime()[0]
        month_start = ds.datetime()[1]
        day_start = ds.datetime()[2]
        hour_start = ds.datetime()[4]
        minute_start = ds.datetime()[5]
        second_start = ds.datetime()[6]
        
        #reset screens
        display = SSD1306_I2C(128, 32, i2c0)
        display_clock = SSD1306_I2C(128, 32, i2c1)
        
        #set the string to go to the screen
        date0 = "Start: " + str(year_start) + " " + str(month_start) + " " + str(day_start)
        time0 = "Start: " + str(hour_start) + " " + str(minute_start)+ " " + str(second_start)
        
        #set the screen
        display_clock.text(date0, 0, 0, 1)
        display_clock.text(time0, 0, 8, 1)
        display_clock.poweron()
        display_clock.show()
        #check that lights work
        #make this the boot up cause it's pretty
        #toggle_lights()
        
        #test_lights()
        
        loop = 0
        five = 5
        import framebuf
        
        while loop < five:
            ax=round(acl.accel.x,2)
            ay=round(acl.accel.y,2)
            az=round(acl.accel.z,2)
            gx=round(acl.gyro.x)
            gy=round(acl.gyro.y)
            gz=round(acl.gyro.z)
            tem=round(acl.temperature,2)
            #print("\n")
            #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
            #message = "ax: " + str(int(ax))
            sleep(0.1)
            #message = "gx: " + str(int(gx)) + " gy: " + str(int(gy)) + " gz: " + str(int(gz))
            display = SSD1306_I2C(128, 32, i2c0)
            #display.poweron()
            message0 = "ax: " + str(int(ax)) + " gx: " + str(int(gx))
            display.text(message0, 0, 0, 1)
            message1 = "ay: " + str(int(ay)) + " gy: " + str(int(gy))
            display.text(message1, 0, 12, 1)
            message2 = "az: " + str(int(az)) + " gz: " + str(int(gz))
            display.text(message1, 0, 24, 1)
            '''
            byte0 = bytearray()
            byte1 = bytearray()
            byte0.extend(message0)
            byte1.extend(message1)
            
            fbuf0 = framebuf.FrameBuffer(byte0, 16, 8, framebuf.MONO_VLSB)
            display.blit(fbuf0, 0, 0, 0)
            '''
            display.show()
            #sleep(0.1)
            #display.poweroff()
            sleep(0.1)
            loop = loop + 1
        
        #collect tower data
        #pause for dev kit to boot
        sleep(45)
        
        #try to collect towers five times
        loop = 0
        five = 5
        while loop < five:
            print(loop)
            display = SSD1306_I2C(128, 32, i2c0)
            tower_num = "Tower Search: " + str(loop + 1)
            display.text(tower_num, 0, 0, 1)
            display.show()
            Collect_Towers.value(High)
            sleep(0.1)
            Collect_Towers.value(Low)
            loop = loop + 1
            #pause to reconnect to other towers
            sleep(20)
        
        sleep(10)
        Store_Towers.value(High)
        Output_Other.value(High)
        sleep(0.2)
        Store_Towers.value(Low)
        Output_Other.value(Low)
        sleep(0.2)
        
        
        #wait for a specified time to turn back one
        print(ds.datetime())
        year_now = ds.datetime()[0]
        month_now = ds.datetime()[1]
        day_now = ds.datetime()[2]
        hour_now = ds.datetime()[4]
        minute_now = ds.datetime()[5]
        second_now = ds.datetime()[6]
        
        #refresh clock time
        display_clock = SSD1306_I2C(128, 32, i2c1)
        display = SSD1306_I2C(128, 32, i2c0)
        display_clock.poweroff()
        sleep(0.1)
        display_clock.poweron()
        
        #set end time
        date1 = "End  : " + str(year_now) + " " + str(month_now) + " " + str(day_now)
        time1 = "End  : " + str(hour_now) + " " + str(minute_now)+ " " + str(second_now)
        display_clock.text(date0, 0, 0, 1)
        display_clock.text(date1, 0, 8, 1)
        display_clock.text(time0, 0, 16, 1)
        display_clock.text(time1, 0, 24, 1)
        display_clock.show()
        
        sleep(10)
        
        #time spent running
        year_run = year_now - year_start
        month_run = month_now - month_start
        day_run = day_now - day_start
        hour_run = hour_now - hour_start
        minute_run = minute_now - minute_start
        second_run = second_now - second_start
        
        print("Total time spent collecting data")
        print("Year(s): " + str(year_run))
        print("Month(s): " + str(month_run))
        print("Day(s): " + str(day_run))
        print("Hour(s): " + str(hour_run))
        print("Minute(s): " + str(minute_run))
        print("Second(s): " + str(second_run))        
        
        
        #boot back up in a specified amount of time
        #boot_time = hour_now + 1
        boot_hour = hour_now
        boot_minute = minute_now + 2
        boot_second = second_now
        #if boot_time == 24:
        #    boot_time = 0
        print("Booting up at: " + str(boot_hour) + ":" + str(boot_minute) + ":" + str(boot_second))
        
        #refresh clock time
        display_clock.poweroff()
        sleep(0.1)
        display_clock.poweron()
        
        #display next boot time
        display_clock = SSD1306_I2C(128, 32, i2c1)
        #nextTime = "Boot: " + str(boot_time) + " " + str(minute_now) + " " + str(second_now)
        nextTime = "Boot: " + str(boot_hour) + " " + str(minute_now) + " " + str(second_now)
        display_clock.text(nextTime, 0, 0, 1)
        display_clock.show()
        display.poweroff()
        sleep(0.1)
        display.poweron()
        display.poweroff()
        
        '''
        #boot back up in an hour
        #turn on if device moves
        boot_time_hour = 1
        boot_time_min = boot_time_hour * 60
        boot_time_sec = boot_time_min * 60
        '''
        
        #boot back up in 2 minutes
        #boot_time_min = 2
        #boot_time_sec = boot_time_min * 60
        
        #boot back up in 20 seconds
        boot_time_sec = 20
        
        #set boot time counter
        wake = 0
        
        #multiply boot time sec by ten to account for rapid sleep
        boot_time_deci = boot_time_sec * 10
        
        #set baseline position
        ax_base=round(acl.accel.x,2)
        ay_base=round(acl.accel.y,2)
        az_base=round(acl.accel.z,2)
        gx_base=round(acl.gyro.x)
        gy_base=round(acl.gyro.y)
        gz_base=round(acl.gyro.z)
        #turn on the board if movement is detected
        on = 0
        
        while on == 0:
            #get new reading
            ax=round(acl.accel.x,2)
            ay=round(acl.accel.y,2)
            az=round(acl.accel.z,2)
            gx=round(acl.gyro.x)
            gy=round(acl.gyro.y)
            gz=round(acl.gyro.z)
            
            #compare new reading to base
            
            #acl
            if ax_base >= ax:
                ax_diff = ax_base - ax
            else:
                ax_diff = ax - ax_base
                
            if ay_base >= ay:
                ay_diff = ay_base - ay
            else:
                ay_diff = ay - ay_base
            
            if az_base >= az:
                az_diff = az_base - az
            else:
                az_diff = az - az_base
            
            #gyro
            if gx_base >= gx:
                gx_diff = gx_base - gx
            else:
                gx_diff = gx - gx_base   
            
            if gy_base >= gy:
                gy_diff = gy_base - gy
            else:
                gy_diff = gy - gy_base
            
            if gz_base >= gz:
                gz_diff = gz_base - gz
            else:
                gz_diff = gz - gz_base
                
            #turn on the board if movement is detected
            if gx_diff > 10:
                on = 1
            elif gy_diff > 10:
                on = 1
            elif gz_diff > 10:
                on = 1
            else:
                on = 0
            
            #if time has been reached
            if wake == boot_time_deci:
                on = 1
            else:
                wake = wake + 1
            
            #sleep for a decisecond
            sleep(0.1)
            
        #sleep(boot_time_sec)
        
        
        #Power the board back up
        
        Power_Button.value(High)
        sleep(0.2)
        Power_Button.value(Low)
        sleep(0.2)
        

if __name__=="__main__":
    main()
