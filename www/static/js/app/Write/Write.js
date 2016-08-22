'use strict';

angular.module('Write', ['ngRoute', 'ngSanitize'])

.config(['$routeProvider', function($routeProvider) {

    $routeProvider.when('/write', {
        templateUrl: '/static/ui/write.html?v=' + NationStory.appSettings.ver,
        controller: 'WriteController'
    });

    $routeProvider.when('/write/:storyId', {
        templateUrl: '/static/ui/write.html?v=' + NationStory.appSettings.ver,
        controller: 'WriteController'
    });
}])

.controller('WriteController', function($scope, $routeParams, $http, $window, $interval, Stories, ModalService) {
    if (!NS.userSettings.id) {
        $window.location = '/';
    }

    $scope.$emit('sidebar:hide', '');
    $scope.title = '';
    $scope._id = $routeParams.storyId;
    $scope.body = '';
    $scope.busy = false;
    $scope.errorMsg = '';
    $scope.story = null;
    $scope.coverPhoto = '';
    $scope.hideCoverPhotoUpload = false;
    var original = {'title': $scope.title, 'body': $scope.body};

    $scope.stories = new Stories();
    $scope.stories.url = '/api/opinions/' + NS.userSettings.username;
    $scope.stories.nextPage();

    var setupEditor = function() {
        $('#editor').wysiwyg({activeToolbarClass: 'btn-highlight', uploadUrl: '/api/photoupload', overlayClass:"editor-overlay"});
        $('.editor-container a').tooltip();
        original = {'title': $scope.title, 'body': $scope.body};
    };

    $scope.loadPost = function() {
        $scope.busy = true;

        $http.get('/api/userstories/' + $scope._id).success(function(data) {
            $scope.story = data.story;

            if (data.story.status == 0 && data.story.draft) {
                $scope.title = data.story.draft.title;
                $scope.body = data.story.draft.body;
                $scope.coverPhoto = data.story.draft.cover_pic;
            } else {
                $scope.title = data.story.title;
                $scope.body = data.story.body;
                $scope.coverPhoto = data.story.cover_pic;

                if (data.story.draft) {
                    $scope.draftAvailable = true;
                }
            }
            $scope.busy = false;
            setupEditor();
        }.bind(this))
        .error(function(data, status, headers, config) {
            var message="Some unknown error happened.";
            if (data.message) {
                message = data.message;
            }
            $scope.errorMsg = message;
            $scope.busy = false;
        }.bind(this));

    };

    if ($scope._id) {
        $scope.loadPost();
    } else {
        setupEditor();
    }

    $scope.editDraft = function() {
        $scope.title = $scope.story.draft.title;
        $scope.body = $scope.story.draft.body;
        $scope.coverPhoto = $scope.story.draft.cover_pic;

        $scope.draftAvailable = false;
    }

    $scope.inputClicked = function(e) {
        e.stopPropagation();
    };

    $scope.publishPost = function() {
        var post = {_id: $scope._id, title: $scope.title, body: $('#editor').cleanHtml(),
                    action: 'publish', cover_pic: $scope.coverPhoto};
        $http.post('/api/userstories', post)
            .success(function(data) {
                $scope._id = data._id;
                //NationStory.notify('Your post has been published.', "success");
                resetOriginal();
                $window.location = '/opinion/' + data._id;
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NS.notify("You need to log in to do this action.", "error");
                    return;
                }
                if (data.message) {
                    NS.notify(data.message, "error");
                } else {
                    NS.notify("Server encountered an error.", "error");
                }
            });
    };

    $scope.saveDraft = function() {
        var post = {_id: $scope._id, title: $scope.title, body: $('#editor').cleanHtml(),
                    action: 'draft', cover_pic: $scope.coverPhoto};

        $http.post('/api/userstories', post)
            .success(function(data) {
                $scope._id = data._id;
                NationStory.notify('Your draft has been saved.', "success");
                resetOriginal();
            }.bind(this))
            .error(function(data, status, headers, config){
                if (status == 401) {
                    NS.notify("You need to log in to do this action.", "error");
                    return;
                }
                if (data.message) {
                    NS.notify(data.message, "error");
                } else {
                    NS.notify("Server encountered an error.", "error");
                }
            });
    };

    var resetOriginal = function(){
        original = {'title': $scope.title, 'body': $scope.body};
    };

    $scope.saveDiff = function() {
        if ($scope.title != original.title || $scope.body != original.body) {
            var post = {_id: $scope._id, title: $scope.title, body: $('#editor').cleanHtml(),
                        action: 'draft', cover_pic: $scope.coverPhoto};

            $http.post('/api/userstories', post)
                .success(function(data) {
                    $scope._id = data._id;
                    resetOriginal();
                }.bind(this));
        }
    };

    $scope.uploadCoverImage = function(element) {

        var data = new FormData();
        $.each(element.files, function (idx, fileInfo) {
            data.append('file', fileInfo);
        });


        var spinner = new Spinner().spin();
        $('.editor-cover-photo-container').append(spinner.el);
        $('.editor-cover-overlay').addClass('white-bg');

         $.ajax({
             url: '/api/photoupload',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false, // Don't process the files
             contentType: false, // Set content type to false as jQuery will tell the server its a query string request
             context: this,
             success: function(data, textStatus, jqXHR) {
                $scope.coverPhoto = data.url;
                $scope.$apply();
                $('.editor-cover-photo-container .spinner').remove();
                $('.editor-cover-overlay').removeClass('white-bg');
             },
             error: function(jqXHR, textStatus, errorThrown)
             {
                $('.editor-cover-photo-container .spinner').remove();
                $('.editor-cover-overlay').removeClass('white-bg');
                NS.notify('There was an error in uploading image.', 'error');
             }
         });

    };

    $scope.deletePost = function() {

        ModalService.showModal({
            templateUrl: "/static/ui/custom-dialog.html?v=" + NationStory.appSettings.ver,
            controller: "DeleteConfirmController",
            inputs: {
                opinionId: $scope._id
            }
        }).then(function(modal) {
            modal.element.modal();
        });

    };

    //$interval($scope.saveDiff, 15000, 0);
})

.controller('DeleteConfirmController', function($scope, $http, $element, opinionId, $window, close) {
    $scope.title = 'Confirm';
    $scope.message = 'Do you want to delete this post? This action can not be undone.';
    $scope.confirmBtnText = 'Confirm'

    $scope.confirm = function() {
        $http.delete('/api/userstories/' + opinionId)
            .success(function(data) {
                $window.location = '/write';
            }.bind(this))
            .error(function(data, status, headers, config) {
                if (status == 401) {
                    NS.notify("You need to log in to do this action.", "error");
                    return;
                }
                if (data.message) {
                    NS.notify(data.message, "error");
                } else {
                    NS.notify("Server encountered an error.", "error");
                }

        });

        $element.modal('hide');
        close(null, 200);
        $('.modal-backdrop').remove();
    };
});
