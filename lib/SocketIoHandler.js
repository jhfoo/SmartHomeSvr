'use strict';
var log4js = require('log4js'),
  edimax = require('edimax-smartplug');

var logger = log4js.getLogger();

function SocketIoHandler (io) {
  io.on('connection', (socket) => {
    logger.debug('New Socket.io connection');
    // NOTE: PING is a reserved event!
    socket.on('pingy', (data) => {
      logger.debug('PINGY received: ' + data);
      socket.emit('pingy','pongy: ' + data);
    });

    socket.on('DeviceAction', (data) => {
      logger.debug('DeviceAction: ' + JSON.stringify(data));

      var options = {
        timeout: 10000,
        name:'edimax',
        host: data.ip,
        username: 'admin',
        password: '1234'
      };
      var IsPowerOn = data.state === 'ON';

      edimax.getStatusValues(true, options).then(function (info) {
        console.log(info);

        return edimax.setSwitchState(IsPowerOn, options);
      }).catch(function(e) {console.log("Request failed: ", e)});



    });
  });
}

module.exports = SocketIoHandler;