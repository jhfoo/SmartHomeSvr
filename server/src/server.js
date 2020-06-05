const restify = require('restify'),
    mqtt = require('mqtt')

const SERVICE = {
        PORT: 9090
    },
    MQTT = {
        url: 'mqtt://mosquitto.service.yishun.consul',
        DataTopic: 'sensor-data'
    }

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
})

console.log('Starting service...')
var server = restify.createServer()

server.get('/api/fitbit/profile', (req, res, next) => {
})

// require('./routes/face').applyRoutes(server, '/face')

server.listen(SERVICE.PORT, function() {
  console.log('%s listening at %s', server.name, server.url);
})