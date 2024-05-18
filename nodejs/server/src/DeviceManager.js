const PromClient = require('prom-client')

module.exports = {
  getStates: getDeviceStates,
  setState: setDeviceState,
  monitor: monitorDevices,
  prometheus: getMetrics,
  init: init,
}

var DeviceConfig = {},
  DeviceDrivers = {}

async function getMetrics(ctx) {
  const PromRegistry = PromClient.register
  PromRegistry.clear()
  ctx.params.metrics = {}
  ctx.params.metrics.energy = new PromClient.Gauge({
    name: 'EnergyW',
    help: 'Energy consumption',
    labelNames: ['device'],
    register: PromRegistry,
  })

  ctx.params.metrics.PowerRelay = new PromClient.Gauge({
    name: 'PowerRelay',
    help: 'Relay state (on/ off)',
    labelNames: ['device'],
    register: PromRegistry,
  })

  // iterate through devices
  let DeviceIds = Object.keys(DeviceConfig)
  MetricPromises = []
  DeviceIds.forEach(async (DeviceId) => {
    if (DeviceConfig[DeviceId].isMetric) {
      ctx.broker.logger.debug(`Retrieve metrics for ${DeviceId}`)
      MetricPromises.push(DeviceDrivers[DeviceConfig[DeviceId].driver].getMetrics(ctx, DeviceId, DeviceConfig[DeviceId]))
    }
  })
  try {
    // let DeviceId = DeviceIds[idx]
    const PromiseResults = await Promise.all(MetricPromises.map(p => p.catch(e => e)))
    const errors = PromiseResults.filter(result => result instanceof Error)
    ctx.broker.logger.error(`${errors.length} errors retrieving metrics`)

    // get metrics in Prometheus format
    const ret = await PromRegistry.metrics()
    ctx.meta.$responseType = 'text/plain'
    return ret
  } catch (err) {
    ctx.broker.logger.error(err)
  } 
// for (let idx = 0; idx < DeviceIds.length; idx++) {
  // }

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

  setTimeout(() => {
    ctx.broker.call('devicemanager.monitor', {
      RunInterval: ctx.params.RunInterval,
    })
  }, ctx.params.RunInterval)
}

