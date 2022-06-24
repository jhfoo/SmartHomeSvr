const BMS = require('./BmsConst')

module.exports = {
  onMonitor: onMonitor,
}

async function onMonitor(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug('BmsHandler.onMonitor')

  const DeviceStates = await ctx.broker.call('devicemanager.getStates', {
    DeviceId: DeviceId,
  })
  ctx.broker.logger.debug(`BMS states: ${JSON.stringify(DeviceStates, null, 2)}`)

  if (DeviceStates.capacity < BMS.MIN_CAPACITY 
    && DeviceConfig.state != BMS.STATE_UNDERVOLTAGE) {
    DeviceConfig.state = BMS.STATE_UNDERVOLTAGE
    ctx.broker.logger.info('Battery is under voltage')
    
    // turn off battery to home
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarMainsSwitch',
      StateName: 'power',
      StateValue: 'off',
    })

    // turn off battery to servers
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarServerSwitch',
      StateName: 'power',
      StateValue: 'off',
    })
    return
  }

  if (DeviceStates.capacity >= BMS.UNDER_RECOVERY_CAPACITY 
    && DeviceConfig.state === BMS.STATE_UNDERVOLTAGE) {
    DeviceConfig.state = BMS.STATE_NORMAL
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarServerSwitch',
      StateName: 'power',
      StateValue: 'on',
    })
    return
  }
}