var app = angular.module('thrum');
app.directive('wordTree', ['Flask', WordTree]);
app.directive('wordSearch', ['Flask', WordSearch]);

function WordTree() {

    var directive = {
        restrict: 'E',
        scope: {},
        templateUrl: '../views/wordtree-directive.html',
        link: link,
        controller: controller
    };

    function link($scope, elem) {

    }

    function controller($scope, Flask) {
        $scope.selected;
        $scope.colleges;
        $scope.render = render;
        $scope.select = selectCollege;
        init();

        function init() {
            Flask.getColleges().success(function(response, status) {
                $scope.colleges = response.data;
            })
                .error(function(response, status) {
                    alert('Server responsed with ' + response);
                });
        }

        function render() {
            if (!$scope.term) {
                alert('please type a word and select a college');
                return;
            }

            Flask.getWordTreeData($scope.selected, $scope.term).success(drawWordTree)
                .error(function(response, status) {

                });
        }

        function selectCollege(college) {
            $scope.selected = college;
        }

        function drawWordTree(response, status) {
            var google_data = google.visualization.arrayToDataTable(response.data);
            var options = {};
            options.wordtree = {
                format: 'implicit',
                word: $scope.term,
                type: 'double'
            };
            var chart = new google.visualization.WordTree(document.getElementById('wordtree'));
            chart.draw(google_data, options);
        }

    }

    return directive;
}

function WordSearch() {

    var directive = {
        restrict: 'E',
        scope: {},
        templateUrl: '../views/wordsearch-directive.html',
        link: link,
        controller: controller
    };

    function link($scope, element, attrs) {
        var width = 850;
        var height = 400;
        var margin = {
            top: 20,
            left: 20,
            right: 20,
            bottom: 20
        };

        var svg = d3.select('#line-graph')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.right + ')');

        var yScale = d3.scale.linear()
            .range([height - margin.top - margin.bottom, 0]);

        var xScale = d3.time.scale()
            .range([margin.left, width - margin.right]);


        var line = d3.svg.line().interpolate('interpolate')
            .x(function(d) {
                return xScale(new Date(d.date));
            })
            .y(function(d) {
                return yScale(d.count);
            });

        $scope.$watch('data', function() {
            if (!$scope.data) {
                return;
            }


            var ymin = 0;
            var ymax = 0;
            var xmin, xmax;

            $scope.data.forEach(function(college) {
                college.values.forEach(function(d) {
                    ymin = (d.count < ymin) ? ymin = d.count : ymin = ymin;
                    ymax = (d.count > ymax) ? ymax = d.count : ymax = ymax;

                    var date = new Date(d.date);
                    if (!xmin || !xmax) {
                        xmin = date;
                        xmax = date;
                    } else {
                        xmin = (date < xmin) ? xmin = date : xmin;
                        xmax = (date > xmax) ? xmax = date : xmax;
                    }
                });
            });

            xScale.domain([xmin, xmax]);
            yScale.domain([ymin, ymax]);
            var yAxis = d3.svg.axis().scale(yScale).orient('left');
            var xAxis = d3.svg.axis().scale(xScale).orient('bottom');

            svg.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(' + 0 + ',' + (height - margin.bottom - margin.top) + ')')
                .call(xAxis);

            svg.append('g')
                .attr('class', 'y axis')
                .attr('transform', 'translate(' + margin.left + ',' + 0 + ')')
                .call(yAxis);

            var color = d3.scale.linear()
                .domain([0, $scope.data.length - 1])
                .range(['red', 'blue', 'orange', 'yellow', 'green']);

            $scope.data.forEach(function(d, i) {
                svg.append("path")
                    .datum(d.values)
                    .attr("class", "line")
                    .attr('fill', 'none')
                    .style('stroke', color(i))
                    .style('stroke-width', '3px')
                    .attr("d", line);

                var points = svg.selectAll(".point")
                    .data(d.values)
                    .enter().append("svg:circle")
                    .attr("stroke", "black")
                    .attr("fill", color(i))
                    .attr("cx", function(d, i) {
                        return xScale(new Date(d.date))
                    })
                    .attr("cy", function(d, i) {
                        return yScale(d.count)
                    })
                    .attr("r", 5);
            });

        });
    }

    function controller($scope, Flask) {
        $scope.data;
        $scope.timePeriod;
        $scope.colleges = [];
        $scope.selection = [];
        $scope.term;
        $scope.toggle = toggle;
        $scope.getUsage = getUsage;

        init();

        function init() {
            Flask.getColleges().success(function(response, status) {
                $scope.colleges = response.data;
            })
                .error(function(response, status) {
                    alert('Server responsed with ' + response);
                });
        }

        function toggle(college) {
            var index = $scope.selection.indexOf(college);
            if (index > -1) {
                $scope.selection.splice(index, 1);
            } else {
                $scope.selection.push(college);
            }
            console.log($scope.selection);
        }

        function getUsage() {
            if (!$scope.term || !$scope.selection) {
                alert('Please select a college and enter a term');
            }
            Flask.getUsage($scope.selection, $scope.term)
            .success(function(response, status) {
                    $scope.data = response.data;
                })
                .error(function(response, status) {
                    alert('Server responsed with ' + status);
                });
        }
    }

    return directive;

}