import network
import machine
import ntptime
import utime
import constants
import telemetry
import util

# Init device
print ('')
GreenLed = machine.Pin(constants.PIN_GREENLED, machine.Pin.OUT)
GreenLed.off()

# Wifi: init
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
ntptime.host = constants.NTP_SERVER
ntptime.settime()
local = utime.time() + constants.NTP_TZ * 3600
print ("Local time after synchronization：%s" %str(utime.localtime(local)))

# Infinite loop
while True:
# for i in range(100 * 1000):
# for i in range(2):
    try:
        if (telemetry.doCycle() is None):
            print ("Aborting normal operations")
            break
    except Exception as err:
        util.logError('Unknown error')
        machine.reset()
