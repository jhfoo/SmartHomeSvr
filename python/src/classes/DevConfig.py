import copy
import json
import yaml

KEY_DEFAULT = 'default'

class DevConfig:
  _config = None

  @staticmethod
  def init():
    DevConfig.loadConfig()

  @staticmethod
  def loadConfig():
    with open('conf/devices.yaml', 'r') as f:
      DevConfig._config = yaml.safe_load(f)

  @staticmethod
  def deepMerge(dict1, dict2):
    """
    Recursively merge dict2 into dict1.
    """
    merged = copy.deepcopy(dict1)  # Create a deep copy of dict1
    for key, value in dict2.items():
      if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
        # If both values are dictionaries, merge them recursively
        merged[key] = DevConfig.deepMerge(merged[key], value)
      else:
        # Otherwise, overwrite or add the value
        merged[key] = copy.deepcopy(value)

    return merged

  # @staticmethod
  # def getDefaultType(config: dict) -> dict:
  #   for types in config.values()
  #   if 'type' in config:
  #     return config['type']
  #   return 'unknown'
  @staticmethod
  def getConfig(make: str = None, model: str = None, id: str = None):
    print (f"DevConfig.getConfig(): make={make}, model={model}, id={id}")
    ret = {}
    if KEY_DEFAULT in DevConfig._config:
      ret = copy.deepcopy(DevConfig._config[KEY_DEFAULT])

    if make is None:
      # unknown make: return base defaults
      return ret
    
    # make is known
    print (f'[debug] make in DevConfig._config: {make in DevConfig._config}')
    if make in DevConfig._config:
      # merge with make defaults
      if KEY_DEFAULT in DevConfig._config[make]:
        ret = DevConfig.deepMerge(ret, DevConfig._config[make][KEY_DEFAULT])

      # model is unknown
      if model is None:
        return ret
      
      # model is known
      if model in DevConfig._config[make]:
        # merge with model defaults
        if KEY_DEFAULT in DevConfig._config[make][model]:
          ret = DevConfig.deepMerge(ret, DevConfig._config[make][model][KEY_DEFAULT])

        # id is unknown
        if id is None:
          return ret
        
        # id is known
        if id in DevConfig._config[make][model]:
          # merge with id config
          ret = DevConfig.deepMerge(ret, DevConfig._config[make][model][id])

    return ret