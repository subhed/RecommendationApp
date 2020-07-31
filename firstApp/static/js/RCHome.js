$(document).ready(function() {
    $("#id_location").removeAttr("required");
    $("#id_image").addClass('custom-file-input1 col-3');
    $("#id_category").addClass('form-control col-3 m-2');
    $("#id_category").css({ 'display': 'inline', 'border': '0px solid #fff' });



    $(".addCategory").click(function() {
        $('#id_category').replaceWith('<input type="text" name="category" class="form-control col-4 m-2" style="display: inline; border: 0px solid rgb(255, 255, 255);" placeholder="Enter Your Category." id="id_category">');
    });

    $("#submit").click(function() {
        var content = $('#id_post_message').val();
        var location = $('#id_location').val();
        var category = $('#id_category').val();
        var user = $('#user_id').val();
        var user_name = $('#user_name').val();

        csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        var data = new FormData();

        if ($("#id_image").val() != '') {
            var myFile = document.getElementById('id_image'); // Our HTML files' ID
            var files = myFile.files;
            var file = files[0];
            data.append('image', file, file.name);
        }

        data.append('post_message', content);
        data.append('location', location);
        data.append('category', category);
        data.append('user', user);
        data.append('user_name', user_name);



        console.log("Data");
        for (var pair of data.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }


        if (content != "") {
            $.ajax({
                url: 'http://localhost:8000/postCheck/',
                type: 'POST',
                contentType: 'multipart/form-data',
                cache: false,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: data,
                success: function(data) {

                    $('#id_post_message').val("");
                    $('#id_location').val("");
                    $('#id_category').val("");


                    if (location) {
                        frame = '<iframe class="p-3" style="width: 100%; height: 15em;" id="gmap_canvas" src="https://maps.google.com/maps?q=' + location + '&t=&z=13&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>';
                    } else {
                        frame = '';
                    }

                    if ($("#id_image").val() != '') {
                        image = '<img src="http://localhost:8000' + data.image + '" style="max-width: 100%; padding: 1em; max-height: 500px;">';
                    } else {
                        image = '';
                    }



                    $('#post_box').prepend('<div id="post' + data.postId + '" class="box border mt-3" style="width: 100%; height: auto;"> <div class="row"> <div class="col-6 pl-4 pt-3"> <img src="https://i.ya-webdesign.com/images/teacher-clip-filipino-3.png" class="img-thumbnail border-0" style="display: inline; height: 3em;"> <span class="font-weight-normal" style="display: inline;">' + user_name + '</span></div><div class="col-6 pt-4 pr-4 text-right"><p class="mr-1" style="color: #d3d3d3; font-size: .7em; display: inline;"><i class="far fa-clock" style=""></i> Now </p><p class="mr-1 deleteBtn"  style="color: #d3d3d3; font-size: .7em; display: inline; cursor: pointer;" id="' + data.postId + '"><i class="far fa-trash-alt"></i> Delete</p></div><div class="col-6 pl-4 pt-3"> <p style="display: inline; font-size: .9em; color: #000;" class="pl-1">' + content + '</p></div></div>' + image + ' ' + frame + '<div class="p-3"> <div class="row mb-3"> <img src="https://i.ya-webdesign.com/images/teacher-clip-filipino-3.png" class=" ml-3 img-thumbnail border-0" style="display: inline; height: 3em;"> <form class="col-9 w-100" id="form' + data.postId + '"> <textarea id="textIn' + data.postId + '" style="height: 2.5em; border-color: #d3d3d3; padding: .5em; width: 100%;" placeholder="Comment here.."></textarea> <input type="text" style="display: none;" value="Something"> </form> <div class="col-1 cmt-post btn-default w-100" style="height: 3em; margin: 0px; margin-left: 1em;vertical-align: middle; text-align: center; padding-top: .8em; width: 100%; font-size: .8em;" id="' + data.postId + '"> Post</div></div><div style="font-size: 1em;" id="com' + data.postId + '"> </div></div></div>');
                    // &middot; <p style="display: inline; font-size: .9em; color: #d3d3d3;">' + category + '</p><
                }
            });

        }

    });


    $.getJSON("http://localhost:8000/getCategory/", function(result) {

        var obj = JSON.parse(result);
        for (var cat in obj) {

            $('#chatGroup').append('<a href="/chat/' + obj[cat].fields.category + '/"><div class="btn btn-default w-100">' + obj[cat].fields.category + '</div></a>');

        }
    });

});

$(document).on('click', '.cmt-post', function() {
    var id = $(this).attr("id");
    var content = $('#textIn' + id).val();

    // csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    if (content != "") {
        $.ajax({
            url: '/commentCheck',
            type: 'GET',

            data: {
                'comment_message': content,
                'post_id': id
            },
            success: function(data) {

                $('#textIn' + id).val("");
                $('#com' + id).prepend(' <div id="cmt' + data.cmtId + '" class="row"><div class="col-7"> <span class="text-default font-weight-bold">' + data.name + ' &centerdot; </span> ' + data.comment_message + ' </div><div class="col-5" style="font-size: .8em; padding: .3em; text-align:right;"><p id="' + data.cmtId + '" class="like mr-1" style="color: #66c2ff; font-size: .9em; display: inline;cursor: pointer;"> <i class="far fa-thumbs-up"></i><span class="like' + data.cmtId + '"> 0</span> </p><p id="' + data.cmtId + '" class="dislike mr-1" style="color: #ff6666; font-size: .9em; display: inline;cursor: pointer;"> <i class="far fa-thumbs-down"></i><span class="dislike' + data.cmtId + '"> 0</span> </p><p class="mr-1" style="color: #d3d3d3; font-size: .7em; display: inline;"><i class="far fa-clock" style=""></i> Just Now</p> <p class="deleteBtnCmt mr-1" id="' + data.cmtId + '"  style="color: #d3d3d3; font-size: .7em; display: inline; cursor: pointer;"><i class="far fa-trash-alt"></i> Delete</p> </div>  </div> ');
            }
        });

    }

});



$(document).on('click', '.deleteBtn', function() {
    var id = $(this).attr("id");
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    var r = confirm("Do you want to delete this post?");
    if (r == true) {
        if (id != "") {
            $.ajax({
                url: 'http://localhost:8000/postDelete/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    'postId': id
                },
                success: function(data) {
                    $("#post" + id).slideUp('slow');

                }
            });

        }
    }
});

$(document).on('click', '.deleteBtnCmt', function() {
    var id = $(this).attr("id");
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var r = confirm("Do you want to delete this post?");
    if (r == true) {
        if (id != "") {
            $.ajax({
                url: 'http://localhost:8000/commentDelete/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                data: {
                    'cmtId': id
                },
                success: function(data) {

                    $("#cmt" + id).slideUp('slow');

                }
            });

        }
    }



});


$(document).on('click', '.dislike', function() {
    var id = $(this).attr("id");
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    if (id != "") {
        $.ajax({
            url: 'http://localhost:8000/commentDisLike/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            data: {
                'cmtId': id
            },
            success: function(data) {
                $('.dislike' + id).html(data.newCount);
            }
        });

    }


});

$(document).on('click', '.like', function() {
    var id = $(this).attr("id");
    csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    if (id != "") {
        $.ajax({
            url: 'http://localhost:8000/commentLike/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            data: {
                'cmtId': id
            },
            success: function(data) {
                $('.like' + id).html(data.newCount);
            }
        });

    }

});