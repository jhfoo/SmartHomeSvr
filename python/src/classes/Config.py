import yaml

_config = None

def getValue(path: str):
  global _config
  if _config is None:
    with open('conf/app.yaml', 'r') as f:
      _config = yaml.safe_load(f)
  
  keys = path.split('.')
  value = _config
  for key in keys:
    value = value.get(key)
    if value is None:
      return None
  return value