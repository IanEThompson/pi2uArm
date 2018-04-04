import serial
import time

def wait4Response(ser, timeOut):
    """ Waits for a 'line' response from the serial port
        Returns the string response
        If no response after timeOut, returns and empty string
    """
    startTime = time.time()
    Response = ""
    while Response == "" and time.time()- startTime < timeOut:
        if ser.inWaiting() > 0:
            time.sleep(1)
            Response = ser.readline().decode("utf-8")
    return Response

def getResponse(ser):
    """ Returns any data from the serial input buffer
        No waiting, no timeout
    """
    serData=""
    while ser.inWaiting()>0:
        serData =  serData + ser.read(1).decode("utf-8")
    return serData

#Open the uArm serial port
#Note: you may need to change the port /dev/ttyACM0
#if the device is on a different port
uArm = serial.Serial("/dev/ttyACM0",115200, timeout=2)
time.sleep(1)  #pause for a sec

#listen to the port for the uArm boot-up sequence, and print it
print(wait4Response(uArm,10))
print(getResponse(uArm))


print("Moving to start position: G0 X150 Y0 Z0")
uArm.write(("\rG0 X150 Y0 Z0\r").encode("utf-8"))
print("Received: ", wait4Response(uArm, 20))   #wait for response
print(getResponse(uArm))                       #soak up any extra chars


#forever loop
while True:
    #get a line of input from the keyboard and send it to the uArm
    uArmCommand = input("command>")
    print("Sending: ", uArmCommand)
    uArm.write((uArmCommand + "\r").encode("utf-8"))
    
    #print the uArm's response to the screen
    print("Received: ", wait4Response(uArm, 10))   #wait for response
    print(getResponse(uArm))                       #soak up any extra chars
