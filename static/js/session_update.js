$(function() {
    $('#session_update_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
     all_classes = []
    no_of_classes = parseInt($("#class_length").val())
    for(i=1; i < no_of_classes+1; i++){
      old_selector = "old"+i
      new_selector = "new"+i
      message = "message"+i
      if ($('#'+new_selector).val() == ""){
        $('.red').text(" ")
        $('#'+message).text($("#"+old_selector).val().toUpperCase()+" does not have a new name for the new session")
        $("#"+new_selector).focus()
        break
      }
      else if($("#"+old_selector).val().toLowerCase() == $("#"+new_selector).val().toLowerCase()){
        $('.red').text('')
        $("#"+message).text($("#"+new_selector).val().toUpperCase() +" have the same name as Last session")
        $("#"+new_selector).focus()
        break
      }
      else{
        all_classes.push($("#"+new_selector).val())
        if(i == no_of_classes){
         uniq = new Set(all_classes)
  
            if (uniq.size != all_classes.length){
              $('.red').text('')
              $('.red').text('Two or more classes have the same name for the new session')
              break
            }
            else{
              $('.red').text('')
              $('#session_update_button').attr('disabled', true);
              $('#cancel').attr('disabled', true);
              $('#session_update_button').text("please wait");
              $('#session_update_form').submit()  
              break 
            }
  
        }
      }


    }
    });
  });
  