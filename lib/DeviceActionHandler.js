'use strict';
var log4js = require('log4js'),
  edimax = require('edimax-smartplug');

var logger = log4js.getLogger();

module.exports = {
  handleAction: (data) => {
    var options = {
      timeout: 10000,
      name:'edimax',
      host: data.ip,
      username: 'admin',
      password: '1234'
    };
    var IsPowerOn = data.state === 'ON';

    return edimax.getStatusValues(true, options).then(function (info) {
      console.log(info);

      return edimax.setSwitchState(IsPowerOn, options);
    });
  }
};