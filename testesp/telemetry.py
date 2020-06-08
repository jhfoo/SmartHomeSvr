import dht
import json
import utime
import machine
import os
import constants
import ubinascii
from umqtt.simple import MQTTClient
import util

def doCycle():
    led = machine.Pin(constants.PIN_REDLED, machine.Pin.OUT)
    led.on()

    # opportunity to break cycle
    btn = machine.Pin(0, machine.Pin.IN)
    if (btn.value() == 0):
        print ("*** GPIO0 pressed ***")
        led.off()
        return None

    # commited to exec cycle
    alarm = machine.Timer(-1)
    # cycle must finish within CYCLE_TIMEOUT, else CycleTimeout()
    alarm.init(period=constants.CYCLE_TIMEOUT, mode=machine.Timer.ONE_SHOT, callback=CycleTimeout)

    MqClient = MQTTClient('umqtt_client', constants.MQTT_SVR)
    print ("[MQTT] Connecting...")
    MqClient.connect()
    print ("[MQTT] Connected")
    if (util.isFileExist(constants.FNAME_ERROR)):
        print ("[MQTT] Publishing last error...")
        Infile = open(constants.FNAME_ERROR)
        ErrorMsg = Infile.read()
        Infile.close()
        MqClient.publish(constants.MQTT_TOPICERROR, ErrorMsg)
        os.remove(constants.FNAME_ERROR)

    print ("[MQTT] Publishing data...")
    MqClient.publish(constants.MQTT_TOPIC,json.dumps(getTelemetry()))
    MqClient.disconnect()
    print ("[MQTT] Disconnected")
    # made it this far: stop the timer!
    alarm.deinit()

    led.off()
    print ("Sleeping...")
    machine.lightsleep(constants.SLEEP_DURATION)
    return 1

# sometimes shit happens: mqtt server doesn't respond, wifi connection lost
# this timeout addresses intermittent issues by logging the incident and doing a soft reset
def CycleTimeout(timer):
    print ('[CycleTimeout] Timeout triggered')
    util.logError(util.getFormattedDateTime() + ', CycleTimeout() called (CYCLE_TIMEOUT = ' + str(constants.CYCLE_TIMEOUT) + ')')
    machine.reset()

def getTelemetry():
    dht22 = dht.DHT22(machine.Pin(constants.PIN_DHT22))
    dht22.measure()

    MqttData = {
        "DeviceId": util.getDevice(),
        "DateTime": util.getFormattedDateTime(),
        "TempCel": str(dht22.temperature()),
        "HumiPercent": str(dht22.humidity())
    }
    print ("Temp (Cel): " + str(dht22.temperature()))
    print ("Humidity (%): " + str(dht22.humidity()))
    return MqttData
