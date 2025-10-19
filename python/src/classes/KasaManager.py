# community
from apscheduler.triggers.interval import IntervalTrigger
import kasa

# custom
from src.classes.KasaDeviceCache import KasaDeviceCache
import classes.Config as Config

async def scanDevices():
  print ('[kasa] scanning for devices...')
  await kasa.Discover.discover(
    target=Config.getValue('ecosystem.kasa.network'),
    # target='192.168.86.255',
    on_discovered=updateDeviceCache,
    username=Config.getValue('ecosystem.kasa.email'),
    password=Config.getValue('ecosystem.kasa.password')
  )

async def readPowerUsage():
  for device in KasaDeviceCache.devices():
    if device.has_emeter:
      await device.update()
      # device = await kasa.Discover.discover_single(device.host,
      #   username=Config.getValue('ecosystem.kasa.email'),
      #   password=Config.getValue('ecosystem.kasa.password')
      # )
      if 'Current consumption' in device.state_information:
        print (f'[kasa] {device.alias} current consumption: {device.state_information["Current consumption"]}')

  
async def init(scheduler):
  await scanDevices()
  scheduler.add_job(scanDevices, IntervalTrigger(seconds=5 * 60))
  scheduler.add_job(readPowerUsage, IntervalTrigger(seconds=5))

async def updateDeviceCache(device):
  print (f'[kasa] discovered device: {device.alias}')
  await device.update()
  print (getDeviceAsDict(device))
  KasaDeviceCache.addDevice(device)

def getDeviceAsDict(device):
  print (device)
  return {
    'alias': device.alias,
    'hardware': device.hw_info,
    'state': device.state_information,
    'host': device.host,
    'hasMeter': device.has_emeter
  }
