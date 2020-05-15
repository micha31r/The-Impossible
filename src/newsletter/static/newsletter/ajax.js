// Subscribe to mailing list ajax
function join_newsletter_ajax(email) {
    $(document).ready(
        function() {
            $.ajax(
                {
                    url: `/newsletter/join/`,
                    data: {
                        'email':email,
                    },
                    dataType: 'json',
                    success: function(data) {
                        var msg;
                        $("#join-status").attr("class","alert alert-danger");
                        if (data.exsist) {
                                msg = "Email already exsist";
                        } else if (data.failed) {
                            msg = "Join Failed";
                        } else {
                            $("#join-status").attr("class","alert alert-success");
                            $("#join-form").css("display","none");
                            msg = "You have successfully subscribed!";
                        }
                        $("#join-status").html(msg);
                        $("#join-status").css("display","block");
                    }
                }
            );
        }
    );
}