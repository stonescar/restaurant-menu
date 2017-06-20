$(document).ready(function() {
    $('.flash-message').click(function() {
        $(this).animate({height: 'toggle', opacity: 'toggle'}, "slow");
    });
});