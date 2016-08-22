'use strict';

angular.module('ManageTags', ['ngRoute', 'restangular', 'angularModalService'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/nsadmin/manage-tags', {
        templateUrl: '/static/ui/nsadmin/manage-tags.html?v=' + NationStory.appSettings.ver,
        controller: 'ManageTagsController'
    });
}])

.controller('ManageTagsController', function($scope, $routeParams, Restangular, ModalService) {
    $scope.searchTag = '';
    $scope.status = 0;
    $scope.tags = [];
    var tagsLoader = Restangular.all('tags');

    $scope.search = function() {
        if ($scope.searchTag !== '') {
            $scope.status = 1;
            $scope.busy = true;

            tagsLoader.getList({q: $scope.searchTag}).then(function(tags) {
                _.map(tags, function(tag) {
                    tag.tagsCsv = tag.tags.join(",");
                });
                $scope.tags = tags;
                $scope.status = 0;
            });

        }
    };

    $scope.editTag = function(event, tag) {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-tag.html?v=" + NationStory.appSettings.ver,
            controller: "TagEditController",
            inputs: {
                tag: tag
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(tag) {
                tag.tags = tag.tagsCsv.split(',');
                tag.put();
            });
        });
    };

    $scope.removeTag = function(event, tag) {
        var tagWithId = _.find($scope.tags, function(s) {
            return tag._id === s._id;
        });

        tag.remove().then(function() {
            var index = $scope.tags.indexOf(tagWithId);
            if (index > -1) $scope.tags.splice(index, 1);
        });
    };

    $scope.addNewTag = function() {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-tag.html?v=" + NationStory.appSettings.ver,
            controller: "TagEditController",
            inputs: {
                tag: {}
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(tag) {
                tag.tags = tag.tagsCsv.split(',');
                tagsLoader.post(tag).then(function(newTag) {
                    newTag.tagsCsv = newTag.tags.join(',');
                    $scope.tags.push(newTag);
                  }, function() {
                    console.log("There was an error saving");
                  });
            });
        });
    };
})

.controller('TagEditController', function($scope, tag, $element, close) {
    $scope.tag = tag;
    $scope.new = false;

    if (!$scope._id) {
        $scope.new = true;
    }
    $scope.saveTag = function() {
        $element.modal('hide');
        close(tag, 200);
    };

    $scope.dismissModal = function(result) {
        close(null, 200); // close, but give 200ms for bootstrap to animate
     };
});