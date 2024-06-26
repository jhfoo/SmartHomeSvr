# core
import asyncio

class KasaDeviceCache:
  _DeviceCache = {}

  @staticmethod
  def addDevice(device):
    KasaDeviceCache._DeviceCache[device.alias] = device

  @staticmethod
  def devices():
    return KasaDeviceCache._DeviceCache.values()

  @staticmethod
  async def getDeviceByAlias(alias:str, isUpdate: bool = False):
    if alias in KasaDeviceCache._DeviceCache:
      device = KasaDeviceCache._DeviceCache[alias]
      if isUpdate:
        await asyncio.create_task(device.update())
      return device
    else:
      return None

  @staticmethod
  def getDeviceByIp(IpAddr:str):
    for device in KasaDeviceCache.devices():
      if device.host == IpAddr:
        return device

    return None

  @staticmethod
  async def doCommand(device, cmd: dict):
    if 'power' in cmd:
      ret = None
      if cmd['power'] == 'on':
        print ('[kasa] power on')
        ret = await asyncio.create_task(device.turn_on()) 
      elif cmd['power'] == 'toggle':
        print (f'Device power state: {"on" if device.is_on else "off"}')
        if device.is_on:
          await asyncio.create_task(device.turn_off())
          ret = await asyncio.create_task(device.update())
        else:
          await asyncio.create_task(device.turn_on())
          ret = await asyncio.create_task(device.update())
      else:
        print ('[kasa] power off')
        ret = await asyncio.create_task(device.turn_off())

      return ret
    else:
      return None