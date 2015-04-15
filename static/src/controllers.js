var app = angular.module('thrum');

app.controller('TrendingController', TrendingController);
app.controller('WordTreeController', WordTreeController);
app.controller('SearchController', SearchController);


TrendingController.$inject = ['$scope', 'Flask'];
function TrendingController($scope) {
    $scope.colleges;
    $scope.trending;

    //////////////

    $scope.getTrending = getTrending;
    init();

    function init(){
        Flask.getColleges().success(function(response, status) {
            $scope.colleges = response.data;
        })
        .error(function(response, status) {
            alert('Server responded with ' + response);
        });
    }

    function getTrending(college) {
        Flask.getTrending(collge).success(function(response, status) {

        })
        .error(function(response, status) {
            alert('Server responded with ' + response);
        });
    }
}

WordTreeController.$inject = ['$scope'];
function WordTreeController($scope) {

}

SearchController.$inject = ['$scope'];
function SearchController($scope) {

}