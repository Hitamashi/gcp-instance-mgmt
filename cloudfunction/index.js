/*eslint-disable no-unused-params, no-unused-vars*/
var http = require('http');
var Compute = require('@google-cloud/compute');
var compute = Compute();

// Get íntance info
exports.getInstance = function startInstance(req, res) {
	if(!req.query.zone || !req.query.vm){
		res.status(400).send("Missing parameters")
	}
	
    var zone = compute.zone(req.query.zone);
    var vm = zone.vm(req.query.vm);
  
    vm.get(function(err, operation, apiResponse) {
      if(err)
        res.status(200).send('Cannot get instance info')
      res.status(200).send(apiResponse);
    });
};

// Start instance
exports.startInstance = function startInstance(req, res) {
	if( !req.query.zone || !req.query.vm){
		res.status(400).send("Missing parameters")
	}
	
    var zone = compute.zone(req.query.zone);
    var vm = zone.vm(req.query.vm);
    vm.start(function(err, operation, apiResponse) {
    	if (err) {
            console.error(err);
            res.status(200).send("Failed to start instance");
        }
        console.log('instance start successfully');
    });
res.status(200).send('Success start instance');
};

//Stop instance
exports.stopInstance = function stopInstance(req, res) {
	if( !req.query.zone || !req.query.vm){
		res.status(400).send("Missing parameters")
	}

    var zone = compute.zone(req.query.zone);
    var vm = zone.vm(req.query.vm);
    vm.stop(function(err, operation, apiResponse) {
    	if (err) {
            console.error(err);
            res.status(200).send("Failed to stop instance");
        }
        console.log('instance stop successfully');
    });
	res.status(200).send('Success stop instance');
};