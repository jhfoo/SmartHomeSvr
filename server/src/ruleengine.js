const { ServiceBroker } = require('moleculer'),
  ApiService = require('moleculer-web'),
  DeviceManager = require('./DeviceManager')

const broker = new ServiceBroker({
  logLevel: 'debug',
})

DeviceManager.init({
  DeviceConfig: require('./DeviceConfig'),
  DeviceDrivers: {
    tplink: require('./TplinkDriver'),
    custombms: require('./BmsDriver'),
    chat: require('./ChatDriver'),
  }
})
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
  actions: DeviceManager,
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
  
}

