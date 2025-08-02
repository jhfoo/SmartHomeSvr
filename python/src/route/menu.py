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
  for menu in FullMenu:
    if 'devices' in menu:
      for MenuDevice in menu['devices']:
        if 'mac' in MenuDevice:
          device = await KasaDeviceCache.getDeviceByMac(MenuDevice['mac'], True)
          if not device is None:
            MenuDevice['alias'] = device.alias
            MenuDevice['isOn'] = device.is_on
          else:
            print(f"Device not found for mac: {MenuDevice['mac']}")
    print (device.mac)
  return FullMenu