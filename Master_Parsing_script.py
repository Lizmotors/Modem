import serial
import time
import logging
import datetime


# get current UTC time
now = datetime.datetime.utcnow()

# create log file name with timestamp
log_file = f"Modem_log_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.log"
logging.basicConfig(filename=log_file, level=logging.INFO)
logger = logging.getLogger()
loginfo = str("Modem System Logs | Gauss Moto Inc | ") + \
    str("  Created on : ") + str(datetime.datetime.utcnow())
logger.info(loginfo)

# Define Serial Port
ser = serial.Serial(
    "/dev/ttyUSB3",
    baudrate=9600,
    rtscts=True,
    dsrdtr=True,
    timeout=1)

print("Device is Connected to: " + ser.portstr)


def send(ser, cmd):
    ser.write(cmd)
    # read complete line from serial output
    val = ser.readline(1024)
    while '\\n' not in str(val):         # check if full data is received.
        # This loop is entered only if serial read value doesn't contain \n
        # which indicates end of a sentence.
        # str(val) - val is byte where string operation to check `\\n`
        # can't be performed
        time.sleep(1)                # delay of 1s
        temp = ser.readline()           # check for serial output.
        if not not temp.decode():       # if temp is not empty.
            val = (val.decode() + temp.decode()).encode()
            # requrired to decode, sum, then encode because
            # long values might require multiple passes
    val = val.decode()                  # decoding from bytes
    # stripping leading and trailing spaces.
    val = val.strip()
    output = ''.join(val)

    ser_cell = '+QENG: "servingcell"' in output
    net_info = '+QNWINFO:' in output
    neg_info_inter = '+QENG: "neighbourcell inter"' in output
    neg_info_intra = '+QENG: "neighbourcell intra"' in output
    gps_loc = '+QGPSLOC:' in output

    if gps_loc is True:
        elements = output.split(':')[1].split(',')
        keys = [
            'UTC Time:',
            'Latitude:',
            'Longitude:',
            'HDOP:',
            'Altitude:',
            'Fix:',
            'Course:',
            'Speed (km):',
            'Speed (kn):',
            'date:',
            'Satellites:']
        my_dict = dict(zip(keys, elements))
        print(my_dict.get('state'))
        for key, value in my_dict.items():
            print(key, value)
            if (key, value) != "":
                loginfo = str(datetime.datetime.utcnow()) + \
                    ":" + str(key) + ":" + str(value)
                logger.info(loginfo)

    if ser_cell is True:
        elements = output.split(':')[1].split(',')
        # print(elements)
        keys = [
            'Topic:',
            'Connection State:',
            'Acess_Tech:',
            'FDD/TDD:',
            'MCC:',
            'MNC:',
            'CellID:',
            'PCID:',
            'EARFCN:',
            'FBI:',
            'UL_BW:',
            'DL_BW:',
            'TAC:',
            'RSRP:',
            'RSCP:',
            'RSRQ:',
            'RSSI:',
            'SINR:',
            'CQI:',
            'TX-Power:',
            'SRxlev:']
        my_dict = dict(zip(keys, elements))
        print(my_dict.get('state'))
        for key, value in my_dict.items():
            print(key, value)
            if (key, value) != "":
                loginfo = str(datetime.datetime.utcnow()) + \
                    ":" + str(key) + ":" + str(value)
                logger.info(loginfo)

    if net_info is True:
        elements = output.split(':')[1].split(',')
        # print(elements)
        keys = ['Acess_Tech:', 'Operator:', 'Band:', 'Channel:']
        my_dict = dict(zip(keys, elements))
        print(my_dict.get('state'))
        for key, value in my_dict.items():
            print(key, value)
            if (key, value) != "":
                loginfo = str(datetime.datetime.utcnow()) + \
                    ":" + str(key) + ":" + str(value)
                logger.info(loginfo)

    if neg_info_inter is True:
        elements = output.split(':')[1].split(',')
        # print(elements)
        keys = [
            'Topic:',
            'Acess_Tech:',
            'EARFCN',
            'PCID:',
            'RSRQ:',
            'RSRP:',
            'RSSI:',
            'SINR:',
            'srxlev:',
            'Cell_resel_priority:',
            'threshold_Xlow:',
            'threshold_Xhigh:']
        my_dict = dict(zip(keys, elements))
        print(my_dict.get('state'))
        for key, value in my_dict.items():
            print(key, value)
            if (key, value) != "":
                loginfo = str(datetime.datetime.utcnow()) + \
                    ":" + str(key) + ":" + str(value)
                logger.info(loginfo)

    if neg_info_intra is True:
        elements = output.split(':')[1].split(',')
        # print(elements)
        keys = [
            'Topic:',
            'Acess_Tech:',
            'EARFCN',
            'PCID:',
            'RSRQ:',
            'RSRP:',
            'RSSI:',
            'SINR:',
            'srxlev:',
            'Cell_resel_priority:',
            's_non_intra_search',
            'thresh_serv_low:',
            's_intra_search:']
        my_dict = dict(zip(keys, elements))
        print(my_dict.get('state'))
        for key, value in my_dict.items():
            print(key, value)
            if (key, value) != "":
                loginfo = str(datetime.datetime.utcnow()) + \
                    ":" + str(key) + ":" + str(value)
                logger.info(loginfo)
    else:

        print(val)
        loginfo = str(datetime.datetime.utcnow()) + ":" + str(val)
        logger.info(loginfo)


# Enable GPS

def gps_enable(ser):
    send(ser, b'AT+QGPS=1\r')


def gps_nmea(ser):
    send(ser, b'AT+QGPSCFG="gpsnmeatype",31\r')

# Device information (Static)"


def device_info(ser):
    send(ser, b'ATI\r')


def device_serial(ser):
    send(ser, b'AT+CGSN\r')


def device_imei(ser):
    send(ser, b'AT+CIMI\r')


def device_iccid(ser):
    send(ser, b'AT+QCCID\r')


def sw_version(ser):
    send(ser, b'CGMR\n')


# Device Configuration information (Static)"
def apn_information(ser):
    send(ser, b'AT+CGDCONT?\r')


def ip_information(ser):
    send(ser, b'AT+CGPADDR=1\r')

# Device Location Information(Dynamic)"


def gps_location(ser):
    send(ser, b'AT+QGPSLOC=2\r')

# Device Network Information(Dynamic)"


def network_info(ser):
    send(ser, b'AT+QNWINFO\r')


def servingcell_info(ser):
    send(ser, b'AT+QENG="servingcell"\r')


def neighbourcell_info(ser):
    send(ser, b'AT+QENG="neighbourcell"\r')


def data_packets(ser):
    send(ser, b'AT+QGDCNT?\r')


print("Device Information:\n")
gps_enable(ser)
gps_nmea(ser)
device_info(ser)
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
