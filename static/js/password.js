$(function() {
    $('#password_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="password"]').val() == ""){
    alert("you must provide a password");
  }
 else{
      $.post( $SCRIPT_ROOT + '/login_check',{
        password: $('input[name="password"]').val()
      }, function(data) {
          if (data == "fail"){alert("invalid  password")}
          else{
            $("#password_form").submit();
          }
      });}
    });
  });