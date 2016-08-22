'use strict';

angular.module('Story', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/story/:storyId', {
        templateUrl: '/static/ui/story.html?v=' + NationStory.appSettings.ver,
        controller: 'StoryController'
    });
}])

.factory('Story', function($http) {
    var Story = function(storyId) {
        this.item = null;
        this.busy = false;
        this.storyId = storyId;
        this.ready = false;
        this.getLink = function() {
            return NationStory.appSettings.app_url + '/story/' + this.item._id;
        };
    };

    Story.prototype.fetch = function() {
        if (this.busy) return;
        this.busy = true;

        var url = "/api/stories/" + this.storyId;
        $http.get(url).success(function(data) {
            this.busy = false;
            this.ready = true;
            this.item = data.story;
            this.item.base_link = this.item.link.split('/')[2];
        }.bind(this));
    };

    return Story;
})

.controller('StoryController', function($scope, $routeParams, Story) {
    $scope.storyId = $routeParams.storyId;
    $scope.story = new Story($scope.storyId);

    var init = function() {
        $scope.story.fetch();
    };
    init();
});