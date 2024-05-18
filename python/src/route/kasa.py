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
  print (device.device_type)

@router.get('/discover')
async def getDevices():
  print ('/discover')
  devices = await asyncio.create_task(kasa.Discover.discover(
    on_discovered=updateDeviceCache
  ))
  ret = []
  for DeviceIpKey in devices:
    DiscoveredDevices[devices[DeviceIpKey].alias] = devices[DeviceIpKey]
    ret.append(devices[DeviceIpKey].alias)

  return ret

@router.post('/device')
def setDevice(cmd : dict):
  KEY_DEVICE_ALIAS = 'DeviceAlias'

  print (cmd)
  if not KEY_DEVICE_ALIAS in cmd:
    raise HTTPException (
      status_code=400,
      detail = 'Missing DeviceAlias'
      )

  DeviceAlias = cmd[KEY_DEVICE_ALIAS]
  if not DeviceAlias in DiscoveredDevices.keys():
    raise HTTPException (
      status_code=400,
      detail = f'Unknown device alias "{DeviceAlias}"'
      )

  return DiscoveredDevices[DeviceAlias].device_type