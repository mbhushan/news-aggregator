$(document).ready(function() {
    for(var i=0; i<NationStory.messages.length; i++) {
        NationStory.notify(NationStory.messages[i].message, NationStory.messages[i].type);
    }
});

(function() {
    var app = angular.module('nsadmin',['infinite-scroll','ngRoute', 'restangular', 'NewsSources',
                                        'ManageTags', 'XMLUpload', 'VideoCards',
                                        'UserStories']);

    app.config(function($routeProvider, $locationProvider, $httpProvider) {
        $httpProvider.defaults.headers.delete = {'Content-Type': 'application/json'};

        $routeProvider.
            when('/nsadmin', {
                templateUrl: '/static/ui/nsadmin/admin.html?v=' + NationStory.appSettings.ver,
                controller: 'AdminController'
            })
            .otherwise({ redirectTo: '/nsadmin' });

            // configure html5 to get links working on jsfiddle
            $locationProvider.html5Mode(true);
    }).
    run(function(Restangular) {
        Restangular.setBaseUrl('/api/admin')
    });

    app.controller('AdminController', function($scope, $route) {});
})();