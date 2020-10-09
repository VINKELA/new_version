// A get post method
// function api(apiConnectType, url, data, asyncMode, callback=null, failureCallback = null) {
//     $.ajax({
//             type: apiConnectType,
//             url: SCRIPT_ROOT + url,
//             async: asyncMode,
//             data: data,
//             dataType: "json",
//             timeout: 60000,
//             // headers: {
//             //     "user-auth": $("#auth").val()
//             // }
//     })
//         .success(function (remoteData) {
//             // if (remoteData.message === true) {
//             //     if (callback !== null && typeof callback === "function") {
//                     // if (feedBack) {
//                     //     alert(remoteData.Message);
//                     //     setTimeout(function() {
//                     //             callback(remoteData.Data);
//                     //         },
//                     //         2000);
//                     // } else
//                         callback(remoteData.Data);
//                 // } 
//                 // else {
//                 //     if (feedBack) {
//                 //         alert(remoteData.Message);
//                 //     }
//                 // }
//             // } else {
//             //     if (callbackOnFailure && callback !== null && typeof callback === "function") callback(remoteData.Data);
//             //     alert(remoteData.Message);
//             // }
//         })
//         .error(function (e) {
//             // if (e.statusText === 'error' && e.responseText === '' && e.readyState === 0) { // means we had no response and the request was unsent i.e. unable to get to the server -> highly probable that it's no connectivity between client and server
//             //     alert("Something seems to be wrong with your network. Please check your Internet connection");
//             //     return;
//             // }
//             // else if (e.statusText === 'timeout' && e.readyState === 0) { // we've waited for too long oo
//             //     //swalInfo('Could not get a response from the server. Reloading now');
//             //     this.abort();
//             //     location.reload();
//             //     return;
//             // }
//             failureCallback(e.statusText);
//         });
// };

function api(apiConnectType, url, payload, successCallback,errorCallback, ){
        $.ajax({
            type: apiConnectType,
            url:  $SCRIPT_ROOT + url,
            async: false,
            data: payload,
            dataType: "json",
            timeout: 60000,
    })
    .success(function(remoteData){
        if(remoteData.message === 'success'){
            successCallback(remoteData)
        }
        else{
            errorCallback(remoteData)
        }
    })
    .error(function(e){
            if (e.statusText === 'error' && e.responseText === '' && e.readyState === 0) { // means we had no response and the request was unsent i.e. unable to get to the server -> highly probable that it's no connectivity between client and server
                alert("Something seems to be wrong with your network. Please check your Internet connection");
                return;
            }
            else if (e.statusText === 'timeout' && e.readyState === 0) { // we've waited for too long oo
                //swalInfo('Could not get a response from the server. Reloading now');
                this.abort();
                location.reload();
                return;
            }
            console.log(e.responseText);
    })

   }


// $(function() {
//     $('#submit_scoresheet').bind('click', function() {
//   // Stop form from submitting normally
//   event.preventDefault();
//   if($('input[name="subject_name"]').val() == ""){
//     $('.red').text("")
//     $('#subject_message').text("subject name is empty!");
//     $('input[name="subject_name"]').focus()

//   }

//   else if($('#your_class').find(":selected").val() ==""){
//     $('.red').text("")
//     $('#class_message').text("Scoresheet is for which class? select");
//     $('#your_class').focus()

//   }

//    else if($('input[name="subject_teacher"]').val() ==""){

//     $('.red').text("")
//     $('#teacher_message').text("please provide the subject teachers name");
//     $('input[name="subject_teacher"]').focus()
//   }
//   else{
//       $.post( $SCRIPT_ROOT + '/subject_check',{
//         subject_name: $('input[name="subject_name"]').val(),class_id:$('#your_class').find(":selected").val()
//       }, function(data) {
//           if (data == "false")
//           {
//             $('.red').text("")
//             $('#subject_message').text($('input[name="subject_name"]').val()+" scoresheet already submitted for selected class")
//           }
//           else{
//             $('.red').text("")
//             $('#submit_scoresheet').attr('disabled', true)
//             $('#cancel').attr('disabled',true)
            
//             $('#submit_scoresheet').text('please wait...')
//             $("#submit_score").submit();
//               };
//       });};
//       });
// });

function base64u(base64) {
    return base64.replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
}
