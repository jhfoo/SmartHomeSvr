const https = require('https'),
  axios = require('axios')

module.exports = {
  getDeviceStates: getDeviceStates,
  setState: setDeviceState,
}

async function getDeviceStates(ctx, DeviceId, config) {
  return {}
}

async function setDeviceState(ctx, DeviceId, config) {
  const agent = new https.Agent({  
    rejectUnauthorized: false
  })
  const resp = await axios.post(config.send[ctx.params.channel],
    'payload=' + JSON.stringify({
      text: ctx.params.text,
    }), {
    httpsAgent: agent,
  })
  ctx.broker.logger.debug(`Chat text: ${ctx.params.text}`)
  ctx.broker.logger.debug(`Chat response: ${resp.status}`)
}
