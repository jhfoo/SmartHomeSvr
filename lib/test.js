var router = require('koa-router')(),
  DeviceActionHandler = require('./DeviceActionHandler');

router.get('/ping', function *(next) {
  this.body = 'pong';
});

router.get('/error', function *(next) {
  this.body = 'boo';
  throw new Error('Oh noes!');
});

router.get('/lighton', function *(next) {
  this.body = 'light ON';
  DeviceActionHandler.handleAction({
    state: 'ON',
    ip: '192.168.1.18'
  }).catch(function(e) {console.log("Request failed: ", e)});
});

router.get('/lightoff', function *(next) {
  this.body = 'light OFF';
  DeviceActionHandler.handleAction({
    state: 'OFF',
    ip: '192.168.1.18'
  }).catch(function(e) {console.log("Request failed: ", e)});
});

module.exports = router;