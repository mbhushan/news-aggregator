'use strict';

angular.module('NewsSources', ['ngRoute', 'restangular', 'angularModalService'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/nsadmin/sources', {
        templateUrl: '/static/ui/nsadmin/news-sources.html?v=' + NationStory.appSettings.ver,
        controller: 'NewsSourcesController'
    });
}])

.controller('NewsSourcesController', function($scope, $routeParams, Restangular, ModalService) {
    var newsSourcesLoader = Restangular.all('news_sources');
    $scope.busy = true;

    newsSourcesLoader.getList().then(function(sources){
        $scope.sources = sources;
        $scope.busy = false;
    });

    $scope.editSource = function(event, source) {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-source.html?v=" + NationStory.appSettings.ver,
            controller: "SourceEditController",
            inputs: {
                source: source
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(source) {
                source.put();
            });
        });
    };

    $scope.removeSource = function(event, source) {
        var sourceWithId = _.find($scope.sources, function(s) {
            return source._id === s._id;
        });

        source.remove().then(function() {
            var index = $scope.sources.indexOf(sourceWithId);
            if (index > -1) $scope.sources.splice(index, 1);
        });
    };

    $scope.addNewSource = function() {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-source.html?v=" + NationStory.appSettings.ver,
            controller: "SourceEditController",
            inputs: {
                source: {}
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(source) {
                newsSourcesLoader.post(source).then(function(newSource) {
                    $scope.sources.push(newSource);
                  }, function() {
                    alert("There was an error saving");
                  });
            });
        });
    };

    $scope.addBulk = function() {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/bulk-source.html?v=" + NationStory.appSettings.ver,
            controller: "SourceEditController",
            inputs: {
                source: {}
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(source) {
                newsSourcesLoader.post(source).then(function(newSources) {
                    $.each(newSources, function(index, nsource){
                        $scope.sources.push(nsource);
                    });

                  }, function() {
                    alert("There was an error saving");
                  });
            });
        });
    }
})

.controller('SourceEditController', function($scope, source, $element, close, $http) {
    $scope.source = source;
    if (!$scope.source.source_type) {
        $scope.source.source_type = '2';
    }
    $scope.saveSource = function() {
        $element.modal('hide');
        close(source, 200);
    };

    $scope.testRegex = function() {
        $http.post('/api/admin/news_sources',{url: source.url, pattern: source.pattern, test: true}
            ).success(function(data) {
                alert(data.result);
            }.bind(this));
    };

    $scope.dismissModal = function(result) {
        close(null, 200); // close, but give 200ms for bootstrap to animate
     };
});