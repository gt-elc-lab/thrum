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

    function link($scope, elem, attrs) {

    }

    function controller($scope, Flask) {
        $scope.colleges = [];
        $scope.selection = [];
        $scope.showColleges;
        $scope.toggle = toggle;
        $scope.term;
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
            }
            else {
                $scope.selection.push(college);
            }
            console.log($scope.selection);
        }

        function getUsage(){
            Flask.getUsage($scope.selection, $scope.term).success(function(response, status) {
                console.log(response.data);
            })
            .error(function(response, status) {
                alert('Server responsed with ' + status);
            });
        }

    }

    return directive;

}