'use strict';

angular.module('About', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/about', {
        templateUrl: '/static/ui/about.html?v=' + NationStory.appSettings.ver,
        controller: 'AboutController'
    });
    $routeProvider.when('/aboutus', {
        templateUrl: '/static/ui/about.html?v=' + NationStory.appSettings.ver,
        controller: 'AboutController'
    });
}])

.controller('AboutController', function($scope, $routeParams, $http) {

});