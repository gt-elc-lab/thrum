var app = angular.module('thrum');
app.directive('wordTree', ['Flask', WordTree]);


function WordTree() {

    var directive = {
        restrict: 'E',
        scope: {},
        templateUrl: '../views/wordtree-directive.html',
        link: link,
        controller: controller
    };

    function link(scope, elem) {

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

            Flask.getWordTreeData($scope.selected, $scope.term).success(function(response, status) {
                console.log(response.data);
                var google_data = google.visualization.arrayToDataTable(response.data);
                var options = {};
                options.wordtree = {
                    format : 'implicit',
                    word: $scope.term,
                    type: 'double'
                };
                var chart =  new google.visualization.WordTree(document.getElementById('wordtree'));
                chart.draw(google_data, options);
            })
                .error(function(response, status) {

                });
        }

        function selectCollege(college) {
            $scope.selected = college;
        }



    }

    return directive;
}