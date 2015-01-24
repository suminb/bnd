$(document).ready(function () {
    $('[data-toggle="offcanvas"]').click(function () {
        $('.row-offcanvas').toggleClass('active')
    });
});

$(function() {
    // Event handlers for checkpoint blocks
    $('a.checkpoint-view').bind('click', function(evt) {
        var teamID = $(evt.currentTarget).data('team-id');
        var checkpointID = $(evt.currentTarget).data('checkpoint-id');

        showGoalsForCheckpoint(teamID, checkpointID);
    });
});

function showGoalsForCheckpoint(teamID, checkpointID) {
    $.get(sprintf('/goal/view_all/ajax?team_id=%d', teamID), function(response) {
        $('#rendered-results').html(response);
    });
}