const BmsHandler = require('./BmsHandler'),
  TplinkHandler = require('./TplinkHandler')

module.exports = {
  SolarMainsSwitch: {
    ip: '192.168.88.50',
    driver: 'tplink',
    isMonitor: false,
    isMetric: true,
  },
  SolarServerSwitch: {
    ip: '192.168.88.52',
    driver: 'tplink',
    isMonitor: false,
    isMetric: true,
  },
  SolarAuxSwitch: {
    ip: '192.168.88.51',
    driver: 'tplink',
    isMonitor: true,
    isMetric: true,
    onMonitor: TplinkHandler.onMonitor,
  },
  SolarPowerSwitch: {
    ip: '192.168.88.53',
    driver: 'tplink',
    isMonitor: true,
    onMonitor: TplinkHandler.onMonitor,
    isMetric: true,
  },
  bms: {
    ip: '192.168.88.40',
    driver: 'custombms',
    isMonitor: true,
    onMonitor: BmsHandler.onMonitor,
  },
  chat: {
    send: {
      smarthome: 'https://192.168.88.13:5001/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%229Qdndrm2KwEu5Z4AdRw9075VmrmYheSXqqYcjk7CnB6L3GLiECpyR20IoUczMDXq%22',
    },
    isMonitor: false,
    driver: 'chat',
  }
}
