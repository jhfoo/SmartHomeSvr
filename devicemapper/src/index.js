const { ServiceBroker } = require('moleculer'),
  ApiService = require('moleculer-web'),
  tplink = require('tplink-smarthome-api')

const broker = new ServiceBroker()

const DeviceConfig = {
  SolarFeedSwitch: {
    mac: '28:ee:52:ba:e3:9f',
  }
}

broker.createService({
  name: 'devicemap',
  actions: {
    status(ctx) {
      return 1
    }
  }
})

broker.createService({
  mixins: [ApiService],
  settings: {
    port: 3001,
  },
  onError(req, res, err) {
    res.setHeader('Content-Type', 'text/plain')
    res.writeHead(501)
    res.end(`Customer global error: ${err.message}`)
  }
})

broker.start()
.catch((err) => {
  console.error(err)
})

startScanning()

function startScanning() {
  TplinkClient = new tplink.Client()
  TplinkClient.startDiscovery().on('device-new', async (device) => {
    let info = await device.sysInfo()
    console.log(info)
  })
}