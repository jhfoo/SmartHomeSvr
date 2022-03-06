const axios = require('axios')

module.exports = {
  update: getDeviceState,
  setState: setDeviceState,
}

const MIN_CAPACITY = 100,
  MIN_BATTERY_VOLTAGE = 2.9

async function getDeviceState(ctx, DeviceId, config) {
  const resp = await axios.get(`http://${config.ip}:8000`)
  let IgnoredEvents = []

  resp.data.split('\n').forEach((line) => {
    let matches = line.match(/^BatteryVoltage\S+\s+([\d\.]+)$/)
    if (matches) {
      // ctx.broker.logger.debug(matches[1])
      const BatteryVoltage = parseFloat(matches[1])
      if (BatteryVoltage <= MIN_BATTERY_VOLTAGE
        && !IgnoredEvents.includes('undervoltage')) {
        // undervoltage: stop power to main from battery
        ctx.broker.call('devicemanager.setState', {
          StateName: 'power',
          StateValue: 'off',
        })
        IgnoredEvents.push('undervoltage')
      }
      return
    }

    matches = line.match(/^capacity{type="rated"}\s+([\d\.]+)$/)
    if (matches) {
      // ctx.broker.logger.debug(matches[1])
      const CapacityAH = parseFloat(matches[1])
      if (CapacityAH <= MIN_CAPACITY
        && !IgnoredEvents.includes('undervoltage')) {
        // undervoltage: stop power to main from battery
        ctx.broker.call('devicemanager.setState', {
          DeviceId: 'SolarMainsSwitch',
          StateName: 'power',
          StateValue: 'off',
        })
        IgnoredEvents.push('undervoltage')
      }
      return
    }
  })
}

async function setDeviceState(ctx, DeviceId, config) {
}
