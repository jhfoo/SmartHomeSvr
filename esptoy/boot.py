import machine
import constants
import telemetry
import util
import init

# create watchdog for init phase
alarm = machine.Timer(1)
alarm.init(period=constants.INIT_TIMEOUT, mode=machine.Timer.ONE_SHOT, callback=init.initTimeout)

# Init device
init.initLeds()
init.initWifi()
init.initTime()

# made it this far: stop the timer!
init.stopBlinker()
alarm.deinit()

def MainLoop():
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

MainLoop()

