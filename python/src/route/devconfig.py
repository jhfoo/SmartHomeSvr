from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import yaml

# custom
from classes.DevConfig import DevConfig

router = APIRouter(
  prefix="/devconfig",
)

@router.get('/')
def root(make: str = None, model: str = None, id: str = None):
  return DevConfig.getConfig(make = make, model = model, id = id)

@router.get('/reload')
def reload():
  DevConfig.loadConfig()
  return { 'status': 'ok' }