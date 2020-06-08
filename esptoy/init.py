import network
import machine
import ntptime
import utime
import util
import constants

GreenLed = machine.Pin(constants.PIN_GREENLED, machine.Pin.OUT)
BlueLed = machine.Pin(constants.PIN_BLUELED, machine.Pin.OUT)
blinker = machine.Timer(2)
BLINK_TIMEOUT = 1 * 1000
isBlinkerOn = True

def initLeds():
    global GreenLed
    print ('')
    GreenLed.off()
    # starts blinker
    blinker.init(period=BLINK_TIMEOUT, mode=machine.Timer.PERIODIC, callback=onToggleBlinker)

def onToggleBlinker(ThisTimer):
    global isBlinkerOn
    isBlinkerOn = not isBlinkerOn
    if (isBlinkerOn):
        BlueLed.on()
    else:
        BlueLed.off()

def stopBlinker():
    BlueLed.off()
    blinker.deinit()

def initWifi():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    if sta_if.isconnected():
        print ('Already connected to wireless')
    else:
        # Wifi: connect to AP
        print ('Connecting to wireless...')
        sta_if.active(True)
        ap_if.active(False)
        sta_if.connect(constants.WIFI_SSID, constants.WIFI_PWD)
        while not sta_if.isconnected():
            pass
    print ('Network: ', sta_if.ifconfig())

def initTime():
    ntptime.host = constants.NTP_SERVER
    ntptime.settime()
    local = utime.time() + constants.NTP_TZ * 3600
    print ("Local time after synchronization：%s" %str(utime.localtime(local)))

def initTimeout(timer):
    print ('[INIT_TIMEOUT] Timeout triggered')
    util.logError(util.getFormattedDateTime() + ', InitTimeout() called (INIT_TIMEOUT = ' + str(constants.INIT_TIMEOUT) + ')')
    machine.reset()