# core
import asyncio

# community
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict
import kasa

DiscoveredDevices = {}

router = APIRouter(
  prefix = '/kasa'
)

async def init():
  return asyncio.create_task(kasa.Discover.discover(
    on_discovered=updateDeviceCache
  ))

async def updateDeviceCache(device):
  print (f'[kasa] discovered device: {device.alias}')
  DiscoveredDevices[device.alias] = device

@router.get('/discover')
async def getDevices():
  print ('/discover')
  devices = await asyncio.create_task(kasa.Discover.discover(
    on_discovered=updateDeviceCache
  ))
  ret = []
  print (f'Discovered devices: {len(devices)}')
  for DeviceIpKey in devices:
    DiscoveredDevices[devices[DeviceIpKey].alias] = devices[DeviceIpKey]
    ret.append(devices[DeviceIpKey].alias)

  return ret

@router.post('/device')
async def setDevice(evt : dict):
  KEY_DEVICE_ALIAS = 'DeviceAlias'

  print (evt)
  if not KEY_DEVICE_ALIAS in evt:
    raise HTTPException (
      status_code=400,
      detail = 'Missing DeviceAlias'
    )

  DeviceAlias = evt[KEY_DEVICE_ALIAS]
  if not DeviceAlias in DiscoveredDevices.keys():
    raise HTTPException (
      status_code=400,
      detail = f'Unknown device alias "{DeviceAlias}"'
    )

  TargetDevice = DiscoveredDevices[DeviceAlias]
  # get the latest state
  await asyncio.create_task(TargetDevice.update())

  if 'cmd' in evt:
    ret = None
    if 'power' in evt['cmd']:
      if evt['cmd']['power'] == 'on':
        print ('[kasa] power on')
        ret = await asyncio.create_task(DiscoveredDevices[DeviceAlias].turn_on()) 
      elif evt['cmd']['power'] == 'toggle':
        print (f'Device power state: {"on" if TargetDevice.is_on else "off"}')
        if TargetDevice.is_on:
          await asyncio.create_task(TargetDevice.turn_off())
          await asyncio.create_task(TargetDevice.update())
        else:
          await asyncio.create_task(TargetDevice.turn_on())
          await asyncio.create_task(TargetDevice.update())
      else:
        print ('[kasa] power off')
        ret = await asyncio.create_task(DiscoveredDevices[DeviceAlias].turn_off())

      return ret
    else:
      raise HTTPException (
        status_code=400,
        detail = f'Unknown command {evt["cmd"]}'
      )

  return DiscoveredDevices[DeviceAlias].device_type