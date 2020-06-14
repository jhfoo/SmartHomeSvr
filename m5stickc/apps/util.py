import ubinascii
import machine

def DeviceId():
    return ubinascii.hexlify(machine.unique_id()).decode('utf-8')