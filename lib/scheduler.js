'use strict';
var log4js = require('log4js'),
  parser = require('cron-parser'),
  NodeSchedule = require('node-schedule'),
  DeviceActionHandler = require('./DeviceActionHandler');

var logger = log4js.getLogger();

function Scheduler (config) {
  this.config = config.schedules;

  logger.debug('Schedules loaded: ' + this.config.length);
}

Scheduler.prototype.run = function() {
  this.config.forEach((item) => {
    NodeSchedule.scheduleJob(item.frequency, () => {
      if (item.event.type === 'DeviceAction') {
        DeviceActionHandler.handleAction(item.event.data);
        logger.debug(item);
      }
    });
  });
}


module.exports = Scheduler;