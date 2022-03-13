tplink = require('tplink-smarthome-api')  

module.exports = {
  getDeviceStates: getDeviceStates,
  setState: setDeviceState,
}

const models = {
  'HS103(US)': {
    states: ['power'],
  }
}

async function getDeviceStates(ctx, DeviceId, config) {
  let driver = new tplink.Client()
  let device = await driver.getDevice({
    host: config.ip
  })

  const states = await device.getInfo()
  ctx.broker.logger.debug(`states: ${states}`)    

  return states
}

async function setDeviceState(ctx, DeviceId, DeviceConfig) {
  let driver = new tplink.Client()
  let device = await driver.getDevice({
    host: DeviceConfig.ip
  })
  let DeviceInfo = await device.getSysInfo()

  // validate model is in capability config
  if (!(DeviceInfo.model in models)) {
    ctx.broker.logger.error(`Unknown model capability: ${DeviceInfo.model}`)
    return
  }

  // validate model supports state
  if (!models[DeviceInfo.model].states.includes(ctx.params.StateName)) {
    ctx.broker.logger.error(`Unsupported state for ${DeviceInfo.model}: ${ctx.params.StateName}`)
    return
  }

  switch (ctx.params.StateName) {
    case 'power':
      const NewValue = ctx.params.StateValue === 'on' ? true : false
      ctx.broker.logger.debug(`Setting power value for ${DeviceInfo.model}: ${NewValue}`)
      device.setPowerState(NewValue)
      break
  }
}
