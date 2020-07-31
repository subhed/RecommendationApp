$(document).ready(function() {
    $("#submit").click(function() {
        var email = $('#defaultLoginFormEmail').val();
        var password = $('#defaultLoginFormPassword').val();
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        if (email != "" && password != "") {
            $.ajax({
                url: '{% url '
                loginCheck ' %}',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    'email': email,
                    'password': password
                },
                success: function(data) {


                    $('#defaultLoginFormEmail').val("");
                    $('#defaultLoginFormPassword').val("");

                }
            });

        }

    });
});