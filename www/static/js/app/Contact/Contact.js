'use strict';

angular.module('Contact', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/contact', {
        templateUrl: '/static/ui/contact.html?v=' + NationStory.appSettings.ver,
        controller: 'ContactController'
    });
}])

.controller('ContactController', function($scope, $routeParams, $http) {
    $scope.email = '';
    $scope.feedback = '';
    $scope.authenticated = false;
    $scope.emailError = false;
    $scope.feedbackError = false;
    $scope.sendText = 'Send';
    $scope.alertMsg = '';
    $scope.alertType = '';

    if (NS.userSettings.id) {
        $scope.authenticated = true;
        $scope.email = NS.userSettings.email;
    }
    $scope.sendFeedback = function() {
        $scope.alertMsg = '';
        $scope.alertType = '';

        $scope.emailError = false;
        $scope.feedbackError = false;

        if ($scope.email.trim() == '') {
            $scope.emailError = true;
            return;
        }

        if ($scope.feedback.trim() == '') {
            $scope.feedbackError = true;
            return;
        }

        $scope.sendText = 'Sending';

        $http.post('/api/feedback', {'feedback': $scope.feedback, email:$scope.email})
        .success(function(data) {
            $scope.sendText = 'Send';
            $scope.alertMsg = 'Your request has been received. We will respond to your request in 24 hours.';
            $scope.alertType = 'success';
        }.bind(this))
        .error(function(data, status, headers, config){
            $scope.sendText = 'Send';
            var message = "There was an error in submitting your request. Please try again or use one of the email addresses mentioned on the left.";
            if (data && data.status) {
                message = data.message;
            }
            $scope.alertMsg = message;
            $scope.alertType = 'danger';
        });
    };

});