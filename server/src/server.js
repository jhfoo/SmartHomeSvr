const restify = require('restify'),
    mqtt = require('mqtt'),
    PromClient = require('prom-client'),
    registry = new PromClient.Registry()

const SERVICE = {
        PORT: 9090
    },
    MQTT = {
        url: 'mqtt://mosquitto.service.yishun.consul',
        DataTopic: 'sensor-data'
    }

// configure MQTT client
const MqClient = mqtt.connect(MQTT.url)
MqClient.on('connect', () => {
    MqClient.subscribe(MQTT.DataTopic, (err) => {
        if (err) {
            console.error(err)
            process.exit(1)
        }
        // else
        console.log('Subscribed to %s', MQTT.DataTopic)
    })
})

MqClient.on('message', (topic, message) => {
    console.log(message.toString())
    ReadingCounter.inc(1)

    let data = JSON.parse(message.toString())
    TemperatureHist.observe({
        DeviceId: data.DeviceId
    }, Math.floor(data.TempCel * 10))
})

// configure Prometheus client
ReadingCounter = new PromClient.Counter({
    name: 'reading_count',
    help: 'Number of data points',
})
// registry.registerMetric(ReadingCounter)

TemperatureHist = new PromClient.Summary({
    name: 'temperature',
    help: 'Environment temperature readings',
    labelNames: ['DeviceId'],
    // maxAgeSeconds: 60,
    // ageBuckets: 3
})
registry.registerMetric(TemperatureHist)

console.log('Starting service...')
var server = restify.createServer()

server.get('/metrics', (req, res, next) => {
    res.header('content-type', registry.contentType)
    res.send(registry.metrics())
    registry.resetMetrics()
    next()
})

// require('./routes/face').applyRoutes(server, '/face')

server.listen(SERVICE.PORT, function() {
  console.log('%s listening at %s', server.name, server.url);
})