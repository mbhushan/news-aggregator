'use strict';

angular.module('Headlines', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/explore', {
        templateUrl: '/static/ui/stories.html',
        controller: 'HeadlinesController'
    });
}])

.controller('HeadlinesController', function($scope, $routeParams, Stories, $http) {
    $scope.stories = new Stories();
    $scope.stories.url = '/api/headlines';

    var init = function() {
        $scope.$emit('navTopic:changed', '');
    };

    init();

});