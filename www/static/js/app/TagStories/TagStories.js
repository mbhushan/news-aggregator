'use strict';

angular.module('TagStories', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/tag/:tagId', {
        templateUrl: '/static/ui/stories.html?v=' + NationStory.appSettings.ver,
        controller: 'TagStoriesController'
    });
}])

.controller('TagStoriesController', function($scope, $routeParams, Stories, $http) {
    $scope.stories = new Stories();
    $scope.tag = $routeParams.tagId;
    $scope.stories.url = '/api/tag/' + $scope.tag;

    var init = function() {
        _gaq.push(['_trackEvent', 'tagload', $scope.tag]);

        if (NationStory.userSettings.topics) {
            for (var i=0; i<NationStory.userSettings.topics.length; i++) {
                if (NationStory.userSettings.topics[i].name == $scope.tag) {
                    NationStory.userSettings.topics[i].count = 0
                }
            }
            $scope.$emit('pinnedTopics:changed');
        }
        $scope.$emit('navTopic:changed', $scope.tag);
    }

    init();

    $scope.isPinned = function() {
        if (NationStory.userSettings && NationStory.userSettings.topics) {
            for (var i=0; i<NationStory.userSettings.topics.length; i++) {
                if (NationStory.userSettings.topics[i].name == $scope.tag) {
                    return true;
                }
            }
        }
        return false;
    };

    $scope.pinTag = function(e) {
        $http.post('/api/pintopic', {topic: $scope.tag, action:'add'})
            .success(function(data) {
                NationStory.notify('You have started following ' + $scope.tag.replace(/-/g, ' ') + '.', "success");
                NationStory.userSettings.topics.push({name:$scope.tag, count: 0});
                $scope.$emit('pinnedTopics:changed');
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NationStory.notify("You need to log in to pin this topic.", "error");
                    return;
                }
                var message="Some error happened";
                if (data.message) {
                    message = data.message;
                }
                NationStory.notify(message, "error");
            });
    };

    $scope.unpinTag = function(e) {
        $http.post('/api/pintopic', {topic: $scope.tag, action:'remove'})
            .success(function(data) {
                NationStory.notify('You have stopped following ' + $scope.tag.replace(/-/g, ' ') + '.', "success");
                var index = -1;
                for (var i=0; i<NationStory.userSettings.topics.length; i++) {
                    if (NationStory.userSettings.topics[i].name == $scope.tag) {
                        index = i;
                    }
                }
                NationStory.userSettings.topics.splice(index, 1);

                $scope.$emit('pinnedTopics:changed');
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NationStory.notify("You need to log in to follow this topic.", "error");
                    return;
                }
                var message="Some error happened";
                if (data.message) {
                    message = data.message;
                }
                NationStory.notify(message, "error");
            });
    };
});