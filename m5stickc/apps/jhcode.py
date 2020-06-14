from m5stack import *
from m5ui import *
from uiflow import *
import hat
lcd.setRotation(1)
import hat
import machine
from machine import Timer
import wifiCfg
from m5mqtt import M5mqtt
import json
import apps.util
import apps.constants

hat_env0 = hat.get(hat.ENV)
CurrentPage = 0
isDataSent = False
m5mqtt = None
CycleTimer = None
CycleTimeout = None
TOPIC_ACK = "sensor-ack"

def main():
    # init
    setScreenColor(0x000000)
    axp.setLcdBrightness(50)
    M5Led.on()
    wifiCfg.doConnect('GrandpaFoo', '62573969')
    M5Led.off()
    showPage0()

def showPage0():
    lcd.clear()
    lcd.print('TTemp', 3, 0, 0xffffff)
    lcd.print((hat_env0.temperature), 80, 0, 0xffffff)
    lcd.print('Humi', 3, 15, 0xffffff)
    lcd.print(apps.util.DeviceId(), 50, 15, 0xffffff)
    # lcd.print((hat_env0.humidity), 80, 15, 0xffffff)
    lcd.print('Batt volt', 3, 30, 0xffffff)
    lcd.print((axp.getBatVoltage()), 80, 30, 0xffffff)
    lcd.print('VBus Cur', 3, 45, 0xffffff)
    lcd.print((axp.getVBusCurrent()), 80, 45, 0xffffff)
    lcd.print('Batt cur', 3, 60, 0xffffff)
    lcd.print((axp.getBatCurrent()), 80, 60, 0xffffff)

def onIncomingTopicMsg(topic_data):
    global isDataSent, CycleTimer, CycleTimeout
    data = json.loads(topic_data)
    print (TOPIC_ACK, ": ", data["DeviceId"])
    print ("DeviceId: ", apps.util.DeviceId())
    if (isDataSent and data["DeviceId"] == apps.util.DeviceId()):
        CycleTimeout.deinit()
        M5Led.off()
        isDataSent = False
        # machine.lightsleep( 3 * 1000)
        CycleTimer = Timer(-1)
        CycleTimer.init(period=apps.constants.CYCLE_DURATION_MS, mode=Timer.ONE_SHOT, callback=onCycleTimer)

def onCycleTimer(timer):
    global CycleTimeout
    # watchdog to restart if cycle does not complete within max duration
    CycleTimeout = Timer(-1)
    CycleTimeout.init(period=30 * 1000, mode=Timer.ONE_SHOT, callback=onCycleTimeout)
    sendTelemetry()

def onCycleTimeout(timer):
    machine.reset()

def sendTelemetry():
    global isDataSent, m5mqtt
    try:
        M5Led.on()
        data = {
            "TempCel": hat_env0.temperature,
            "HumiPercent": hat_env0.humidity,
            "DeviceId": apps.util.DeviceId()
        }
        isDataSent = True
        m5mqtt.publish('sensor-data',json.dumps(data))
    except Exception as err:
        print (err)
        

def showPage1():
    global isDataSent, m5mqtt
    # turn off lcd power
    axp.setLDO2Volt(0)
    m5mqtt = M5mqtt('umqtt_client', apps.constants.MQTT_SERVER, apps.constants.MQTT_PORT, '', '', 300)
    m5mqtt.subscribe(str(TOPIC_ACK), onIncomingTopicMsg)
    m5mqtt.start()
    onCycleTimer(None)
    # lcd.clear()
    # lcd.image(0, 0, 'res/heart.jpg')


def changePage():
    global CurrentPage
    print (CurrentPage)
    if (CurrentPage == 0):
        CurrentPage = 1
        showPage1()
    else:
        CurrentPage = 0
        showPage0()

btnA.wasPressed(changePage)



