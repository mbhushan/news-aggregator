function fbSingin() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            $.ajax({
              url: "/register/facebook",
              type: 'POST',
              data : {token: response.authResponse.accessToken},
              dataType: "json",
              success: function(data) {
                  window.location.href = '/';
              },
              error: function() {
                  $('#modal').modal();
              }
            });

        } else if (response.status === 'not_authorized') {
            $('#modal').modal();
        } else {
            $('#modal').modal();
        }
    }, {scope: 'public_profile,email'});
}


window.fbAsyncInit = function() {
  FB.init({
    appId      : NationStory.appSettings.facebook,
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.1' // use version 2.1
  });
};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function googleSingin() {
    var additionalParams = {
        'callback': signinCallback,
        'clientid': NationStory.appSettings.google
    };
    gapi.auth.signIn(additionalParams);
}

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
                window.location.href = '/';
            },
            error: function() {
                $('#modal').modal();
            }
        });
        } else {}
}
