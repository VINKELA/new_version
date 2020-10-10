var logInText = 'Log In';
var signingInText = 'Signing In...';



function logIn() {

    $('#signInButton').attr('disabled', true);
    $('.info').text('')
    const username = $('#username').val();
    const password = $('#password').val();

    // if (!username || username.length === 0 || !password || password.length === 0) {
    //     swalWarning('Invalid log in credentials supplied. Please input valid credentials');
    //     return;
    // }

    if (username.length === 0 || !username)
    {
        $('#emailInfo').text("username cannot be empty")
        $('#signInButton').attr('disabled', false); 
        return
    }
    if (password.length === 0 || !password)
    {
        $('#passwordInfo').text("password cannot be empty")
        $('#signInButton').attr('disabled', false);
        return
    }

    const data = {
        username: username,
        password: password
    };

    const base64 = CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(JSON.stringify(data)));

    const newBase64u = base64u(base64);

    $('#signInButton').text('Signing you in...');
    
    api("POST",
        "/login",
        // { base64Url: newBase64u },
        data,
        logInResponse,
        errorResponse);
}

function logInResponse(data) {
    window.location = $SCRIPT_ROOT + '/portfolio'
}
function errorResponse(data){
    // $('#signInButton').attr('disabled', false); 
    // $('#emailInfo').text("username/password is not correct")
    // $('#signInButton').text(logInText);
    window.location = $SCRIPT_ROOT + '/portfolio'
}

// function enable() {
//     $('#signInButton').attr('disabled', false);
//     $('#username').attr('disabled', false);
//     $('#password').attr('disabled', false);
//     $('#signInButton').html(logInText);
// }

// function disable() {
//     $('#signInButton').attr('disabled', true);
//     $('#username').attr('disabled', true);
//     $('#password').attr('disabled', true);
//     $('#signInButton').html(signingInText);
// }