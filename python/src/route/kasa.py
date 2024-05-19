# core
import asyncio

# community
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict
import kasa

# custom
from src.classes.KasaDeviceCache import KasaDeviceCache

router = APIRouter(
  prefix = '/kasa'
)

async def init():
  return asyncio.create_task(kasa.Discover.discover(
    on_discovered=updateDeviceCache
  ))

async def updateDeviceCache(device):
  print (f'[kasa] discovered device: {device.alias}')
  KasaDeviceCache.addDevice(device)


def getDeviceAsDict(device):
  return {
    'alias': device.alias,
    'hardware': device.hw_info,
    'state': device.state_information,
    'host': device.host,
    'hasMeter': device.has_emeter
  }

@router.get('/device/get')
async def getDevice(ip: str = None, alias: str = None):
  device = None

  if ip:
    device = KasaDeviceCache.getDeviceByIp(ip)
    if not device:
      raise HTTPException (
        status_code=400,
        detail = f'Unknown device at "{ip}"'
      )
  elif alias:
    device = KasaDeviceCache.getDeviceByAlias(alias)
    if not device:
      raise HTTPException (
        status_code=400,
        detail = f'Unknown device alias "{alias}"'
      )

  # else
  return getDeviceAsDict(device) 

@router.get('/device/list')
async def getDevices():
  ret = {}
  for device in KasaDeviceCache.devices():
    await asyncio.create_task(device.update())
    ret[device.alias] = getDeviceAsDict(device) 

  return ret

@router.get('/discover')
async def findDevices():
  print ('/discover')
  devices = await init()
  ret = []
  print (f'Discovered devices: {len(devices)}')
  for device in KasaDeviceCache.devices():
    ret.append(device.alias)

  return ret

@router.post('/device/command')
async def setDevice(evt : dict):
  KEY_DEVICE_ALIAS = 'DeviceAlias'

  print (evt)
  if not KEY_DEVICE_ALIAS in evt:
    raise HTTPException (
      status_code=400,
      detail = 'Missing DeviceAlias'
    )

  DeviceAlias = evt[KEY_DEVICE_ALIAS]
  TargetDevice = await KasaDeviceCache.getDeviceByAlias(DeviceAlias, isUpdate = True)
  if not TargetDevice:
    raise HTTPException (
      status_code=400,
      detail = f'Unknown device alias "{DeviceAlias}"'
    )

  if 'cmd' in evt:
    await KasaDeviceCache.doCommand(TargetDevice, evt['cmd'])
    return getDeviceAsDict(TargetDevice)

  return TargetDevice.device_type