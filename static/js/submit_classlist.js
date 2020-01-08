$(function() {
      $('#btnsubmiting').bind('click', function() {
    // Stop form from submitting normally
    event.preventDefault();
    $('#classlist').submit()
    $('#cancel').attr('disabled', true)
    $('#btnsubmiting').attr('disabled', true)
    $('#btnsubmiting').text('please wait....')
        });
  });