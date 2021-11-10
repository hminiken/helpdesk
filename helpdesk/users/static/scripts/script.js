


$(document).ready(function () {

    //For the login/sign up switch functionality
    const switchers = [...document.querySelectorAll('.switcher')]

    switchers.forEach(item => {
        item.addEventListener('click', function () {
            console.log("MY JS FILE")

            switchers.forEach(item => item.parentElement.classList.remove('is-active'))
            this.parentElement.classList.add('is-active')
        })
    });


    $(document).on('click', 'div.profile-ticket-item', function () {
        var id = $(this).attr('id');
        console.log(id);
        // $("#ticket_detailed_info").html("");
        console.log("HI");

        if ($("#ticket_detailed_info_" + id).text() == "")
        {
            console.log("HI2");

            $.ajax({
                url: "/tickets/ticket_details",
                type: "get",
                data: { ticket_id: id },
                // dataType: 'json',
                success: function (response) {
                    // location.reload();
                    // $("#ticket_detailed_info").load(location.href + " #ticket_detailed_info>*", "");
                    // $("#ticket_detailed_info").load(" #ticket_detailed_info");
                    console.log("HI3");

                    $("#ticket_detailed_info_" + id).html(response);
                    console.log($("#ticket_detailed_info_" + id).text());

                },
                error: function (xhr) {
                    //Do Something to handle error
                }
            });
        } else {
            $("#ticket_detailed_info_" + id).html("");
        }


    });




    //code to get login info
    $("#submit_new_user").submit(function (e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            // data: form.serialize(), // serializes the form's elements.
            data: {
            
            },
            success: function (data) {
                alert(data); // show response from the php script.
            }
        });
    });





    $("div.ticket_detailed_info").on("click", "button.assign_watcher_li", function () {
        var id = $(this).attr('id');
        console.log(id);
        var current_ticket = $("#current_ticket_id").attr('ticket_id');
        console.log("current_ticket " + current_ticket);


        $.ajax({
            url: "/tickets/assign_watcher",
            type: "get",
            data: { user_id: id, ticket_id: current_ticket },
            // dataType: 'json',
            success: function (response) {
                $.ajax({
                    url: "/tickets/ticket_details",
                    type: "get",
                    data: { ticket_id: current_ticket },
                    // dataType: 'json',
                    success: function (response) {
                        console.log("WATCHER: " + "#ticket_detailed_info_" + id)
                        $("#ticket_detailed_info_" + current_ticket).html("");

                        $("#ticket_detailed_info_" + current_ticket).html(response);
                        //Refresh the ticket table
                        var self = window.location.href;
                        $('#ticket_profile_lists').load(self + ' #ticket_profile_lists');

                    },
                    error: function (xhr) {
                        //Do Something to handle error
                    }
                });

            },
            error: function (xhr) {
                //Do Something to handle error
            }
        });

    });


    // $("#submit_ticket_status").submit(function (e) {
    $(document).on("click", "#submit_ticket_status", function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');



        id = $("#current_ticket_id").attr('ticket_id');
        console.log("SUBMIT " + id);


        const fields = {
            csrf_token: {
                input: document.getElementById('csrf_token'),
                error: document.getElementById('csrf_token-error')
            },
            comment: {
                input: document.getElementById('comment'),
            },
            ticket_ID: {
                input: document.getElementById('ticket_id'),
            }
        }


        $.ajax({
            type: "POST",
            url: '/tickets/ticket_details',
            data: {
                csrf_token: fields.csrf_token.input.value,
                comment: fields.comment.input.value,
                ticket_id: fields.ticket_ID.input.value
            },


            success: function (response) {
                // console.log(response)
                $("#ticket_detailed_info_" + id).html("");
                $("#ticket_detailed_info_" + id).html(response);


            },
            error: function (error) {
                console.log("ERROR");
                console.log(error);
            },
        });


    });



});
