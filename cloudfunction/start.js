/*eslint-disable no-unused-params, no-unused-vars*/
var http = require('http');
var Compute = require('@google-cloud/compute');
var compute = Compute();

exports.startInstance = function startInstance(req, res) {
    var zone = compute.zone('asia-southeast1-b');
    var vm = zone.vm('ts');
    vm.start(function(err, operation, apiResponse) {
    	if (err) {
            console.error(err);
            res.status(200).send("Failed to start instance");
        }
        console.log('instance start successfully');
    });
res.status(200).send('Success start instance');
};