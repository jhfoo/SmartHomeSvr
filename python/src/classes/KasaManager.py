# community
from apscheduler.triggers.interval import IntervalTrigger
import kasa

# custom
from src.classes.KasaDeviceCache import KasaDeviceCache
import classes.Config as Config

KEY_POWER = 'power'
KEY_AVERAGE = 'average'

_metrics = {}

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
  global _metrics

  for device in KasaDeviceCache.devices():
    if device.has_emeter:
      await device.update()
      # device = await kasa.Discover.discover_single(device.host,
      #   username=Config.getValue('ecosystem.kasa.email'),
      #   password=Config.getValue('ecosystem.kasa.password')
      # )
      if 'Current consumption' in device.state_information:
        # auto init _metrics
        if KEY_POWER not in _metrics:
          _metrics[KEY_POWER] = {}
        if device.alias not in _metrics[KEY_POWER]:
          _metrics[KEY_POWER][device.alias] = {
            'count': 0,
            'average': 0
          }

        # update average
        power = device.state_information['Current consumption']
        metric = _metrics[KEY_POWER][device.alias]
        metric[KEY_AVERAGE] = (metric[KEY_AVERAGE] * metric['count']) + power
        metric['count'] += 1
        metric[KEY_AVERAGE] = metric[KEY_AVERAGE] / metric['count']
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

def getMetrics():
  global _metrics
  return _metrics

def resetMetrics():
  global _metrics
  _metrics = {}