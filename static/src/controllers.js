var app = angular.module('thrum');

app.controller('TrendingController', TrendingController);
app.controller('WordTreeController', WordTreeController);
app.controller('WordSearchController', WordSearchController);


TrendingController.$inject = ['$scope', 'Flask'];

function TrendingController($scope, Flask) {
    $scope.selected = 'Colleges';
    $scope.trending = [];
    $scope.colleges;

    //////////////

    $scope.getTrending = getTrending;
    init();

    function init() {
        Flask.getColleges().success(function(response, status) {
            $scope.colleges = response.data;
        })
            .error(function(response, status) {
                alert('Server responded with ' + response);
            });
    }

    function getTrending(college) {
        $scope.selected = college;
        Flask.getTrending(college).success(function(response, status) {
            $scope.trending = response.data;
        })
            .error(function(response, status) {
                alert('Server responded with ' + response);
            });
    }
}

WordTreeController.$inject = ['$scope', 'Flask'];

function WordTreeController($scope, Flask) {
    $scope.instances = [1];

    init();

    function init() {
        Flask.getColleges().success(function(response, status) {
            $scope.colleges = response.data;
        })
            .error(function(response, status) {
                alert('Server responsed with ' + response);
            });
    }


    $scope.addInstance = function() {
        $scope.instances.push(1);
    };

    $scope.removeInstance = function() {
        if ($scope.instances.length > 1) {
            $scope.instances.pop();
            // $scope.$apply();
        }
        console.log($scope.instances);
    };
}

WordSearchController.$inject = ['$scope'];

function WordSearchController($scope) {

}