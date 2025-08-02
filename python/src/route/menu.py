# core
import copy

# community
from fastapi import APIRouter
import yaml

# custom
from src.classes.KasaDeviceCache import KasaDeviceCache

router = APIRouter(
  prefix = '/menu'
)

_menu = None

async def init():
  global _menu
  with open("conf/menu.yaml", "r") as f:
    _menu = yaml.safe_load(f)
    print(_menu)
    return _menu

@router.get('/reload')
async def reloadMenu():
  return (await init())

@router.get('/all')
async def ping():
  """
  Fetches and returns a deep copy of the menu configuration, augmenting device entries
  with additional information from KasaDeviceCache.

  For each device in the menu, it attempts to retrieve the device's alias and power state
  using its MAC address. If a device is found, its alias and power state are added to the 
  menu device entry. If not found, a message is printed indicating the missing device.

  Returns:
      list: A deep copy of the menu with updated device information.
  """
  FullMenu = copy.deepcopy(_menu)
  for room in FullMenu['rooms']:
    print (room)
    if 'devices' in room:
      for MenuDevice in room['devices']:
        if 'mac' in MenuDevice:
          device = await KasaDeviceCache.getDeviceByMac(MenuDevice['mac'], True)
          if not device is None:
            MenuDevice['alias'] = device.alias
            MenuDevice['isOn'] = device.is_on
          else:
            print(f"Device not found for mac: {MenuDevice['mac']}")
  return FullMenu