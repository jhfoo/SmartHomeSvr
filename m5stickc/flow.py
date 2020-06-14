import gc, os, binascii
from m5stack import *
from m5cloud import M5Cloud
import unit
import wifiCfg
import m5base
from lib import wifiCfg

wifiCfg.autoConnect(lcdShow=True)

__VERSION__ = m5base.get_version()

if btnB.isPressed():
    try:
        machine.nvs_erase('apikey.pem')
    except:
        pass
        

# Display 
lcd.clear(lcd.BLACK)
lcd.setTextColor(lcd.WHITE, lcd.BLACK)

# apikey qrcode
lcd.font(lcd.FONT_Default)
lcd.print(__VERSION__, lcd.CENTER, 5)
lcd.image(16, 95, 'img/1-3.jpg')


lcd.font(lcd.FONT_DejaVu18)
lcd.setTextColor(0xaaaaaa, lcd.BLACK)
lcd.println("APIKEY", lcd.CENTER, 25)
lcd.print(apikey[:3], lcd.CENTER, 50, color=lcd.ORANGE)
lcd.print(apikey[3:], lcd.CENTER, 65, color=lcd.ORANGE)

m5cloud = M5Cloud()

# Why this work error, look run error..........
gc.collect()
gc.threshold(10*1024)

m5cloud.run(thread=False)
# gc.collect()