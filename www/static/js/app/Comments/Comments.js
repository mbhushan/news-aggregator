'use strict';

angular.module('Comments', [])

.factory('Comments', function($http, $rootScope) {
    var Comments = function() {
        this.items = [];
        this.busy = false;
        this.after = '';
        this.url = "/api/comments";

        this.type = null;
        this.id = null;
        this.fetchError = false;
    };

    Comments.prototype.nextPage = function() {
        if (this.busy || this.after == -1) return;
        this.busy = true;
        var args;
        if (this.after) {
            args = {
                t: this.after
            };
        } else {
            args = {type: this.type, id: this.id};
        }

        $http.get(this.url, {
                params: args
            }).success(function(data) {
                for (var i = 0; i < data.comments.length; i++) {
                    this.items.push(data.comments[i]);
                }

                if (!data.t) {
                    this.after = -1;
                } else {
                    this.after = data.t;
                }
                this.busy = false;
            }.bind(this)).
            error(function(data, status, headers, config) {
                this.busy = false;
                this.fetchError = true;
            }.bind(this));
    };

    Comments.prototype.post = function(text) {
        $http.post('/api/comments', {text: text, id: this.id, type: this.type})
            .success(function(data) {
                this.items.unshift(data.comment);
                $rootScope.$emit('comments:added', data.comment);
            }.bind(this))
            .error(function(data, status, headers, config) {
                if (status == 401) {
                    $rootScope.$emit('comments:posterror', "You need to log in post comment.", "unauthenticated");
                    return;
                }
                var message="Some unknown error happened";
                if (data.message) {
                    message = data.message;
                }
                $rootScope.$emit('comments:posterror', message);
            });
    };
    return Comments;
});