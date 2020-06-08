import utime
import ubinascii
import machine
import lib.constants

def getDevice():
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')

def getFormattedDateTime():
    local = utime.time() + lib.constants.NTP_TZ * 3600
    now = utime.localtime(local)
    return '{:04d}{:02d}{:02d}-{:02d}{:02d}{:02d}'.format(now[0], now[1], now[2], now[3], now[4], now[5])

def isFileExist(filename):
    try:
        TestFile = open(filename, 'r')
        TestFile.close()
        return True
    except OSError:
        return False

def logError(message):
    OutFile = open(lib.constants.FNAME_ERROR, 'w')
    OutFile.write(message)
    OutFile.close()
