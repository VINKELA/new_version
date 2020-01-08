$(function() {
    $('#edit_class_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="surname"]').val() == ""){
    $('.red').text('')
    $("#surname_msg").text("form teachers surname?");
    $('input[name="surname"]').focus()

  }
  else if($('input[name="firstname"]').val() == ""){
    $('.red').text('')
    $("#firstname_msg").text("form teachers firstname?");
    $('input[name="firstname"]').focus()
  }
  else if($('input[name="class_name"]').val() == ""){
    $('.red').text('')
    $("#class_msg").text("class does not have a name?");
    $('input[name="class_name"]').focus()
  }
  else if($('input[name="password"]').val() == ""){
    $('.red').text('')
    $("#pass_msg").text("password is empty");
    $('input[name="password"]').focus()
  }    
  else if($('#section').val() == ""){
    $('.red').text('')
    $('#section').focus()
    $("#section_msg").text("password is empty");
  }
  else{
  $.post( $SCRIPT_ROOT + '/class_name',{
    classname: $('input[name="class_name"]').val(),
    oldname: $('input[name="old_name"]').val(),

  }, function(data) {
      if (data.value == "fail"){
        $('.red').text('')
        $("#class_msg").text("class with name "+$('input[name="class_name"]').val()+" already exist");
        $('input[name="class_name"]').focus()
          }
      else{
        $('.red').text('')
        $("#edit_class_button").attr("disabled", true);
        $("#edit_class_button").text("please wait");
        $("#edit_class_form").submit();
  }
  });}

    });
  });

  $(function() {
    $('#delete').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  $("#delete").attr("disabled", true);
  var con = confirm("Are you sure you want to delete "+$('input[name="class_name"]').val().toUpperCase())
  if (con == true){
    $("#delete").text("please wait");
    $("#delete_form").submit();  
  }
  else{
    $("#delete").attr("disabled", false);

  }
    });
  });