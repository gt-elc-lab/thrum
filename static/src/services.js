var app = angular.module('thrum');
app.service('Api', ['$http', Api]);
function Api($http) {

    var exports = {};

    exports.getColleges = function() {
        return $http({
            url: '/colleges',
            method: 'GET',
            params: null
        });
    };

    exports.getTrending = function(college) {
        return $http({
            url: '/trending',
            method: 'GET',
            params: {
                college: college
            }
        });
    };

    exports.getUsage = function(college, term) {
        return $http({
            url: '/usage',
            method: 'GET',
            params: {
                college: college,
                term: term
            }
        });
    };

    exports.getContent = function(college, term) {
        return $http({
            url: '/content',
            method: 'GET',
            params: {
                college: college,
                term: term
            }
      });
    };

    return exports;
}