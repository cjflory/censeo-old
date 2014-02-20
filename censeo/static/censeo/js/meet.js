(function () {

  'use strict';

  $(function () {

    var meetingId = $('#meetingId').data('meeting-id'),
      $tickets = $('#tickets'),
      $voting = $('#voting'),
      $users = $('#users'),
      $addTicketForm = $('#addTicket');

    $addTicketForm.on('submit', function (e) {
      e.preventDefault();

      var $ticketList = $tickets.find('.ticket-list'),
        $addTicketInput = $('#addTicketInput');

      $.post($addTicketForm.attr('action'), $addTicketForm.serialize(), function (result) {
        $ticketList.find('> .error').remove();
        $ticketList.append(result);
        $addTicketInput.val('').focus();
      });
    });
  });

}());
