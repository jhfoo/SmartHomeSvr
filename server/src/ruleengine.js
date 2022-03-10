const { ServiceBroker } = require('moleculer'),
  ApiService = require('moleculer-web'),
  BmsHandler = require('./BmsHandler'),
  TplinkHandler = require('./TplinkHandler')

const broker = new ServiceBroker({
  logLevel: 'debug',
})

const DeviceConfig = {
  SolarMainsSwitch: {
    ip: '192.168.88.50',
    driver: 'tplink',
    isMonitor: false,
  },
  SolarAuxSwitch: {
    ip: '192.168.88.51',
    driver: 'tplink',
    isMonitor: true,
    onMonitor: TplinkHandler.onMonitor,
  },
  bms: {
    ip: '192.168.88.40',
    driver: 'custombms',
    isMonitor: true,
    onMonitor: BmsHandler.onMonitor,
  }
}

const DeviceDrivers = {
  tplink: require('./TplinkDriver'),
  custombms: require('./BmsDriver'),
}

// console.log(DeviceDrivers)
// process.exit(0)

broker.createService({
  name: 'solarbattery',
  actions: {
    status(ctx) {
      return 1
    }
  }
})

broker.createService({
  name: 'devicemanager',
  actions: {
    getStates: getDeviceStates,
    setState: setDeviceState,
    monitor: monitorDevices,
  }
})

broker.createService({
  mixins: [ApiService],
  settings: {
    port: 8008,
  },
  onError(req, res, err) {
    res.setHeader('Content-Type', 'text/plain')
    res.writeHead(501)
    res.end(`Customer global error: ${err.message}`)
  }
})

broker.start()
.then(() => {
  startMonitoring()
})
.catch((err) => {
  console.error(err)
})

function startMonitoring() {
  broker.call('devicemanager.monitor', {
    config: DeviceConfig,
    drivers: DeviceDrivers,
  })
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
    await DeviceDrivers[TargetDevice.driver].setState(ctx, TargetDevice)
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
      if (ctx.params.config[DeviceId].isMonitor) {
        // device configured to be monitored
        // ctx.broker.logger.debug(`Device to be monitored: ${DeviceId}`)
        let DeviceDriver = DeviceConfig[DeviceId].driver
        if (DeviceDriver in ctx.params.drivers) {
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
    startMonitoring()
  }, RUN_INTERVAL)
}

