


$(document).ready(function () {

    // ======
    //code to get login info
    //For the login/sign up switch functionality
    const switchers = [...document.querySelectorAll('.switcher')]
    switchers.forEach(item => {
        item.addEventListener('click', function () {
            switchers.forEach(item => item.parentElement.classList.remove('is-active'))
            this.parentElement.classList.add('is-active')
        })
    });
    

    // ======
    // Submit the new ticket
    $(document).on('click', 'div.profile-ticket-item', function () {
        var id = $(this).attr('id');
        console.log(id);

        if ($("#ticket_detailed_info_" + id).text() == "") {
            $.ajax({
                url: "/tickets/ticket_details",
                type: "get",
                data: { ticket_id: id },
                // dataType: 'json',
                success: function (response) {
                    $("#ticket_detailed_info_" + id).html(response);
                    $("#ticket_assigned_detailed_info_" + id).html(response);
                },
                error: function (xhr) {
                    //Do Something to handle error
                }
            });
        } else {
            $("#ticket_detailed_info_" + id).html("");
            $("#ticket_assigned_detailed_info_" + id).html("");
        }
    });



    // ======
    //code to get login info
    $("#submit_new_user").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: {},
            success: function (data) {
                alert(data); // show response from the php script.
            }
        });
    });


    // ======
    //code to get login info
    $("div.ticket_detailed_info").on("click", "button.assign_watcher_li", function () {
        var id = $(this).attr('id');
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

        $.ajax({
            url: "/tickets/assign_watcher",
            type: "get",
            data: { user_id: id, ticket_id: current_ticket },
            success: function (response) {
                $.ajax({
                    url: "/tickets/ticket_details",
                    type: "get",
                    data: { ticket_id: current_ticket },
                    success: function (response) {
                        $("#ticket_detailed_info_" + current_ticket).html("");
                        $("#ticket_detailed_info_" + current_ticket).html(response);
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

    // ======
    //code to get login info
    $(document).on("click", "#submit_ticket_status", function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.
        var form = $(this);
        id = $("#current_ticket_id").attr('ticket_id');

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
                $("#ticket_detailed_info_" + id).html("");
                $("#ticket_detailed_info_" + id).html(response);
            },
            error: function (error) {
                console.log("ERROR");
                console.log(error);
            },
        });


    });

    $(document).on("click", "#clear_ticket_updates", function (e) {
        console.log("DELETING");
        $.ajax({
            type: "POST",
            url: '/user/clear_ticket_updates',
            
            success: function (response) {
                
                var self = window.location.href;
                $('#ticket_status_lists').load(self + ' #ticket_status_lists>*', '')
                // $('#ticket_updates_badge').load(self + ' #ticket_updates_badge', function () {
                //     // $('#ticket_updates_badge').trigger("refresh");

                // });
            },
            error: function (error) {
                console.log("ERROR");
                console.log(error);
            },
        });
    });



});
