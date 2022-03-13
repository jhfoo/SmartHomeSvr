module.exports = {
  getStates: getDeviceStates,
  setState: setDeviceState,
  monitor: monitorDevices,
  prometheus: getMetrics,
  init: init,
}

var DeviceConfig = {},
  DeviceDrivers = {}

function getMetrics(ctx) {
  return 'ok'
}

function init(config) {
  DeviceConfig = config.DeviceConfig
  DeviceDrivers = config.DeviceDrivers
}

async function getDeviceStates(ctx) {
  // validate DeviceId
  if (!(ctx.params.DeviceId in DeviceConfig)) {
    throw new Error(`Invalidate device id: ${ctx.params.DeviceId}`)
  }

  // validate device driver
  const device = DeviceConfig[ctx.params.DeviceId]
  if (!(device.driver in DeviceDrivers)) {
    throw new Error(`Invalidate driver for DeviceId ${ctx.params.DeviceId}: ${device.driver}`)
  }

  return await DeviceDrivers[device.driver].getDeviceStates(ctx, ctx.params.DeviceId, device)
}

async function setDeviceState(ctx) {
  this.logger.debug(`setDeviceState: id = ${ctx.params.DeviceId}, ${ctx.params.StateName} = ${ctx.params.StateValue}`)
  if (!(ctx.params.DeviceId in DeviceConfig)) {
    ctx.broker.logger.error(`Unknown DeviceId: ${ctx.params.DeviceId}`)
    return
  }

  const TargetDevice = DeviceConfig[ctx.params.DeviceId]
  if (TargetDevice.driver in DeviceDrivers) {
    await DeviceDrivers[TargetDevice.driver].setState(ctx, ctx.params.DeviceId, TargetDevice)
  } else {
    throw new Error(`Unknown driver: ${TargetDevice.driver}`)
  }
}

async function monitorDevices(ctx) {
  ctx.broker.logger.debug(`monitorDevices: executing`)

  let DeviceIds = Object.keys(DeviceConfig)

  for (let idx = 0; idx < DeviceIds.length; idx++) {
    try {
      let DeviceId = DeviceIds[idx]
      if (DeviceConfig[DeviceId].isMonitor) {
        // device configured to be monitored
        // ctx.broker.logger.debug(`Device to be monitored: ${DeviceId}`)
        let DeviceDriver = DeviceConfig[DeviceId].driver
        if (DeviceDriver in DeviceDrivers) {
          // driver for device exists
          await DeviceConfig[DeviceId].onMonitor(ctx, DeviceId, DeviceConfig[DeviceId])
        } else {
          throw new Error(`Unknown driver: ${DeviceDriver}`)
        }
      }
    } catch (err) {
      ctx.broker.logger.error(err)
    }
  }

  const RUN_INTERVAL = 2 * 60 * 1000
  setTimeout(() => {
    ctx.broker.call('devicemanager.monitor')
  }, RUN_INTERVAL)
}

