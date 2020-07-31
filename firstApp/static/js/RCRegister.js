$(document).ready(function() {
    $("#submit").click(function() {
        var name = $('#id_name').val();
        var email = $('#id_email').val();
        var password = $('#id_password').val();
        var password2 = $('#id_password2').val();
        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        if (email != "" && password != "") {
            $.ajax({
                url: '{% url '
                registerView ' %}',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    'name': name,
                    'email': email,
                    'password': password,
                    'password2': password2
                },
                success: function(data) {

                    var objC = data;

                    objC.toString = function() {
                        return "objC"
                    };

                    console.log(objC);

                    // $('#tBody').append(' <tr><td>' + objC.email + '</td><td>' + objC.password + '</td><td>' + objC.message + '</td></tr>');


                }
            });
        }

    });
});