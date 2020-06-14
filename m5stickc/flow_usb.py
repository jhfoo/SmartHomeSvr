from m5stack import *
import m5base
import m5ucloud

lcd.clear()
__VERSION__ = m5base.get_version()
# Reset apikey
if btnB.isPressed():
    try:
        machine.nvs_erase('apikey.pem')
    except:
        pass
        
# apikey qrcode
lcd.clear(lcd.BLACK)
lcd.font(lcd.FONT_Default)
lcd.setTextColor(lcd.WHITE, lcd.BLACK)
lcd.print(__VERSION__, lcd.CENTER, 5)

lcd.font(lcd.FONT_DejaVu18)
lcd.setTextColor(0xaaaaaa, lcd.BLACK)
lcd.println("APIKEY", lcd.CENTER, 25)
lcd.print(apikey[:3], lcd.CENTER, 50, color=lcd.ORANGE)
lcd.print(apikey[3:], lcd.CENTER, 65, color=lcd.ORANGE)
lcd.image(16, 95, 'img/1-1.jpg')

cloud = m5ucloud.M5UCloud()
cloud.run()