/*eslint-disable no-unused-params, no-unused-vars*/
var http = require('http');
var Compute = require('@google-cloud/compute');
var compute = Compute();

exports.getInstance = function startInstance(req, res) {
    var zone = compute.zone('asia-southeast1-b');
    var vm = zone.vm('ts');
  
    vm.get(function(err, operation, apiResponse) {
      if(err)
        res.status(200).send('Cannot get instance info')
      res.status(200).send(apiResponse);
    });
};