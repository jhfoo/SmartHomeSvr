from fastapi import APIRouter

from fastapi.responses import PlainTextResponse

# custom
import store
from classes.Gauges import Gauges
import classes.KasaManager as KasaManager

router = APIRouter(
  prefix="/metrics",
)


  
@router.get('/test')
def test():
  return {"status": "ok"}

@router.get('/', response_class=PlainTextResponse)
def getMetrics():
  with store.devices_lock:
    gauges = Gauges()
    for DeviceId in store.devices.keys():
      device = store.devices[DeviceId]
      for key in device.keys():
        value = device[key]['value']
        g = gauges.getGauge(key)
        g.labels(DeviceId=DeviceId).set(value)


    # reset metrics
    store.devices = {}

  # merge metrics from KasaManager
  metrics = KasaManager.getMetrics()
  for metric in metrics:
    print (f'Merging Kasa metric: {metric}')
    g = gauges.getGauge(metric)
    for DeviceId in metrics[metric].keys():
      if metric == KasaManager.KEY_POWER:
        g.labels(DeviceId=DeviceId).set(metrics[metric][DeviceId][KasaManager.KEY_AVERAGE])
  KasaManager.resetMetrics()
  
  return gauges.generate()

@router.post('/')
def post_metrics(metric: dict):
  print (f'received POST metrics: {metric}')
  with store.devices_lock:
    print (f"Received metric: {metric}")
    if not 'DeviceId' in metric:
      return {"error": "DeviceId is required"}
    
    if not metric['DeviceId'] in store.devices:
      print (f"Creating device {metric['DeviceId']}")
      store.devices[metric['DeviceId']] = {}

    device = store.devices[metric['DeviceId']]
    for key in metric['metrics'].keys():
      value = metric['metrics'][key]
      if not key in device:
        print (f"Creating metric {key} for device {metric['DeviceId']}")
        device[key] = {'value': value, 'count': 1}
      else:
        device[key]['value'] = (device[key]['value'] * device[key]['count'] + value) / (device[key]['count'] + 1)
        device[key]['count'] += 1

      print (f'This {key} = {value}')
      print (f'Avg for {key} = {device[key]["value"]}')
      print (f'{key} = {device[key]["value"]}, {device[key]["count"]}')
    return {"status": "Metric received", "metric": metric}