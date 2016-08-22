'use strict';

angular.module('Stories', ['ngRoute', 'ngAnimate', 'angularSpinner'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: '/static/ui/stories.html?v=' + NationStory.appSettings.ver,
        controller: 'StoriesController',
        resolve: {
            special: function () { return null; }
        }
    })
    .when('/tag/:tagId', {
        templateUrl: '/static/ui/stories.html?v=' + NationStory.appSettings.ver,
        controller: 'StoriesController',
        resolve: {
            special: function () { return null; }
        }
    })
    .when('/:path', {
        templateUrl: '/static/ui/stories.html?v=' + NationStory.appSettings.ver,
        controller: 'StoriesController',
        resolve: {
            special: function () { return null; }
        }
    });
}])

.factory('Stories', function($http, $rootScope) {
    var Stories = function() {
        this.items = [];
        this.relatedTopics = [];
        this.busy = false;
        this.after = '';
        this.url = "/api/stories";
        this.userStories = false; //supress some features when loading user stories

        this.getLink = function(item, type) {
            if (type) {
                return NS.appSettings.app_url + '/' + type + '/' + item._id;
            }
            return NS.appSettings.app_url + '/story/' + item._id;
        };
    };

    Stories.prototype.nextPage = function() {
        if (this.busy || this.after == -1) return;
        this.busy = true;
        var args;
        if (this.after) {
            args = {
                t: this.after
            };
        } else {
            args = {};
        }

        $http.get(this.url, {
                params: args
            }).success(function(data) {
                for (var i = 0; i < data.stories.length; i++) {
                    this.items.push(data.stories[i]);
                }

                if (!this.userStories) {
                    if (data.related_tags) {
                        this.relatedTopics = data.related_tags;
                    } else {
                        this.relatedTopics = [];
                    }
                    $rootScope.$emit('relatedTopics:changed', this.relatedTopics);
                }

                if (!data.t) {
                    this.after = -1;
                } else {
                    this.after = data.t;
                }
                this.busy = false;
            }.bind(this)).
            error(function(data, status, headers, config){
                this.busy = false;
            }.bind(this));
    };

    return Stories;
})

.controller('StoriesController', function($scope, $routeParams, Stories, $http, $location, $route, special) {
    $scope.showCategories = false;
    $scope.stories = new Stories();

    $scope.$emit('sidebar:show', '');

    if ($routeParams.tagId) {
        $scope.tag = $routeParams.tagId;
        $scope.storyType = $scope.tag;
        $scope.stories.url = '/api/tag/' + $scope.tag;
        _gaq.push(['_trackEvent', 'tagload', 'headlines']);
    } else if ($routeParams.path) {
        if ($routeParams.path == 'all') {
            $scope.storyType = 'all news';
            _gaq.push(['_trackEvent', 'tagload', 'all']);
        } else {
            $scope.storyType = $routeParams.path;
            $scope.stories.url = '/api/source/' + $routeParams.path;
            _gaq.push(['_trackEvent', 'tagload', 'all']);
        }

    } else {
        $scope.stories.url = '/api/headlines';
        $scope.storyType = 'headlines';

        if (NS.appSettings.headlines) {
            $scope.stories.items = NS.appSettings.headlines.stories;
            $scope.stories.after = NS.appSettings.headlines.t;

            NS.appSettings.headlines = null;
        }
    }

    var init = function() {
        $scope.$emit('navTopic:changed', '');
        if ($scope.tag) {
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
    };

    init();

    $scope.toggleCategories = function() {
        $scope.showCategories = !$scope.showCategories;
    };

//     $scope.changeStoryType = function(storyType) {
//         $scope.showCategories = false;
//         if ($scope.storyType == storyType) {
//             return;
//         }
//         $scope.storyType = storyType;
//         $scope.tag = null;
//         $location.url('/');
//     };

    $scope.isStoryTypeActive = function(storyType) {
        if ($scope.storyType == storyType) {
            return true;
        }
        return false;
    }

//     $scope.$watch('storyType', function(newval, oldval){
//         _gaq.push(['_trackEvent', 'homepage', newval]);
// //         if (newval == oldval) {
// //             return;
// //         }
//
//         if (newval == 'headlines') {
//             $scope.stories = new Stories();
//             $scope.stories.url = '/api/headlines';
//         } else if (newval == 'all news') {
//             $scope.stories = new Stories();
//         } else {
//             $scope.stories = new Stories();
//             $scope.stories.url = '/api/tag/' + newval;
//         }
//
//         $scope.stories.nextPage();
//     });

    $scope.upvote = function($event, item) {
        if (item.upvoted) {
            return;
        }
        $http.post('/api/vote/' + item._id + '/upvote')
            .success(function(data) {
                this.item.votes = data.votes;
                this.item.downvoted = data.downvoted;
                this.item.upvoted = data.upvoted;
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NationStory.notify("You need to log in to up vote.", "error");
                    return;
                }
                NationStory.notify(data.message, "error");
            });
    };

    $scope.downvote = function($event, item) {
        if (item.downvoted) {
            return;
        }
        $http.post('/api/vote/' + item._id + '/downvote')
            .success(function(data) {
                this.item.votes = data.votes;
                this.item.downvoted = data.downvoted;
                this.item.upvoted = data.upvoted;
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NationStory.notify("You need to log in to down vote.", "error");
                    return;
                }
                NationStory.notify(data.message, "error");
            });
    };

    $scope.isPinned = function() {
        if (NationStory.userSettings && NationStory.userSettings.topics) {
            for (var i=0; i<NationStory.userSettings.topics.length; i++) {
                if (NationStory.userSettings.topics[i].name == $scope.tag) {
                    return true;
                }
            }
        }
        if (['sports', 'entertainment', 'politics'].indexOf($scope.tag) != -1) {
            return true;
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
