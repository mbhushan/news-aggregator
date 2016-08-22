'use strict';

angular.module('Profile', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/user/:username', {
        templateUrl: '/static/ui/user-profile.html?v=' + NationStory.appSettings.ver,
        controller: 'ProfileController'
    });

    $routeProvider.when('/profile', {
        templateUrl: '/static/ui/profile-edit.html?v=' + NationStory.appSettings.ver,
        controller: 'EditProfileController'
    });
}])

.controller('EditProfileController', function($scope, $routeParams, $http, $window) {
    if (!NS.userSettings.id) {
        $window.location = '/';
    }
    $scope.user = NationStory.userSettings;
    $scope.tos = false;
    $scope.tosError = false;
    $scope.errorMsg = false;
    $scope.tosHide = true;

    if ($scope.user.username == '') {
        $scope.user.username = $scope.user.suggested;
//         $scope.tosHide = false;
    }

    $scope.$emit('sidebar:hide', '');

    $scope.saveProfile = function() {
        $scope.errorMsg = false;
        $scope.tosError = false;

        var reg = RegExp("^[a-z0-9_]+$");
        if ($scope.user.username == '' || !reg.test($scope.user.username)) {
            $scope.errorMsg = "Username is invalid.";
            return;
        }

        if ($scope.user.name.trim() == '') {
            $scope.errorMsg = "Name can not be empty.";
            return;
        }

        if (!$scope.tosHide && !$scope.tos) {
            $scope.errorMsg = "You must accept our terms of service.";
            return;
        }

        var params = {username: $scope.user.username, name: $scope.user.name, bio: $scope.user.bio,
                      website: $scope.user.website, facebook_profile: $scope.user.facebook_profile,
                      twitter_profile: $scope.user.twitter_profile};

        $http.post('/api/profile', $.param(params),
            {headers:{'Content-Type': 'application/x-www-form-urlencoded'}}
            ).success(function(data, status, headers, config) {
                $window.location.href = '/';
            }.bind(this))
            .error(function(data, status, headers, config){
                $scope.errorMsg = data.message;
            });
    };
})

.controller('ProfileController', function($scope, $routeParams, $http, $window, Stories) {
    $scope.$emit('sidebar:hide', '');
    $scope.username = $routeParams.username;
    $scope.userStories = true;
    $scope.profileBusy = true;
    $scope.profileErrorMsg = false;

    if ($scope.username == NS.userSettings.username) {
        $scope.user = NS.userSettings;
        $scope.profileBusy = false;
    } else {
        //load profile
        $http.get('/api/profile/' + $scope.username).success(function(data) {
            $scope.user = data.user;
            $scope.profileBusy = false;
        }.bind(this))
        .error(function(data, status, headers, config) {
            var message="Some unknown error happened.";
            if (data.message) {
                message = data.message;
            }
            $scope.profileBusy = false;
            $scope.profileErrorMsg = message;
        });
    }

    $scope.isEditable = function(item) {
        return item.user_id == NS.userSettings.id;
    };

    $scope.getNoStoryText = function() {
        if ($scope.username == NS.userSettings.username) {
            return 'You have not submitted any story.';
        } else {
            return 'User has not submitted any story.';
        }
    };

    $scope.stories = new Stories();
    $scope.stories.url = '/api/opinions/' + $scope.username;

});