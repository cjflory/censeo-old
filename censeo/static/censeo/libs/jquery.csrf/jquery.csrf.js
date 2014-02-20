(function () {

  'use strict';

  $.extend({

    csrf: function (csrfToken) {

      var csrfSafeMethod = function (method) {
          // these HTTP methods do not require CSRF protection
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        sameOrigin = function (url) {
          // test that a given url is a same-origin URL
          // url could be relative or scheme relative or absolute
          var host = document.location.host, // host + port
            protocol = document.location.protocol,
            srOrigin = '//' + host,
            origin = protocol + srOrigin;

          // Allow absolute or scheme relative URLs to same origin
          return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === srOrigin || url.slice(0, srOrigin.length + 1) === srOrigin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
        };

      $.ajaxSetup({
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
          }
        }
      });

    }

  });

}());
