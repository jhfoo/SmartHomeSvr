module.exports = {
  onMonitor: onMonitor,
}

let LastState = null

async function onMonitor(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug('Tplink.onMonitor')

  const DeviceStates = await ctx.broker.call('devicemanager.getStates', {
    DeviceId: DeviceId,
  })

  if (LastState === null) {
    LastState = DeviceStates.relay_state
  } else if (LastState != DeviceStates.relay_state) {
    LastState = DeviceStates.relay_state
    ctx.broker.logger.debug(`Device state changed: ${DeviceStates.relay_state}`)
  }
}