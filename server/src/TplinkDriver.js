tplink = require('tplink-smarthome-api')  

module.exports = {
  getDeviceStates: getDeviceStates,
  setState: setDeviceState,
  getMetrics: getMetrics,
}

const models = {
  'HS103(US)': {
    states: ['power'],
  },
  'KP115(US)': {
    states: ['power'],
  }
}

async function getMetrics(ctx, DeviceId, config) {
  const states = await getDeviceStates(ctx, DeviceId, config)
  // ctx.broker.logger.debug(`Raw info for ${DeviceId}:\n${JSON.stringify(states, null, 2)}`)
  
  try {
    if ('power' in states.emeter.realtime) {
      // ctx.broker.logger.debug(`Metric 'power' for ${DeviceId}: ${states.emeter.realtime.power}`)    
      ctx.params.metrics.energy.set({
        device: DeviceId,
      }, states.emeter.realtime.power)
    }
  
    if ('relay_state' in states.sysInfo) {
      // ctx.broker.logger.debug(`Metric 'PowerRelay' for ${DeviceId}: ${states.sysInfo.relay_state}`)    
      ctx.params.metrics.PowerRelay.set({
        device: DeviceId,
      }, states.sysInfo.relay_state)
    }
  } catch (err) {
    ctx.broker.logger.error('Error in TplinkDriver.getMetrics()') 
    ctx.broker.logger.error(err)    
  }

}

async function getDeviceStates(ctx, DeviceId, config) {
  let driver = new tplink.Client()
  let device = await driver.getDevice({
    host: config.ip
  })

  const states = await device.getInfo()
  // ctx.broker.logger.debug(`states: ${JSON.stringify(states, null, 2)}`)    

  return states
}

async function setDeviceState(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug(`TplinkDriver.setDeviceState: ${DeviceId}, ${ctx.params.StateName}, ${ctx.params.StateValue}`)
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
