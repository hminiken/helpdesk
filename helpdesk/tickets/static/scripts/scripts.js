
$(document).ready(function () {

    $(document).on('click', 'tr.ticket_table', function () {
        var id = $(this).attr('id');
        console.log(id);
        // $("#ticket_detailed_info").html("");
        $.ajax({
            url: "/tickets/ticket_details",
            type: "get",
            data: { ticket_id: id },
            // dataType: 'json',
            success: function (response) {
                // location.reload();
                // $("#ticket_detailed_info").load(location.href + " #ticket_detailed_info>*", "");
                // $("#ticket_detailed_info").load(" #ticket_detailed_info");
                $("#ticket_detailed_info").html(response);
                console.log(response);

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
                $("#ticket_detailed_info").html("");
                $("#ticket_detailed_info").html(response);

            },
            error: function (error) {
                console.log("ERROR");
                console.log(error);
            },
        });


    });


    // Filter table
    $(document).on('keyup', '#table_search_input', function () {
        // $('#table_search_input').on('keyup', function () {
        var search_val = $(this).val().toLowerCase();

        if ($('#show_closed_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) > -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        } else if ($('#show_open_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) <= -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        }
        else if ($('#show_all_tickets').is(':checked')) {
            val = "";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(val) <= 1 &&
                    // $(this).text().toLowerCase().indexOf(val) <= 1) && 
                    $(this).text().toLowerCase().indexOf(search_val) > -1)
            });

        }

    });





    $("#show_closed_tickets").change(function () {

        search_val = document.getElementById('table_search_input').value;
        console.log("SEARCH:" + search_val)
        if ($('#show_closed_tickets').is(':checked')) {
            console.log("CHECKED");
            var val = "closed";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) > -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });

        }

    });



    $("#show_open_tickets").change(function () {

        search_val = document.getElementById('table_search_input').value;

        if ($('#show_open_tickets').is(':checked')) {
            console.log("CHECKED");
            var val = "closed";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) <= -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });

        }

    });


    $("#show_all_tickets").change(function () {

        search_val = document.getElementById('table_search_input').value;
        if ($('#show_all_tickets').is(':checked')) {
            var val = "";
            $("#ticket_table_all tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(val) <= 1 &&
                    // $(this).text().toLowerCase().indexOf(val) <= 1) && 
                    $(this).text().toLowerCase().indexOf(search_val) > -1)
            });

        }


    });





    $("div.ticket-details-div").on("click", "button.assign_status_li", function () {
        var id = $(this).attr('id');
        console.log(id);
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

        $.ajax({
            url: "/tickets/assign_status",
            type: "get",
            data: { status_id: id, ticket_id: current_ticket },
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

    });





    $("div.ticket-details-div").on("click", "button.assign_user_li", function () {
        // $("#assign_user_dropdown").css({ height: "auto" });
        var id = $(this).attr('id');
        console.log(id);
        var current_ticket = $("#current_ticket_id").attr('ticket_id');


        $.ajax({
            url: "/tickets/assign_user",
            type: "get",
            data: { user_id: id, ticket_id: current_ticket },
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
                        // $('#all_ticket_updates').load(self + ' #all_ticket_updates');

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




    // this is the id of the form
    $("#submit_new_ticket").submit(function (e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');

        alert(url);

        $.ajax({
            type: "POST",
            url: url,
            // data: form.serialize(), // serializes the form's elements.
            data: {
                cust: $('#cust_input').val(),
                assy: $('#assy_input').val(),
                pn: $('#pn_input').val(),
                wo: $('#wo_input').val(),
                cat: $('#cat_select').val(),
                subcat: $('#subcat_select').val()
            },
            success: function (data) {
                alert(data); // show response from the php script.
            }
        });


    });







});

