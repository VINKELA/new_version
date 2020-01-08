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

$(function() {
    $('#login').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('#username').val() == ""){
    $('.red').text('')
    $('#signin_message').text("username is empty")
    $('input[name="username"]').focus()
  }

 else if($('#password').val() ==""){
  $('.red').text('')
  $('#password_message').text("password is empty")
  $('input[name="password"]').focus()
}
 else{
      $.post( $SCRIPT_ROOT + '/login_check',{
        username: $('input[name="username"]').val(),
        password: $('input[name="password"]').val()
      }, function(data) {
          if (data == "fail"){
            $('.red').text('')
            $('#signin_message').text("username or password is incorrect")
            $('input[name="username"]').focus()
        }
          else{
            $('.red').text('')
            $('#login').attr('disabled',true)        
            $('#login').text("loging in ....")
            $("#login_form").submit();

          }
      });}
    });
  });

  $(function() {
    $('#check_result').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  var str = $('input[name="regnumber"]').val();
  if($('input[name="regnumber"]').val() == ""){
    $('.red').text('')
    $('#reg_message').text("exam number is empty");
    $('input[name="regnumber"]').focus()
  }
  else if(str.length < 7){
    $('.red').text('')
    $('#reg_message').text("exam number invalid");
    $('input[name="regnumber"]').focus()
  }
  else if($('input[name="pin"]').val() ==""){
    $('.red').text('')
    $('#pin_message').text("pin is empty");
    $('input[name="pin"]').focus()
  }
  else{
      $.post( $SCRIPT_ROOT + '/result_check',{
        regnumber: $('input[name="regnumber"]').val(),
        pin: $('input[name="pin"]').val()
      }, function(data) {
          if (data.value =="fail"){
            $('.red').text('')
            $('#reg_message').text("exam number invalid");
            $('input[name="regnumber"]').focus() 
          }
          else if (data.value =="pin invalid"){
            $('.red').text('')
            $('#pin_message').text("pin is invalid");
            $('input[name="pin"]').focus()
          }
          else if (data.value=="pass"){
            $('.red').text('') 
            $('#check_result').text('checking ....')  
            $('#cancel').attr('disabled',true)
            $("#check_results").submit();
            $('#check_result').text('check result')
          }
      });}
    }
    );
  });
  
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






$(function() {
    $('#but').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();

 if($('input[name="password"]').val() ==""){
    $('.red').text('')
    $("#pass_msg").text("password is empty");
  }
   else if($('input[name="confirmation"]').val() ==""){
    $('.red').text('')
    $("#conf_msg").text("password confirmation is empty");
  }
   else if($('input[name="password"]').val() != $('input[name="confirmation"]').val()){
    $('.red').text('')
    $("#conf_msg").text("password and confirmation do not match");
  }
// Validate length
  else if($('input[name="password"]').val().length < 8) {
    $('.red').text('')
    $("#pass_msg").text(" password must be up to 8 digits");
  }
  else{
    $('.red').text('')
    $('#but').attr('disabled',true)
    $("#change_form").submit();
  }
});
});


