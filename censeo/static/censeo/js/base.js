(function () {

  'use strict';

  $(function () {

    var censeo = window.censeo || (window.censeo = {}),
      $usernameField = $('#id_username');

    // Setup jquery.csrf for AJAX requests
    $.csrf($.cookie('csrftoken'));

    // If there's a username field on the page, focus on it initially
    if ($usernameField.length) {
      $usernameField.focus();
    }

  });

}());
