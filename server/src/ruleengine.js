const { ServiceBroker } = require('moleculer'),
  ApiService = require('moleculer-web')

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
    isMonitor: false,
  },
  bms: {
    ip: '192.168.88.40',
    driver: 'custombms',
    isMonitor: true,
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
    update: monitorDevices,
    setState: setDeviceState,
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
  broker.call('devicemanager.update', {
    config: DeviceConfig,
    drivers: DeviceDrivers,
  })
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

  let config = DeviceConfig
  let DeviceIds = Object.keys(config)

  for (let idx = 0; idx < DeviceIds.length; idx++) {
    try {
      let DeviceId = DeviceIds[idx]
      if (ctx.params.config[DeviceId.isMonitor]) {
        let DeviceDriver = config[DeviceId].driver
        if (DeviceDriver in ctx.params.drivers) {
          await ctx.params.drivers[DeviceDriver].update(ctx, DeviceId, config[DeviceId])
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

