angular.module('raspadmin', [])
	.controller('NzbgetCtrl', function($scope,$http,$timeout) {
		$scope.getInfo = function() {
			$http.get('/nzbget/getstatus')
				.success(function(res) {
					$scope.status = res.status
					$scope.listgroups = res.listgroups
					$scope.postqueue = res.postqueue
					$scope.history = res.history
				});
		};

		$scope.intervalFunction = function(){
    			$timeout(function() {
      			$scope.getInfo();
      			$scope.intervalFunction();
    			}, 10000)
  		};

		$scope.getInfo();
		$scope.intervalFunction();
	});
