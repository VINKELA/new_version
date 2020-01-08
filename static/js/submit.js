$(function() {
    $('#submit_scoresheet').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="subject_name"]').val() == ""){
    $('.red').text("")
    $('#subject_message').text("subject name is empty!");
    $('input[name="subject_name"]').focus()

  }

  else if($('#your_class').find(":selected").val() ==""){
    $('.red').text("")
    $('#class_message').text("Scoresheet is for which class? select");
    $('#your_class').focus()

  }

   else if($('input[name="subject_teacher"]').val() ==""){

    $('.red').text("")
    $('#teacher_message').text("please provide the subject teachers name");
    $('input[name="subject_teacher"]').focus()
  }
  else{
      $.post( $SCRIPT_ROOT + '/subject_check',{
        subject_name: $('input[name="subject_name"]').val(),class_id:$('#your_class').find(":selected").val()
      }, function(data) {
          if (data == "false")
          {
            $('.red').text("")
            $('#subject_message').text($('input[name="subject_name"]').val()+" scoresheet already submitted for selected class")
          }
          else{
            $('.red').text("")
            $('#submit_scoresheet').attr('disabled', true)
            $('#cancel').attr('disabled',true)
            
            $('#submit_scoresheet').text('please wait...')
            $("#submit_score").submit();
              };
      });};
      });
});