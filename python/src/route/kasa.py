# core
import asyncio

# community
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict
import kasa

# custom
from src.classes.KasaDeviceCache import KasaDeviceCache
import classes.Config as Config
import classes.KasaManager as KasaManager

router = APIRouter(
  prefix = '/kasa'
)



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
  return KasaManager.getDeviceAsDict(device) 

@router.get('/device/list')
async def getDevices():
  ret = {}
  for device in KasaDeviceCache.devices():
    print (f'Updating device: {device.alias}')
    await asyncio.create_task(device.update())
    ret[device.alias] = KasaManager.getDeviceAsDict(device) 

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
    return KasaManager.getDeviceAsDict(TargetDevice)

  return TargetDevice.device_type