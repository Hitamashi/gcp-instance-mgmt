/*eslint-disable no-unused-params, no-unused-vars*/
var http = require('http');
var Compute = require('@google-cloud/compute');
var compute = Compute();

exports.stopInstance = function stopInstance(req, res) {
    var zone = compute.zone('asia-southeast1-b');
    var vm = zone.vm('ts');
    vm.stop(function(err, operation, apiResponse) {
        console.log('instance stop successfully');
    });
	res.status(200).send('Success stop instance');
};