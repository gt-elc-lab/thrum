var app = angular.module('thrum');
app.service('Flask', ['$http', Flask]);

function Flask($http) {
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

    exports.getUsage = function(colleges, term) {
        console.log(term);
        return $http({
            url: '/usage',
            method: 'GET',
            params: {
                colleges: colleges,
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
                term: term,
            }
      });
    };

    exports.getWordTreeData = function(college, term) {
        return $http({
            url: '/wordtree',
            method: 'GET',
            params: {
                college: college,
                term: term
            }
        });
    };


    return exports;
}