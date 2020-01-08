$(function() {
      $('#btnsubmit').bind('click', function() {
    // Stop form from submitting normally
    event.preventDefault();
    $('#cancel').attr('disabled', true)
    $('#btnsubmit').attr('disabled', true)
    $('#btnsubmit').text('please wait....')
    $("#submitted").submit();
        });
  });