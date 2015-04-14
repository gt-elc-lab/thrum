'use strict'

var app = angular.module('thrum', []);
app.controller('MainController', MainController);
app.service('Api', ['$http', Api]);
app.service('SelectionService', SelectionService);
app.directive('barGraph', ['SelectionService', BarGraph]);
MainController.$inject = ['$scope', '$rootScope', 'Api'];

function MainController($scope, $rootScope, Api) {
    $scope.selected;
    $scope.colleges;
    $scope.trending;
    $scope.usageData = [];

    init();

    function init() {
        Api.getColleges().success(function(response, status) {
            $scope.colleges = response.data;
        })
            .error(function(data, status) {
                alert('Server Responded with ' + status);
            });
    }

    $scope.selectCollege = function(college) {
        $scope.selected = college;
        Api.getTrending(college).success(function(response, status) {
            $scope.trending = response.data;
        })
            .error(function(response, status) {
                alert('Server Responded with ' + status);
            });
    };

    $scope.usage = function(term) {
        Api.getUsage($scope.selected, term).success(function(response, status) {
            $scope.usageData = response.data;
            $rootScope.$broadcast('dataChanged');
        })
            .error(function(response, status) {
                alert('Server Responded with ' + status);
            });
    };


}

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

    return exports;
}

function BarGraph() {
    var directive = {
        restrict: 'AE',
        scope: {
            data: '='
        },
        link: link,
    };


    function link(scope, element, attrs, SelectionService) {
        var margin = {top: 20, right: 20, bottom: 50, left: 50};
        var width = 800 - margin.left - margin.right;
        var height = 300 - margin.top - margin.bottom;

        function DateDomain(d) {return new Date(d.date);}
        function YCountDomain(d) { return d.count;}

      

        var svg = d3.select(element[0]).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        scope.render  = function(data) {

            var x = d3.time.scale().range([0, width])
                .domain([d3.min(data, DateDomain), 
                    d3.max(data, DateDomain)]);
                
            var y = d3.scale.linear().range([height, 0])
                .domain([0, d3.max(data, YCountDomain)]);
            
            svg.selectAll('.y.axis').remove();
            svg.selectAll('.x.axis').remove();
            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("");

            var line = d3.svg.line()
                .x(function(d) {
                    return x(new Date(d.date));
                })
                .y(function(d) {
                    return y(d.count);
                })
                .interpolate('monotone');

            svg.selectAll(".line").remove();
            svg.append("path")
                .datum(data)
                .attr("class", "line")
                .attr('fill', 'none')
                .style('stroke', 'red')
                .style('stroke-width', '3px')
                .attr("d", line);
                
            svg.selectAll("circle").remove();
            var points = svg.selectAll(".point")
                .data(data)
                .enter().append("svg:circle")
                .attr("stroke", "black")
                .attr("fill", 'blue')
                .attr("cx", function(d) {
                    return x(new Date(d.date));
                })
                .attr("cy", function(d) {
                    return y(d.count);
                })
                .attr("r", 5)
        };


        scope.$on('dataChanged', function() {
            alert('data changed');
            scope.render(scope.data);
        });
    }

    return directive;
}

SelectionService.$inject = ['$rootScope'];
function SelectionService($rootScope) {
    var college;
    var term;
    var data;
    var service = {};
   
    service.setCollege = function(college) {
        this.college = college;
    };

    service.setTerm = function(term) {
        this.term = term;
    };


    service.setData = function(data) {
        this.data = data;
        $rootScope.$broadcast('injected');
    };

    service.addToData = function(moredata) {
        this.data.push(moredata);
    };

    service.getTerm = function() {
        return this.term;
    };

    service.getData = function() {
        return this.data;
    };

    service.getCollege = function() {
        return this.college;
    };

    return service;
}