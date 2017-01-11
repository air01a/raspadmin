angular.module('raspadmin', [])
	.controller('downloadCtrl', function($scope,$http,$timeout) {
		$scope.getInfo = function() {
			$http.get('/downloader/getInfo')
				.success(function(res) {
					$scope.result= res;
				});
		};
	
		$scope.currentFilter = function (item) { 
 			 if (item.state === 'd' || item.state === 'w') {
  				return item;
			 }
		};
	
                $scope.historyFilter = function (item) {
                         if (item.state === 'f' || item.state === 'e' || item.state === 'r' || item.state === 'dr' || item.state==='df') {
                                return item;
                         }
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
