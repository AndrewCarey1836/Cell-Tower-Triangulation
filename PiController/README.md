# Pi Controller

## Main.py
Determines current time and orientation. Then sends 5 signals to the nrf9160 to
collected data from cell towers. Next, the pi pico sends a signal to store the 
collected data to the micro SD card. Finally, it send a low power mode signal 
and waits for a set time or movement to occur before sending a wake signal.

## ds3231.py
Controls the Real Time Clock

## mpu6050.py, imu.py, vector3d.py
Controls the Accelerometer

## ssd1306.py
Controls the Displays