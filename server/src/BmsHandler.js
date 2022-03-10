module.exports = {
  onMonitor: onMonitor,
}

async function onMonitor(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug('BmsHandler.onMonitor')

  const DeviceStates = await ctx.broker.call('devicemanager.getStates', {
    DeviceId: DeviceId,
  })
  ctx.broker.logger.debug(`Device states: ${JSON.stringify(DeviceStates, null, 2)}`)
}