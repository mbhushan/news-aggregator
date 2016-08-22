'use strict';

angular.module('UserStories', ['ngRoute', 'angularModalService'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/nsadmin/user-stories', {
        templateUrl: '/static/ui/nsadmin/user-stories.html?v=' + NationStory.appSettings.ver,
        controller: 'UserStoriesController'
    });
}])

.factory('UserStories', function($http, $rootScope) {
    var UserStories = function() {
        this.items = [];
        this.relatedTopics = [];
        this.busy = false;
        this.after = '';
        this.url = "/api/admin/userstories";
        this.userStories = false; //supress some features when loading user stories

        this.getLink = function(item) {
            return NS.appSettings.app_url + '/opinion/' + item._id;
        };

        this.getTitle = function(item) {
            if (item.status == 0) {
                return item.draft.title;
            } else {
                return item.title;
            }
        };

        this.getStatus = function(item) {
            switch(item.status) {
                case 0:
                    return 'Draft';
                case 1:
                    return 'Pending Approval';
                case 2:
                    return 'Approved';
                case 3:
                    return 'Disapproved';
            }
        };
    };

    UserStories.prototype.nextPage = function() {
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

    return UserStories;
})


.controller('UserStoriesController', function($scope, $routeParams, $http, UserStories, ModalService) {
    $scope.userStories = new UserStories();

    $scope.approve = function($event, item) {
        $http.post('/api/admin/userstories', {_id: item._id, action: 'approve'})
            .success(function(data) {
                NS.notify('Successfully approved', 'success');
                item.status = 2;
            }.bind(this))
            .error(function(data, status, headers, config) {
                var message="Some unknown error happened";
                if (data.message) {
                    message = data.message;
                }
                NS.notify(message, 'error');
            });
    };

    $scope.disapprove = function($event, item) {
        $http.post('/api/admin/userstories', {_id: item._id, action: 'disapprove'})
            .success(function(data) {
                NS.notify('Successfully disapproved', 'success');
                item.status = 3;
            }.bind(this))
            .error(function(data, status, headers, config) {
                var message="Some unknown error happened";
                if (data.message) {
                    message = data.message;
                }
                NS.notify(message, 'error');
            });
    };

});