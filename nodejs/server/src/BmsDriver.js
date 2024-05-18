const axios = require('axios'),
  BMS = require('./BmsConst')

module.exports = {
  getDeviceStates: getDeviceStates,
  setState: setDeviceState,
}

const MIN_CAPACITY = 100,
  MIN_BATTERY_VOLTAGE = 2.9

async function getDeviceStates(ctx, DeviceId, config) {
  if (!('state' in config)) {
    config.state = BMS.STATE_NORMAL
  }

  const resp = await axios.get(`http://${config.ip}:8000`)

  return resp.data.split('\n').reduce((final, line) => {
    let matches = line.match(/^BatteryVoltage\S+\s+([\d\.]+)$/)
    if (matches) {
      const BatteryVoltage = parseFloat(matches[1])
      if (BatteryVoltage > final.BatteryVoltageMax) {
        final.BatteryVoltageMax = BatteryVoltage
      } 
      if (BatteryVoltage < final.BatteryVoltageMin) {
        final.BatteryVoltageMin = BatteryVoltage
      }
      // if (BatteryVoltage <= MIN_BATTERY_VOLTAGE
      //   && !IgnoredEvents.includes('undervoltage')) {
      //   // undervoltage: stop power to main from battery
      //   ctx.broker.call('devicemanager.setState', {
      //     StateName: 'power',
      //     StateValue: 'off',
      //   })
      //   IgnoredEvents.push('undervoltage')
      // }
      // ctx.broker.logger.debug(`Device state: ${final}`)
      return final
    }

    matches = line.match(/^capacity{type="rated"}\s+([\d\.]+)$/)
    if (matches) {
      // ctx.broker.logger.debug(matches[1])
      final.capacity = parseFloat(matches[1])
      
      // if (CapacityAH <= MIN_CAPACITY
      //   && !IgnoredEvents.includes('undervoltage')) {
      //   // undervoltage: stop power to main from battery
      //   ctx.broker.call('devicemanager.setState', {
      //     DeviceId: 'SolarMainsSwitch',
      //     StateName: 'power',
      //     StateValue: 'off',
      //   })
      //   IgnoredEvents.push('undervoltage')
      // }
      return final
    }

    // else
    return final
  }, {
    BatteryVoltageMax: 0,
    BatteryVoltageMin: 1000,
    state: config.state,
  })
}

async function setDeviceState(ctx, DeviceId, config) {
}
