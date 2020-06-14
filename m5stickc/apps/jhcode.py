from m5stack import *
from m5ui import *
from uiflow import *
import hat
lcd.setRotation(1)
import hat
import machine
import wifiCfg
from m5mqtt import M5mqtt
import json
import util

hat_env0 = hat.get(hat.ENV)
CurrentPage = 0
isDataSent = False

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
    lcd.print(ubinascii.hexlify(machine.unique_id()).decode('utf-8'), 50, 15, 0xffffff)
    # lcd.print((hat_env0.humidity), 80, 15, 0xffffff)
    lcd.print('Batt volt', 3, 30, 0xffffff)
    lcd.print((axp.getBatVoltage()), 80, 30, 0xffffff)
    lcd.print('VBus Cur', 3, 45, 0xffffff)
    lcd.print((axp.getVBusCurrent()), 80, 45, 0xffffff)
    lcd.print('Batt cur', 3, 60, 0xffffff)
    lcd.print((axp.getBatCurrent()), 80, 60, 0xffffff)

def onIncomingTopicMsg(topic_data):
    data = json.loads(topic_data)
    if (isDataSent and data["DeviceId"] == util.DeviceId()):
        M5Led.off()
        isDataSent = False
    pass


def showPage1():
    lcd.clear()
    lcd.image(0, 0, 'res/heart.jpg')
    m5mqtt = M5mqtt('umqtt_client', '192.168.1.224', 1883, '', '', 300)
    m5mqtt.subscribe(str('sensor-ack'), onIncomingTopicMsg)
    m5mqtt.start()
    DeviceId = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

    M5Led.on()
    data = {
        "TempCel": hat_env0.temperature,
        "HumiPercent": hat_env0.humidity,
        "DeviceId": DeviceId
    }
    isDataSent = True
    m5mqtt.publish('sensor-data',json.dumps(data))

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



