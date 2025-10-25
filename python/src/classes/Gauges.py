# community
from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

class Gauges:
  def __init__(self, registry: CollectorRegistry = None):
    self._gauges = {}

    if registry is None:
      self.registry = CollectorRegistry()
    else:
      self.registry = registry

  def getGauge(self, name: str) -> Gauge:
    if not name in self._gauges:
      self._gauges[name] = Gauge(name, f'Gauge for {name}', ['DeviceId'], registry=self.registry)

    return self._gauges[name]
  
  def generate(self):
    return generate_latest(self.registry).decode('utf-8')