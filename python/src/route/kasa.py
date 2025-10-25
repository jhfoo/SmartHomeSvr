# core
import asyncio

# community
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict
from prometheus_client import CollectorRegistry, Gauge, generate_latest

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

@router.get('/metrics')
async def getMetrics():
  metrics = KasaManager.getMetrics()
  registry = CollectorRegistry()
  if KasaManager.KEY_POWER in metrics:
    PowerGauge = Gauge('kasa_power_watts', 'Power usage in watts', ['device'], registry=registry)
    SampleGauge = Gauge('sample_count', 'Power samples', ['device'], registry=registry)
    for device_alias in metrics[KasaManager.KEY_POWER]:
      PowerGauge.labels(device=device_alias).set(metrics[KasaManager.KEY_POWER][device_alias]['average'])
      SampleGauge.labels(device=device_alias).set(metrics[KasaManager.KEY_POWER][device_alias]['count'])

  KasaManager.resetMetrics()
  return Response(content=generate_latest(registry), media_type="text/plain")