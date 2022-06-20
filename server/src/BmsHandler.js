module.exports = {
  onMonitor: onMonitor,
}

const MIN_CAPACITY = 100,
  UNDER_RECOVERY_CAPACITY = 120
  MIN_BATTERY_VOLTAGE = 2.9,
  STATE_NORMAL = 'normal',
  STATE_UNDERVOLTAGE = 'undervoltage'
  STATE_OVERVOLTAGE = 'overvoltage'

let BmsState = STATE_NORMAL

async function onMonitor(ctx, DeviceId, DeviceConfig) {
  ctx.broker.logger.debug('BmsHandler.onMonitor')

  const DeviceStates = await ctx.broker.call('devicemanager.getStates', {
    DeviceId: DeviceId,
  })
  ctx.broker.logger.debug(`BMS states: ${JSON.stringify(DeviceStates, null, 2)}`)
  if (DeviceStates.capacity < MIN_CAPACITY 
    && BmsState != STATE_UNDERVOLTAGE) {
    BmsState = STATE_UNDERVOLTAGE
    // turn off battery to home
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarMainsSwitch',
      StateName: 'power',
      StateValue: 'off',
    })
    // turn off battery to servers
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarPowerSwitch',
      StateName: 'power',
      StateValue: 'off',
    })
    return
  }

  if (DeviceStates.capacity >= UNDER_RECOVERY_CAPACITY 
    && BmsState === STATE_UNDERVOLTAGE) {
    BmsState = STATE_NORMAL
    await ctx.broker.call('devicemanager.setState', {
      DeviceId: 'SolarPowerSwitch',
      StateName: 'power',
      StateValue: 'on',
    })
    return
  }
}