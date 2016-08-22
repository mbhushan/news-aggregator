$(document).ready(function() {
    for(var i=0; i<NationStory.messages.length; i++) {
        NationStory.notify(NationStory.messages[i].message, NationStory.messages[i].type);
    }

     $('[data-toggle="tooltip"]').tooltip();
});

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.3";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

window.fbAsyncInit = function() {
  FB.init({
    appId      : NationStory.appSettings.facebook,
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.1' // use version 2.1
  });
};

window.twttr=(function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],t=window.twttr||{};if(d.getElementById(id))return t;js=d.createElement(s);js.id=id;js.src="https://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);t._e=[];t.ready=function(f){t._e.push(f);};return t;}(document,"script","twitter-wjs"));

function signinCallback(authResult) {
    if (authResult['status']['signed_in']) {
        if (authResult['status']['method'] == 'AUTO') {
            return;
        }
        $.ajax({
            url: "/register/google",
            type: 'POST',
            data : {token: authResult.access_token},
            dataType: "json",
            success: function(data) {
                window.location.reload();
            },
            error: function() {
                $('#modal').modal();
            }
        });
        } else {}
}

function googleSingin() {
    var additionalParams = {
        'callback': signinCallback,
        'clientid': NationStory.appSettings.google
    };
    gapi.auth.signIn(additionalParams);
}

function fbSingin() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            $.ajax({
              url: "/register/facebook",
              type: 'POST',
              data : {token: response.authResponse.accessToken},
              dataType: "json",
              success: function(data) {
                  window.location.reload();
              },
              error: function() {
                  $('#login-modal').modal();
              }
            });

        } else if (response.status === 'not_authorized') {
            $('#login-modal').modal();
        } else {
            $('#login-modal').modal();
        }
    }, {scope: 'public_profile,email'});
}


(function() {
    var app = angular.module('nationStory',
                             ['infinite-scroll', 'ngRoute', 'angucomplete', 'About','Contact', 'Profile', 'Opinion',
                              'Write','Story', 'Stories', 'angularModalService', 'Comments', 'angularSpinner']);

    app.config(['$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }]);

    app.config(function($sceDelegateProvider) {
      $sceDelegateProvider.resourceUrlWhitelist([
        // Allow same origin resource loads.
        'self',
        // Allow loading from our assets domain.  Notice the difference between * and **.
        'https://www.youtube.com/**'
      ]);
    });


    app.config(function($routeProvider, $locationProvider) {
        $routeProvider.
            otherwise({ redirectTo: '/' });

            // configure html5 to get links working on jsfiddle
            $locationProvider.html5Mode(true);
    })
    .run( function($rootScope, $location) {
        if (NationStory.userSettings.id && NationStory.userSettings.username == '') {
            $location.path('/profile');
        }
    });

    app.filter('removehypens', function(){
        return function(text) {
            if (!text) {
                return text;
            }
            return text.replace(/-/g, ' ');
        };
    });

    app.controller('MainController', function($scope, $route, $routeParams, $location, $rootScope, $http, ModalService, Comments, $window) {
        $scope.$route = $route;
        $scope.$location = $location;
        $scope.$routeParams = $routeParams;
        $scope.relatedTopics = [];
        $scope.pinnedTopics = [];
        $scope.navTopic = null;
        $scope.searchTag = null;
        $scope.editPinsText = 'edit';
        $scope.editMode = false;
        $scope.smSidebarVisible = 0;
        $scope.showTrailer = false;
        $scope.postBtnText = 'Post';
        $scope.sidebarHidden = false;
        $scope.showLogin = false;

        if (NationStory.userSettings.location_topics) {
            $scope.locationTopics = NationStory.userSettings.location_topics;
        } else {
            $scope.locationTopics = [];
        }

        if (NationStory.userSettings.video_cards) {
            $scope.videoCards = NationStory.userSettings.video_cards;
        } else {
            $scope.videoCards = [];
        }

        $scope.opinions = NS.appSettings.opinions ? NS.appSettings.opinions : [];

        $scope.editPins = function(e) {
            e.preventDefault();
            if ($scope.editMode) {
                $scope.editMode = false;
                $scope.editPinsText = 'edit';
            } else {
                $scope.editMode = true;
                $scope.editPinsText = 'done';
            }
        };

        $scope.playTrailer = function(videoCard) {
            $scope.showTrailer = true;
            $scope.trailerVideoCard = videoCard;

            $scope.trailerComments = new Comments();
            $scope.trailerComments.id = videoCard._id;
            $scope.trailerComments.type = 'video_card';

            $scope.trailerComments.nextPage();
        };

        $scope.submitTrailerComment = function() {
            if (!NS.userSettings.id) {
                NationStory.notify('You need to log in to post comments.', "error");
            } else {
                $scope.postBtnText = 'Posting';
                $http.post('/api/comments', {text: $scope.newTrailerComment, id: $scope.trailerVideoCard._id, type: 'video_card'})
                    .success(function(data) {
                        $scope.postBtnText = 'Post';
                        $scope.newTrailerComment = '';
                        $scope.trailerComments.items.unshift(data.comment);
                    }.bind(this))
                    .error(function(data, status, headers, config) {
                        if (status == 401) {
                            NationStory.notify("You need to log in to post comment.", "error");
                            return;
                        }
                        var message="Some unknown error happened";
                        if (data.message) {
                            message = data.message;
                        }
                        NationStory.notify(message, "error");
                        $scope.postBtnText = 'Post';
                    });
            }
        };

        $scope.closeOverlay = function(event) {
            if (angular.element(event.target).hasClass('close-overlay')) {
                $scope.showTrailer = false;
                $scope.showLogin = false;
                $scope.trailerVideoCard = {};
            }

        };

        $scope.startLogin = function() {
            $scope.showLogin = true;
        };

        $scope.showWrite = function() {
            if (NS.userSettings.id) {
                $window.location = '/write';
            } else {
                $scope.startLogin();
            }
        };


        $scope.track = function(type, subType) {
            _gaq.push(['_trackEvent', 'tagclick', type, subType]);
        };

        $scope.$watch('searchTag', function() {
            if ($scope.searchTag && $scope.searchTag.originalObject) {
                _gaq.push(['_trackEvent', 'search', $scope.searchTag.originalObject.tag]);
                $location.path('/tag/' + $scope.searchTag.originalObject.tag);
            }
        });

        $scope.isRouteActive = function(name) {
            if (name == 'home' && $location.url() == '/') {
                return true;
            } else if (name == 'explore' && $location.url() == '/explore') {
                return true;
            }
            return false;
        };

        $scope.isActive = function(tabName) {
            if (tabName == $scope.navTopic) {
                return true;
            }
            return false;
        };

        $scope.setupPinnedTopics = function() {
            if (NationStory.userSettings.topics) {
                $scope.pinnedTopics = NationStory.userSettings.topics;
            } else {
                $scope.pinnedTopics = [];
            }
        };

        $scope.setupTrendingTopics = function() {
            if (NationStory.userSettings.trending) {
                $scope.trendingTopics = NationStory.userSettings.trending;
            } else {
                $scope.trendingTopics = [];
            }
        };

        $scope.setupRelatedTopics = function(event, topics) {
            if (!topics) {
                $scope.relatedTopics = [];
            } else {
                $scope.relatedTopics = topics;
            }
        };

        $scope.navTopicChanged = function(event, navTopic) {
            $scope.navTopic = navTopic;
            $scope.closeSmSidebar();
        };

        $scope.removePin = function(tag) {
            $http.post('/api/pintopic', {topic: tag, action:'remove'})
            .success(function(data) {
                NationStory.notify('You have stopped following ' + tag.replace(/-/g, ' ') + '.', "success");
                var index = -1;
                for (var i=0; i<NationStory.userSettings.topics.length; i++) {
                    if (NationStory.userSettings.topics[i].name == tag) {
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

        $scope.sendFeedback = function() {
            $scope.closeSmSidebar();
            ModalService.showModal({
                templateUrl: "/static/ui/Feedback/feedback.html?v=" + NationStory.appSettings.ver,
                controller: "FeedbackController"
            }).then(function(modal) {
                modal.element.modal();
            });
        };

        $scope.showSmSidebar = function() {
            if ($scope.smSidebarVisible) {
                $scope.smSidebarVisible = false;
            } else {
                $scope.smSidebarVisible = true;
            }
        };

        $scope.closeSmSidebar = function() {
            $scope.smSidebarVisible = false;
        };

        $scope.hideSidebar = function() {
            $scope.sidebarHidden = true;
        };

        $scope.showSidebar = function() {
            $scope.sidebarHidden = false;
        };

        $scope.setupPinnedTopics();
        $scope.setupTrendingTopics();

        $scope.$on('navTopic:changed', $scope.navTopicChanged);
        $scope.$on('pinnedTopics:changed', $scope.setupPinnedTopics);
        $scope.$on('sidebar:hide', $scope.hideSidebar);
        $scope.$on('sidebar:show', $scope.showSidebar);

        $rootScope.$on('relatedTopics:changed', $scope.setupRelatedTopics);
    });

    app.controller('FeedbackController', function($scope, $http, $element, close) {
        $scope.email = '';
        $scope.feedback = '';
        $scope.authenticated = false;
        $scope.emailError = false;
        $scope.feedbackError = false;

        if (NS.userSettings.id) {
            $scope.authenticated = true;
        }
        $scope.sendFeedback = function() {
            $scope.emailError = false;
            $scope.feedbackError = false;

            if (!$scope.authenticated && $scope.email.trim() == '') {
                $scope.emailError = true;
                return;
            }

            if ($scope.feedback.trim() == '') {
                $scope.feedbackError = true;
                return;
            }

            $http.post('/api/feedback', {'feedback': $scope.feedback, email:$scope.email})
            .success(function(data) {
                NationStory.notify("Thank you for submitting your feedback!", "success");
            }.bind(this))
            .error(function(data, status, headers, config){
                var message = "There was an error in submitting feedback. Please try again!";
                if (data && data.status) {
                    message = data.message;
                }
                NationStory.notify(message, "error");
            });

            $element.modal('hide');
            close(null, 200);
            $('.modal-backdrop').remove();
        };

        $scope.dismissModal = function(result) {
            close(null, 200); // close, but give 200ms for bootstrap to animate
         };

    });

    app.directive('movieTrailer', function() {
        return {
            restrict: 'E',
            templateUrl: '/static/ui/movie-trailer.html?v=' + NationStory.appSettings.ver
        };
    });

    app.directive('commentsBlock', function() {
        return {
            restrict: 'E',
            templateUrl: '/static/ui/comments.html?v=' + NationStory.appSettings.ver
        };
    });

    app.directive('loginBlock', function() {
        return {
            restrict: 'E',
            templateUrl: '/static/ui/login.html?v=' + NationStory.appSettings.ver
        };
    });


})();