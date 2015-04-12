'use strict'

var app = angular.module('thrum', []);
app.controller('MainController', MainController);
app.service('Api', ['$http', Api]);
app.directive('barGraph', BarGraph);
MainController.$inject = ['$scope', 'Api'];

function MainController($scope, Api) {
    $scope.selected;
    $scope.colleges;
    $scope.trending;
    $scope.usageData;
    $scope.myData = [
    {name: 'AngularJS', count: 300},
    {name: 'D3.JS', count: 150},
    {name: 'jQuery', count: 400},
    {name: 'Backbone.js', count: 300},
    {name: 'Ember.js', count: 100}
];

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
        Api.getUsage($scope.selected, term).success(function(response, status){
            $scope.usageData = response.data;
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
                college : college
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
            data : '='
        },
        link : link
    };

    function link(scope, element) {
        
        var margin = {top: 20, right: 20, bottom: 30, left: 40};
        var width = 960 - margin.left - margin.right;
        var height = 500 - margin.top - margin.bottom;

        var y = d3.scale.linear().range([height, 0]);
        var x = d3.time.scale().range([0, width]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
 
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10);

        var svg = d3.select(element[0])
          .append("svg")
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        
        //Render graph based on 'data'
        scope.render = function(data) {
            //Set our scale's domains
          x.domain(data.map(function(d) { return new Date(d.date); }));
          y.domain([0, d3.max(data, function(d) { return d.count; })]);
          
          //Redraw the axes
          svg.selectAll('g.axis').remove();
          //X axis
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);
              
          //Y axis
          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("Count");
              
          var bars = svg.selectAll(".bar").data(data);
          bars.enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(new Date(d.date)); })
            .attr("width", '30px');
 
          //Animate bars
          bars
              .transition()
              .duration(1000)
              .attr('height', function(d) { return height - y(d.count); })
              .attr("y", function(d) { return y(d.count); })
          
 
         //Watch 'data' and run scope.render(newVal) whenever it changes
         //Use true for 'objectEquality' property so comparisons are done on equality and not reference
          scope.$watch('data', function(){
            alert('Data changed');
              scope.render(scope.data);
          }, false);  
        };
    }

    function DateDomain(d) {return new Date(d.date);}
    return directive;
}
