$('.form').find('input, textarea').on('keyup blur focus', function (e) {

  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight');
			} else {
		    label.removeClass('highlight');
			}
    } else if (e.type === 'focus') {

      if( $this.val() === '' ) {
    		label.removeClass('highlight');
			}
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a,.links a').on('click', function (e) {

  e.preventDefault();

  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');

  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();

  $(target).fadeIn(600);

});

addEventListener("load", function() {
  setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); }

addEventListener("load", function()
{ setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); }

var myInput2 = document.getElementById("psw");
var length2 = document.getElementById("length2");



// When the user clicks on the password field, show the message box
myInput2.onfocus = function() {
  document.getElementById("message2").style.display = "block";
};

// When the user clicks outside of the password field, hide the message box
myInput2.onblur = function() {
  document.getElementById("message2").style.display = "none";
};


// When the user starts to type something inside the password field
myInput2.onkeyup = function() {

  // Validate length
  if(myInput2.value.length >= 8) {
    length2.classList.remove("invalid");
    length2.classList.add("valid");
  } else {
    length2.classList.remove("valid");
    length2.classList.add("invalid");
  }
};


  function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}


$(function() {
    $('#submit_registration').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="school_name"]').val() ==""){
    $('.red').text('')
    $('#schoolname_message').text("school name is empty");
    $('input[name="school_name"]').focus();

  }
  else if($('input[name="email"]').val() ==""){
    $('.red').text('')
    $('#email_message').text("email is empty");
    $('input[name="email"]').focus()
  }
  else if(validateEmail($('input[name="email"]').val()) !=true){
    $('.red').text('')
    $('#email_message').text("email is not valid");
    $('input[name="email"]').focus()
  }
  else if($('#term').find(":selected").val() ==""){
    $('.red').text('')
    $('#term_message').text("current term is empty!");
    $('#term').focus()
  }
  else if($('#school_session').find(":selected").val() ==""){
    $('.red').text('')
    $('#session_message').text("current session is empty!");
    $('#school_session').focus()
  }

  else if($('#user').val() == ""){
    $('.red').text('')
    $('#username_message').text("username is empty");
    $('input[name="username"]').focus()

  }
   else if($('#psw').val() ==""){
    $('.red').text('')
    $('#password_message').text("password is empty!")
    $('#psw').focus()
  }
  // Validate length
  else if(myInput2.value.length < 8) {
    $('.red').text('')
    $('#password_message').text("password must be up to 8 digits")
    $('#psw').focus()

  }
   else if($('input[name="confirmation"]').val() ==""){
    $('.red').text('')
    $('#confirmation_message').text("re-enter password")
    $('input[name="confirmation"]').focus()

  }
   else if($('#psw').val() != $('input[name="confirmation"]').val()){
     $('.red').text('')
    $('#confirmation_message').text("password and confirmation do not match")
    $('input[name="confirmation"]').focus()

  }
 else{
      $.post( $SCRIPT_ROOT + '/username_check',{
        username: $('#user').val()
      }, function(data) {
          if (data == "false")
          { 
            $('.red').text('')   
            $('#username_message').text("username already taken")
                $('#user').focus()
        }
          else{ $.post( $SCRIPT_ROOT + '/email_check',{
        email: $('input[name="email"]').val()
      }, function(data) {
          if (data == "false")
          { 
            $('.red').text('')   
            $('#email_message').text("email already exist")
            $('input[name="email"]').focus()
        }
          else{
            $('.red').text('')
            $('#submit_registration').attr('disabled', true)
            $('#cancel').attr('disabled', true)
            $('#submit_registration').text('creating account .....')
            $("#register").submit();
};
      });};
      });
 }
    });
  });



