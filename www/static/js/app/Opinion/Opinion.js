'use strict';

angular.module('Opinion', ['ngRoute', 'ngSanitize'])

.config(['$routeProvider', function($routeProvider) {

    $routeProvider.when('/opinion/:opinionId', {
        templateUrl: '/static/ui/opinion.html?v=' + NationStory.appSettings.ver,
        controller: 'OpinionController'
    });

    $routeProvider.when('/opinions', {
        templateUrl: '/static/ui/opinions.html?v=' + NationStory.appSettings.ver,
        controller: 'OpinionsController'
    });

}])

.controller('OpinionController', function($scope, $routeParams, $http, $rootScope, Comments, $timeout) {
    $scope.$emit('sidebar:hide', '');
    $scope.busy = true;
    $scope.opinionId = $routeParams.opinionId;
    $scope.errorMsg = false;

    $http.get('/api/opinion/' + $scope.opinionId).success(function(data) {
        $scope.story = data.story;
        $scope.user = data.user;
        $scope.busy = false;

        $timeout(function() {
            twttr.widgets.load();
            FB.XFBML.parse();
        }, 800);
    }.bind(this))
    .error(function(data, status, headers, config) {
        var message="Some unknown error happened.";
        if (data.message) {
            message = data.message;
        }
        $scope.errorMsg = message;
        $scope.busy = false;
    });

    $scope.comments = new Comments();
    $scope.comments.id = $routeParams.opinionId;
    $scope.comments.type = 'opinion';
    $scope.comments.nextPage();

    $scope.submitComment = function() {
        if (!NS.userSettings.id) {
            NationStory.notify('You need to log in to post comments.', "error");
        } else {
            $scope.postBtnText = 'Posting';
            $scope.comments.post($scope.commentText);
        }
    };

    this.commentPosted = function() {
        $scope.postBtnText = 'Post';
        $scope.commentText = '';
    };

    this.commentPostError = function(event, message) {
        NS.notify(message, 'error');
        $scope.postBtnText = 'Post';
    };

    $scope.recommend = function(item) {
        if (item.has_recommended) {
            return;
        }

        if (!NS.userSettings.id) {
            NS.notify('Please log in to recommend this story.', 'error');
            return;
        }

        item.recommendation++;
        item.has_recommended = true;

        $http.post('/api/opinion/' + $scope.opinionId).success(function(data) {

        }.bind(this))
        .error(function(data, status, headers, config) {
            item.recommendation++;
            item.has_recommended = false;

            var message="Some unknown error happened.";
            if (data.message) {
                message = data.message;
            }
            NS.notify(message, 'error');
        }.bind(this));
    };

    $rootScope.$on('comments:added', this.commentPosted);
    $rootScope.$on('comments:posterror', this.commentPostError);
})

.controller('OpinionsController', function($scope, $routeParams, $http, $rootScope, Comments, $timeout, Stories) {
    $scope.$emit('sidebar:hide', '');
    $scope.errorMsg = false;

    $scope.stories = new Stories();
    $scope.stories.url = '/api/opinions';
    $scope.stories.userStories = true;

    $scope.recommend = function(item) {
        if (item.has_recommended) {
            return;
        }

        if (!NS.userSettings.id) {
            NS.notify('Please log in to recommend this story.', 'error');
            return;
        }

        item.recommendation++;
        item.has_recommended = true;

        $http.post('/api/opinion/' + $scope.opinionId).success(function(data) {

        }.bind(this))
        .error(function(data, status, headers, config) {
            item.recommendation++;
            item.has_recommended = false;

            var message="Some unknown error happened.";
            if (data.message) {
                message = data.message;
            }
            NS.notify(message, 'error');
        }.bind(this));
    };

});