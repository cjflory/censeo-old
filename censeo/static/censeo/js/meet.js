(function () {

  'use strict';

  var censeo = window.censeo || (window.censeo = {}),
    spinner = new Spinner({
      lines: 9, // The number of lines to draw
      length: 6, // The length of each line
      width: 3, // The line thickness
      radius: 5, // The radius of the inner circle
      top: 0 // Top position relative to parent in px
    });

  _.each(_.keys(censeo.ticketMaskDefinitions), function (key) {
    $.mask.definitions[key] = censeo.ticketMaskDefinitions[key];
  });

  $(function () {

    var // meetingId = $('#meetingId').data('meeting-id'),
      $addTicketForm = $('#addTicket'),
      $addTicketInput = $addTicketForm.find('#addTicketInput'),
      $tickets = $('#tickets'),
      $voting = $('#voting'),
      $users = $('#users'),
      currentTicketId, // Gets set when a ticket is selected
      votePollUrl, // Gets set when a ticket is selected
      ticketPollUrl = $tickets.data('poll-url'),
      userPollUrl = $users.data('poll-url'),
      pollInterval = 1000,
      votePoller, ticketPoller, userPoller,
      startVotePolling = function () {
        var pollFunction = function () {
          $.get(votePollUrl, function (votes) {
            spinner.stop();
            $voting.html(votes);
          });
        };

        // Call the poll function initially, then start polling
        pollFunction();
        // Prevent multiple pollers to get started
        clearInterval(votePoller);
        votePoller = setInterval(pollFunction, pollInterval);
      },
      startTicketPolling = function () {
        // Prevent multiple pollers to get started
        clearInterval(ticketPoller);
        ticketPoller = setInterval(function () {
          $.get(ticketPollUrl, function (tickets) {
            $tickets.html(tickets);
          });
        }, pollInterval);
      },
      startUserPolling = function () {
        // Prevent multiple pollers to get started
        clearInterval(userPoller);
        userPoller = setInterval(function () {
          $.get(userPollUrl, function (users) {
            $users.html(users);
          });
        }, pollInterval);
      };

    // Restrict input to expected format
    $addTicketInput.mask(censeo.ticketMask);

    // Click handler for ticket links
    $tickets.on('click', '.ticket a', function (e) {
      e.preventDefault();
      clearInterval(ticketPoller);
      clearInterval(votePoller);

      var $this = $(this),
        cancelling = $this.hasClass('btn-primary'),
        $allTicketLinks = $tickets.find('.ticket a'),
        ticketId = $this.data('ticket-id');

      $allTicketLinks.removeClass('btn-primary').addClass('btn-default');

      if (cancelling) {
        startTicketPolling();
        $voting.html(censeo.defaultVotingHtml);
        currentTicketId = votePollUrl = undefined;
      } else {
        $this.toggleClass('btn-primary btn-default');

        $voting.children().hide();
        spinner.spin($voting.get(0));

        currentTicketId = ticketId;
        votePollUrl = $this.attr('href');
        startVotePolling();
      }
    });

    // Click handler for #addTicket form
    $addTicketForm.on('submit', function (e) {
      e.preventDefault();

      $.post($addTicketForm.attr('action'), $addTicketForm.serialize(), function (result) {
        $('.errors').remove();

        if (result.errors) {
          // Sample result:  {"errors": {"id": ["Invalid ticket id"]}}
          var addError = function (text) {
            $addTicketForm.append( $('<div>', {'class': 'errors', text: text}) );
          };

          _.each(_.keys(result.errors), function (key) {
            _.each(result.errors[key], addError);
          });
        } else {
          $tickets.find('.ticket-list').append(result);
          $addTicketInput.val('').focus();
        }
      });
    });

    // Click handler for voting on a ticket
    $voting.on('click', '.vote-option a', function (e) {
      e.preventDefault();

      var $this = $(this);

      $voting.children().hide();
      spinner.spin($voting.get(0));

      $.get($this.attr('href'), function (result) {
        spinner.stop();
        $voting.html(result);
      });
    });

    // Click handler for admin to reset votes after completion
    $voting.on('click', 'a.reset-votes', function (event) {
      event.preventDefault();

      $.post($(this).attr('href'));
    });

    // Click handler for voter to become an observer
    $users.on('click', 'a.become-observer', function (event) {
      event.preventDefault();

      $.post($(this).attr('href'));
    });

    startTicketPolling();
    startUserPolling();

  });

}());
