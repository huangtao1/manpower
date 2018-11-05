/**
 * Created by mark.huang on 2018/1/25.
 */
$('#repassword').on('change', function () {
    var pass1 = $('#password').val();
    var pass2 = $('#repassword').val();
    if (pass1 && pass1 != pass2) {
        bootbox.alert('Two Passwords must be equaled!!!')
    }
});
