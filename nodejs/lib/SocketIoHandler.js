'use strict';
var log4js = require('log4js'),
  DeviceActionHandler = require('./DeviceActionHandler');

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

      DeviceActionHandler.handleAction(data).catch(function(e) {console.log("Request failed: ", e)});
    });
  });
}

module.exports = SocketIoHandler;