module.exports = {
  onMonitor: onMonitor,
}

let LastState = null

async function onMonitor(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug('Tplink.onMonitor')

  const DeviceStates = await ctx.broker.call('devicemanager.getStates', {
    DeviceId: DeviceId,
  })

  ctx.broker.logger.debug(`${DeviceId} device state: ${JSON.stringify(DeviceStates, null, 2)}`)

  if (LastState === null) {
    LastState = DeviceStates.sysInfo.relay_state
  } else if (LastState != DeviceStates.sysInfo.relay_state) {
    LastState = DeviceStates.relay_state
    ctx.broker.call('devicemanager.setState', {
      DeviceId: 'chat',
      channel: 'smarthome',
      text: `${DeviceId} state changed: ${DeviceStates.sysInfo.relay_state}`,
    })
    ctx.broker.logger.debug(`${DeviceId} state changed: ${DeviceStates.sysInfo.relay_state}`)
  }
}