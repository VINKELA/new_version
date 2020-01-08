
$(function() {
  $('#customize_submit').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
if ($('#general_password').val().length > 0){
if($('#general_password').val().length < 8)
{
  $('#general_password').focus()
  $('#password_msg').text("password must be 8 or more letters long")
}
}
else{
$('#customize_submit').attr('disabled', true)
$('#cancel').attr('disabled', true)
$('#customize_form').submit()
$('#customize_submit').text('please wait')
}
  });
});