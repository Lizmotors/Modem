import serial
import time
import logging
import datetime


# get current UTC time
now = datetime.datetime.utcnow()

# create log file name with timestamp
log_file = f"Modem_log_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.log"
logging.basicConfig(filename=log_file,level=logging.INFO)
logger = logging.getLogger()
loginfo = str("Modem System Logs | Gauss Moto Inc | ") + str("  Created on : ") + str(datetime.datetime.utcnow()) 
logger.info(loginfo)

#Define Serial Port
ser = serial.Serial("/dev/ttyUSB3", baudrate=9600,rtscts=True, dsrdtr=True,timeout=1)

print("Device is Connected to: " + ser.portstr)

def send(ser, cmd):
    ser.write(cmd)
    val = ser.readline(1024)                # read complete line from serial output
    while not '\\n'in str(val):         # check if full data is received. 
        # This loop is entered only if serial read value doesn't contain \n
        # which indicates end of a sentence. 
        # str(val) - val is byte where string operation to check `\\n` 
        # can't be performed
        time.sleep(1)                # delay of 1s 
        temp = ser.readline()           # check for serial output.
        if not not temp.decode():       # if temp is not empty.
            val = (val.decode()+temp.decode()).encode()
            # requrired to decode, sum, then encode because
            # long values might require multiple passes
    val = val.decode()                  # decoding from bytes
    val = val.strip()                   # stripping leading and trailing spaces.
    print(val)
    if val != "":
        loginfo = str(datetime.datetime.utcnow())+ ":"+ str(val)
        logger.info(loginfo)
        
    
#Device information (Static)"
    
def device_info(ser):
    send(ser,b'ATI\r')
    
def device_serial(ser):
    send(ser,b'AT+CGSN\r')

def device_imei(ser):
    send(ser,b'AT+CIMI\r')
    
def device_iccid(ser):
    send(ser,b'AT+QCCID\r')
    
def sw_version(ser):
    send(ser,b'CGMR\n')


#Device Configuration information (Static)"
def apn_information(ser):
    send(ser,b'AT+CGDCONT?\r')
    

def ip_information(ser):
    send(ser,b'AT+CGPADDR=1\r')
    

#Device Location Information(Dynamic)"
    
def gps_location(ser):
    send(ser,b'AT+QGPSLOC=2\r')
    

#Device Network Information(Dynamic)"
def network_info(ser):
    send(ser,b'AT+QNWINFO\r')

def servingcell_info(ser):
    send(ser,b'AT+QENG="servingcell"\r')
    
def neighbourcell_info(ser):
    send(ser,b'AT+QENG="neighbourcell"\r')
    
def data_packets(ser):
    send(ser,b'AT+QGDCNT?\r')


print("Device Information:\n")
device_info= device_info(ser)
device_serial(ser)
device_imei(ser)
device_iccid(ser)
sw_version(ser)
apn_information(ser)

while True:                             # runs this loop forever
    time.sleep(1)
    network_info(ser)
    ip_information(ser)
    servingcell_info(ser)
    neighbourcell_info(ser)
    data_packets(ser)
    gps_location(ser)

ser.close()
    
