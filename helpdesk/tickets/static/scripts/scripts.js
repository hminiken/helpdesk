
$(document).ready(function () {
    $(document).on('click', 'tr.ticket_table', function () {
    var id = $(this).attr('id');
    console.log(id);
    // $("#ticket_detailed_info").html("");
    $.ajax({
        url: "/tickets/ticket_details",
        type: "get",
        data: { ticket_id: id},
        // dataType: 'json',
        success: function (response) {
            // location.reload();
            // $("#ticket_detailed_info").load(location.href + " #ticket_detailed_info>*", "");
            // $("#ticket_detailed_info").load(" #ticket_detailed_info");
            $("#ticket_detailed_info").html(response);
            
        },
        error: function (xhr) {
            //Do Something to handle error
        }
    });


});


    $("div.ticket-details-div").on("click", "button.assign_user_li", function () {
        // $("#assign_user_dropdown").css({ height: "auto" });
        var id = $(this).attr('id');
        console.log(id);
        var current_ticket = $("#current_ticket_id").attr('ticket_id');


        $.ajax({
            url: "/tickets/assign_user",
            type: "get",
            data: { user_id: id, ticket_id: current_ticket},
            // dataType: 'json',
            success: function (response) {
                // location.reload();
                // $("#ticket_detailed_info").load(location.href + " #ticket_detailed_info>*", "");
                // $("#ticket_detailed_info").load(" #ticket_detailed_info");
                // $("#assign_user_button").html(response);
                $.ajax({
                    url: "/tickets/ticket_details",
                    type: "get",
                    data: { ticket_id: current_ticket },
                    // dataType: 'json',
                    success: function (response) {
                        // location.reload();
                        // $("#ticket_detailed_info").load(location.href + " #ticket_detailed_info>*", "");
                        // $("#ticket_detailed_info").load(" #ticket_detailed_info");
                        $("#ticket_detailed_info").html(response);

                        //Refresh the ticket table
                        var self = window.location.href;
                        console.log("Loading '#ticket_table_all' from " + self);
                        $('#ticket_table_all').load(self + ' #ticket_table_all');

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

        // $('#assign_user_button').html(id)

    });

    


});



// $('#show_task_{{npi['RequestId']}}').unbind().click(function () {

//     // var is_shown  = $('#show_task_{{npi['RequestId']}}').data('task_is_shown');
//     var is_shown = $(this).attr('task_is_shown');
//     console.log(is_shown);
//     if (is_shown === "false") {
//         $('#show_task_{{npi['RequestId']}}').attr("task_is_shown", "true");
//         console.log({{ npi['RequestId']}});
// text = 'Hello'
// $.ajax({
//     url: "/npi_tasks",
//     type: "get",
//     data: { jsdata: is_shown, req_id: '{{ npi['RequestId']}}'},
//     // dataType: 'json',
//     success: function (response) {
//         $("#place_for_suggestions_{{npi['RequestId']}}").html(response);
//     },
//     error: function (xhr) {
//         //Do Something to handle error
//     }
// });

//                 }
//                 else {
//     $('#show_task_{{npi['RequestId']}}').attr("task_is_shown", "false");
//     $("#place_for_suggestions_{{npi['RequestId']}}").text("");
// }


//                 //Stuff
//             });