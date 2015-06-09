angular.module('raspadmin', [])
	.controller('StatusCtrl', function($scope,$http,$timeout) {
		$scope.getInfo = function() {
			$http.get('/status/getinfo')
				.success(function(res) {
					$scope.data = res
					console.log(HttpGraphPtr)
					cpuusage = res.loadavg
					console.log(cpuusage)

					if (Number(cpuusage["la3"])>Number(res.numcpu))
						cpuusage["la3"]=res.numcpu
					if (Number(cpuusage["la2"])>Number(res.numcpu))
                                                cpuusage["la2"]=res.numcpu
					if (Number(cpuusage["la1"])>Number(res.numcpu))
                                                cpuusage["la1"]=res.numcpu

					console.log(HttpGraphPtr['mem'])

					HttpGraphPtr['loadvg3'].value=Number(cpuusage["la3"]);
					HttpGraphPtr['loadvg2'].value=Number(cpuusage["la2"]);
					HttpGraphPtr['loadvg1'].value=Number(cpuusage["la1"]);
					
					HttpGraphPtr['loadvg3'].Draw()
					HttpGraphPtr['loadvg2'].Draw()
					HttpGraphPtr['loadvg1'].Draw()

					//HttpGraphPtr['mem'].data[0]=Number(res.memory.usedraw)
					//HttpGraphPtr['mem'].data[1]=Number(res.memory.freeraw)
					//HttpGraphPtr['mem'].data[2]=Number(res.memory.bufferraw)
					//HttpGraphPtr['mem'].data[3]=Number(res.memory.cachedraw)
					//HttpGraphPtr['mem'].Draw()
				});
		};

		$scope.intervalFunction = function(){
    			$timeout(function() {
      			$scope.getInfo();
      			$scope.intervalFunction();
    			}, 30000)
  		};

		$scope.getInfo();
		$scope.intervalFunction();
	});
