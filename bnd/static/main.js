$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });
});

$(function() {
  // Event handlers for checkpoint blocks
  $('a.checkpoint-view').bind('click', function(evt) {
    console.log($(evt.target).data('checkpoint-id'));
  });
});
