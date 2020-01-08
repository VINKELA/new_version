
$(function() {
    $('#create_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();

 if($('input[name="class_name"]').val() ==""){
   $('.red').text('')
    $('#message_class').text("please enter the class name");
    $('input[name="class_name"]').focus()
  }
   else if($('#section').find(":selected").val() ==""){
    $('.red').text('')
    $('#section_message').text("please select a section ");
    $('#section').focus()
  }

  else if($('input[name="ca"]').val() ==""){
    $('.red').text('')
    $('input[name="ca"]').focus()
   $('#ca_message').text("ca score is empty");
  }
    else if (isNaN($('input[name="ca"]'))== false){
      $('.red').text('')
      $('input[name="ca"]').focus()
      $('#ca_message').text("ca score should be a valid number");
     }
       else if($('input[name="test"]').val() ==""){
        $('.red').text('')
        $('input[name="test"]').focus()
        $('#test_message').text("test score is empty");
       }
      else if (isNaN($('input[name="test"]'))==false){
        $('.red').text('')
        $('input[name="test"]').focus()
        $('#test_message').text("test score should be a valid number");
       }
  else if($('input[name="exam"]').val() ==""){
    $('.red').text('')
    $('input[name="exam"]').focus()
   $('#exam_message').text("exam score is empty");
  }
    else if (isNaN($('input[name="exam"]'))==false){
      $('.red').text('')
      $('input[name="exam"]').focus()
      $('#exam_message').text("exam score should be a valid number");
     }
  else if((parseInt($('input[name="exam"]').val(), 10)+parseInt($('input[name="ca"]').val(), 10) + parseInt($('input[name="test"]').val(), 10)) != 100 ){
    $('.red').text('')
    $('input[name="exam"]').focus()
   $('#exam_message').text("ca + test + exam should add to 100");
  }
   else if($('input[name="no_of_students"]').val() ==""){
    $('.red').text('')
    $('input[name="no_of_students"]').focus()
   $('#students_message').text("how many students are in the class");
  }

  else if (isNaN($('input[name="no_of_students"]')) == false){
    $('.red').text('')
    $('#students_message').text($('input[name="no_of_students"]').val()+" is not a valid number");
    $('input[name="no_of_students"]').focus()
  }
  
    else if($('input[name="firstname"]').val() ==""){
      $('.red').text('')
    $('input[name="firstname"]').focus()
    $('#firstname_message').text("class teachers firstname?");
  }
  else if($('input[name="surname"]').val() ==""){
    $('.red').text('')
    $('input[name="surname"]').focus()
   $('#surname_message').text("class teachers surname");
  }
     else if($('input[name="password"]').val() ==""){
      $('.red').text('')
      $('input[name="password"]').focus()
      $('#pass_message').text("password is empty");
     }
    else if($('input[name="password"]').val().length < 6){
      $('.red').text('')
      $('input[name="password"]').focus()
      $('#pass_message').text("password should be at least 6 digit long");
     }

     else if($('input[name="confirmation"]').val() ==""){
      $('.red').text('')
      $('input[name="confirmation"]').focus()
      $('#confirm_message').text("re-enter password");
     }

   else if($('input[name="password"]').val() != $('input[name="confirmation"]').val()){
    $('.red').text('')
    $('input[name="confirmation"]').focus()
   $('#confirm_message').text("password and confirmation do not match");
  }
else{
  $.post( $SCRIPT_ROOT + '/class_name2',{
    classname: $('input[name="class_name"]').val(),
  }, function(data) {
      if (data == "fail"){
        $('#message_class').text("class already exist")
        $('input[name="class_name"]').focus()
      }
      else{
        $('.red').text('')
        $("#create_button").attr("disabled", true)
        $('#cancel').attr('disabled', true)
        $("#create_button").text("creating")
        $("#create_form").submit();
            }
  });}

});
});



$('.tab a,.links a').on('click', function (e) {

  e.preventDefault();

  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');

  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();

  $(target).fadeIn(600);

});