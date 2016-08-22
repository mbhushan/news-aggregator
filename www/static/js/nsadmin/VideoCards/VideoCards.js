'use strict';

angular.module('VideoCards', ['ngRoute', 'restangular', 'angularModalService'])

.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/nsadmin/video-cards', {
        templateUrl: '/static/ui/nsadmin/video-cards.html?v=' + NationStory.appSettings.ver,
        controller: 'VideoCardsController'
    });
}])

.controller('VideoCardsController', function($scope, $routeParams, Restangular, ModalService) {
    var videoCardsLoader = Restangular.all('video_cards');
    $scope.busy = true;

    videoCardsLoader.getList().then(function(videoCards){
        $scope.videoCards = videoCards;
        $scope.busy = false;
    });

    $scope.editSource = function(event, videoCard) {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-video-card.html?v=" + NationStory.appSettings.ver,
            controller: "VideoCardEditController",
            inputs: {
                videoCard: videoCard
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(videoCard) {
                videoCard.put();
            });
        });
    };

    $scope.removeSource = function(event, videoCard) {
        var withId = _.find($scope.videoCards, function(s) {
            return videoCard._id === s._id;
        });

        videoCard.remove().then(function() {
            var index = $scope.videoCards.indexOf(withId);
            if (index > -1) $scope.videoCards.splice(index, 1);
        });
    };

    $scope.addNewSource = function() {
        ModalService.showModal({
            templateUrl: "/static/ui/nsadmin/edit-video-card.html?v=" + NationStory.appSettings.ver,
            controller: "VideoCardEditController",
            inputs: {
                videoCard: {}
            }
        }).then(function(modal) {
            modal.element.modal();
            modal.close.then(function(videoCard) {
                videoCardsLoader.post(videoCard).then(function(newVideoCard) {
                    $scope.videoCards.push(newVideoCard);
                  }, function() {
                    alert("There was an error saving");
                  });
            });
        });
    };
})

.controller('VideoCardEditController', function($scope, videoCard, $element, close, $http) {
    $scope.videoCard = videoCard;

    $scope.saveSource = function() {
        $element.modal('hide');
        close($scope.videoCard, 200);
    };

    $scope.dismissModal = function(result) {
        close(null, 200); // close, but give 200ms for bootstrap to animate
     };
});
