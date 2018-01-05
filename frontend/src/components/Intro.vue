<template>
  <div id="main_wrap">
    <div class="login_wrap">
      <div class="login_logo"><a href=""><img src="../assets/images/common/login_logo.jpg" alt="" /></a></div>
      <div class="login_f_btn"><a href="javascript:" @click="login"><img src="../assets/images/common/login_f_btn.jpg" alt="" /></a></div>
      <div class="login_prologue"><a href="#/pick">Click here to <strong>pickdata brand site</strong></a></div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import { setUserId } from '../utils/auth'

export default {
  name: 'Intro',
  methods: {
    login () {
      fblogin()
    }
  }
}


function fblogin() {
  window.fbAsyncInit = function() {
    FB.init({
      // appId      : '{{ fb_app_id }}',
      appId      : '1456607077970548',
      cookie     : true,  // enable cookies to allow the server to access
      // the session
      xfbml      : true,  // parse social plugins on this page
      // version    : '{{ fb_app_version }}' // use version 2.2
      version    : 'v2.11' // use version 2.2
    });

    FB.getLoginStatus(function(response) {
      fbCheckStatus(response);
    });
  };

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  FB.login(function(response) {
    if (response.status === "connected") {
      snackLogin(response);
    } else {
      console.log("FB.login Fail!!");
    }
  }, {scope: 'email,ads_management,pages_show_list,manage_pages'});
}

function fbCheckStatus() {
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      // testAPI();
      var login_session = '{{ login_session }}';
      if (login_session = 'None') {
        // PASS
      } else {
        snackLogin(response);
      }
    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
    }
    console.log(response);
  });
}

function snackLogin(res) {
  FB.api('/me?fields=id,name,email,birthday,gender,picture', function(resp) {
    // console.log(res.authResponse.accessToken);
    console.log(res);
    // location.href = "main";

    // axios.post('/users/signin', {
    axios.post('users/signin', {
        fb_username: resp.email,
        fb_id: resp.id,
        fb_name: resp.name,
        fb_gender: resp.gender,
        fb_picture_url: resp.picture.data.url,
        fb_access_token: res.authResponse.accessToken
    })
    .then((response) => {
      var success = response.data.success;
      if (success == "YES") {
        setUserId(resp.id)
        location.href = "#/pick";
      } else {
        alert(response.msg);
      }

    })
    .catch(err => {
      alert("ERROR!!");
      console.log('Error: ', err)
    })
  });
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
