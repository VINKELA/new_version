$(function() {
    $('#verify_teacher').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('#password').val() == ""){
    $('#teacher_msg').text("provide password");
    $('#password').focus()
  }

 else{
      $.post( $SCRIPT_ROOT + '/editclass_check',{
        class_id: $('#id').val(),
        password: $('#password').val()
      }, function(data) {
          if (data == "false"){
            $('#teacher_msg').text("incorrect password");
            $('#password').focus()
          }
          else{
            $('.red').text(" ")
            $("#verify_teacher_form").submit();
          }
      });}
    });
  });


  $(function() {
    $('#edit_student_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('#firstname').val() == ""){
    $('.red').text(" ")
    $('#firstname_msg').text('firstname is empty!')
    $('#firstname').focus()
  }
  else if($('#surname').val() == ""){   
    $('.red').text(" ")
     $('#surname_msg').text('surname is empty!')
     $('#surname').focus()
  }
 else{
  $('.red').text(" ")
  $('#unregister_button').attr('disabled', true)
  $('#cancel').attr('disabled', true)
   $('#edit_student_button').attr('disabled', true)
    $("#edit_student_button").text('please wait');
    
    $("#edit_student_form").submit();
      }
    });
  });


  $(function() {
    $('#add_student_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('#password').val() == ""){
    $('.red').text('')
    $("#msg_pass").text("password is empty");
    $('#add_student_button').focus()
  }

 else{
      $.post( $SCRIPT_ROOT + '/editclass_check',{
        class_id: $('#class_id').val(),
        password: $('#password').val()
      }, function(data) {
          if (data == "false"){
            $('.red').text('')
            $("#msg_pass").text("invalid password")
            $('#add_student_button').focus()

          }
          else{
            $('.red').text('')
            $('#add_student_button').attr('disabled',true)
            $('#add_student_button').attr('please wait')
            $("#add_student_form").submit();
          }
      });}
    });
  });

  $(function() {
    $('#add_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('#firstname').val() == ""){
    $('.red').text('')
    $('#f_msg').text("firstname is empty");
    $('#firstname').focus()
  }
  else if($('#surname').val() == ""){
    $('.red').text('')
    $('#s_msg').text("surname is empty");
    $('#surname').focus()
  }

 else{
    $('.red').text('')
    $("#add_button").attr("disabled", true)
    $("#add_button").text("please wait")
    $("#add_student_form").submit();
      }
    });
  });

  $(function() {
    $('#password_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="password"]').val() == ""){
    $('.red').text('')
    $('#admin_msg').text("please enter admin password");
    $('input[name="password"]').focus()
  }

  else{
    $.post( $SCRIPT_ROOT + '/admin_check',{
      password: $('input[name="password"]').val()
    }, function(data) {
        if (data != 'correct'){ 
          $('.red').text('')
          $('#admin_msg').text("incorrect password");
          $('input[name="password"]').focus()
              }
        else{
          $('.red').text('')
          $("#cancel").attr('disabled',true)
          $("#password_form").submit();
        };
    });}
  });
});


$(function() {
  $('#admin_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
if($('input[name="password"]').val() == ""){
  $('.red').text("")
  $('#msg_pass').text("password is empty");
  $('input[name="password"]').focus()
}
  else{
    $.post( $SCRIPT_ROOT + '/admin_check',{
      password: $('input[name="password"]').val()
    }, function(data) {

        if (data == "incorrect password"){
          
            $('.red').text("")
            $('#msg_pass').text("incorrect passwords");
            $('input[name="password"]').focus()
        }
        else{
          $('.red').text(" ")
          $('#admin_button').attr('disabled', true)
          $('#cancel').attr("disabled", true)
          $('#admin_form').submit()
       }
    });}

    
  });
});


$(function() {
  $('#unregister_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
  $('#unregister_button').attr('disabled', true);
  $('#edit_student_button').attr('disabled', true);
  $('#cancel').attr("disabled", true)
  var con = confirm("You are about to permanently unregister "+$('#firstname').val()+" "+$("#surname").val()+" permanently from this term")
  if( con == true){
    $('#unregister_button').text("please wait");
    $('#unregister_form').submit()      
  }
  else{
    $('#unregister_button').attr('disabled', false);
    $('#edit_student_button').attr('disabled', false);
    $('#cancel').attr("disabled", false)
  }
  });
});

$(function() {
  $('#confirm_student_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
  $('#confirm_student_button').attr('disabled', true);
  $('#cancel').attr("disabled", true)
  $('#confirm_student_button').text("please wait");
  $('#confirm_student_form').submit()    
  });
});

$(function() {
  $('#teacher_customize_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
if($('#password').val() == ""){
  $('.red').text("")
  $('#teacher_customize_button').focus();
  $('#teach_msg').text("password is empty");
}

else{
    $.post( $SCRIPT_ROOT + '/editclass_check',{
      class_id: $('#class_id').val(),
      password: $('#password').val()
    }, function(data) {
        if (data == "false"){
          $(".red").text("")
          $('#teach_msg').text("incorrect password");
        }
        else{
          $('.red').text("")
          $("#teacher_customize_form").submit();
        }
    });}
  });
});

$(function() {
  $('#class_customize_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
  sum_score = 0;
  if( $("#ca").val() != ""){
    ca = parseInt($("#ca").val())
    sum_score = sum_score +  ca
  }
  if( $("#test").val() != ""){
    test = parseInt($("#test").val())
    sum_score = sum_score +  test
  }
  if( $("#exam").val() != ""){
    exam = parseInt($("#exam").val())
    sum_score = sum_score +  exam
  }
  if(sum_score != 100){
    $(".red").text("")
    $("#ca_message").text("ca +")
    $("#test_message").text("test +")
    $("#exam_message").text("exam  must be equal to 100")
    $("#ca").focus()
  } 
  else{
    $('#class_customize_button').attr('disabled', true);
    $('#cancel').attr('disabled', true);
    $('#class_customize_button').text("please wait");
    $('#class_customize_form').submit()    
  }


  });
});

$(function() {
  $('#edit_scoresheet_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
if($('#password').val() == ""){
  $('.red').text("")
  $('#password').focus()
  $('#teacher_msg').text("provide password");
}

else{
    $.post( $SCRIPT_ROOT + '/editclass_check',{
      class_id: $('#id').val(),
      password: $('#password').val()
    }, function(data) {
        if (data == "false"){
          $('.red').text("")
          $('#teacher_msg').text("incorrect password");
        }
        else{
          $('.red').text("")
          $("#edit_scoresheet_form").submit();
        }
    });}
  });
});


$(function() {
  $('#edited_scoresheet_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
if($('#subject_name').val() == ""){
  $('.red').text('')
  $('#subject_msg').text("subject does not have a name");
  $('#subject_name').focus()
}
else if($('#teachers_name').val() == ""){
  $('.red').text('')
  $('#teachers_msg').text("Teachers name is empty")
  $('#teachers_name').focus();
}
else if ($("#previous_name").val() == $("#subject_name").val()){
  $('.red').text('')
  $('#edited_scoresheet_button').attr('disabled',true)
  $('#cancel').attr('disabled', true)
  $('#delete_scoresheet_button').attr('disabled', true)
  $('#edited_scoresheet_button').text('please wait')
  $("#edited_scoresheet_form").submit();
}

else{
  $.post( $SCRIPT_ROOT + '/subject_name_check',{
    subject_name: $('input[name="subject_name"]').val(),class_id:$('#class_id').val(), previous:$("#previous").val()
  }, function(data) {
      if (data == "false")
      {
        $('#subject_msg').text($('input[name="subject_name"]').val()+" scoresheet already submitted for selected class")
        $('#subject_name').focus()
      }
      else{
        $('.red').text('')
        $('#edited_scoresheet_button').attr('disabled',true)
        $('#cancel').attr('disabled', true)
        $('#delete_scoresheet_button').attr('disabled', true)
        $('#edited_scoresheet_button').text('please wait')
        $("#edited_scoresheet_form").submit();
                      };
  });};
  });
});

$(function() {
  $('#delete_scoresheet_button').bind('click', function() {
// Stop form from submitting normally
event.preventDefault();
conf= confirm("press ok to delete "+$('#previous').val()+" permanentely")
if (conf == true){
    $('#edited_scoresheet_button').attr('disabled',true)
    $('#cancel').attr('disabled', true)
    $('#delete_scoresheet_button').attr('disabled', true)
    $('#delete_scoresheet_button').text("please wait");
    $('#delete_scoresheet_form').submit() 
  }
else{
  $('#edited_scoresheet_button').attr('disabled',false)
  $('#cancel').attr('disabled', false)
  $('#delete_scoresheet_button').attr('disabled', false)

}   
  });
});
