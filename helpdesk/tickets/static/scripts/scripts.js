/************************************************************ /
* Author: Hillary Miniken
* Email: hminiken@outlook.com
* Date Created: 2021-11-18
* Filename: script.js
*
* Description: Implementation for javascript in the 
                tickets/index.html page
************************************************************/


$(document).ready(function () {    
    console.log("LOADED");
    // ======
    // Define a function to only show the open tickets, which we use on page load
    function getOnlyOpen() {
            var val = "closed";
        $("#ticket_table_body tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) <= -1
                )
            });
        };
        
    $('#show_open_tickets').prop('checked', true).trigger("click");

    //Call the function on page load, so that it only shows open tickets initially
    getOnlyOpen();


    // ======
    // Get the ticket details and display in the sidebar div "ticket_detailed_info"
    $(document).on('click', 'tr.ticket_table', function () {
        var id = $(this).attr('id');
        $.ajax({
            url: "/tickets/ticket_details",
            type: "get",
            data: { ticket_id: id },
            success: function (response) {
                $("#ticket_detailed_info").html(response);
            },
            error: function (xhr) {
                //Do Something to handle error
            }
        });
    });


    // ======
    // When clicking hte dropdown, apply new status to the ticket
    $(document).on("click", "#submit_ticket_status", function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.

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
                $("#ticket_detailed_info").html("");
                $("#ticket_detailed_info").html(response);
            },
            error: function (error) {
                console.log("ERROR");
                console.log(error);
            },
        });
    });


    // ======
    // Filter table
    $(document).on('keyup', '#table_search_input', function () {
        var search_val = $(this).val().toLowerCase();

        if ($('#show_closed_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) > -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        } else if ($('#show_open_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) <= -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        }
        else if ($('#show_all_tickets').is(':checked')) {
            val = "";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(val) <= 1 &&
                    // $(this).text().toLowerCase().indexOf(val) <= 1) && 
                    $(this).text().toLowerCase().indexOf(search_val) > -1)
            });
        }
    });


    // ======
    // Function to show close tickets when radio button toggles to "Closed"
    $("#show_closed_tickets").change(function () {
        search_val = document.getElementById('table_search_input').value;
        if ($('#show_closed_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) > -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        }
    });


    // ======
    // Function to show open tickets when radio button toggles to "open"
    $("#show_open_tickets").change(function () {
        search_val = document.getElementById('table_search_input').value;
        console.log("CHECKED");
        if ($('#show_open_tickets').is(':checked')) {
            var val = "closed";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle(
                    $(this).text().toLowerCase().indexOf(val) <= -1 &&
                    $(this).text().toLowerCase().indexOf(search_val) > -1
                )
            });
        }
    });


    // ======
    // Function to show all tickets when radio button toggles to "All"
    $("#show_all_tickets").change(function () {

        search_val = document.getElementById('table_search_input').value;
        if ($('#show_all_tickets').is(':checked')) {
            var val = "";
            $("#ticket_table_body tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(val) <= 1 &&
                    // $(this).text().toLowerCase().indexOf(val) <= 1) && 
                    $(this).text().toLowerCase().indexOf(search_val) > -1)
            });
        }
    });



    // ======
    // Upon assigning a status, update the db and then refresh the ticket details
    $("div.ticket-details-div").on("click", "button.assign_status_li", function () {
        var id = $(this).attr('id');
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

        $.ajax({
            url: "/tickets/assign_status",
            type: "get",
            data: { status_id: id, ticket_id: current_ticket },
            // dataType: 'json',
            success: function (response) {
                $.ajax({
                    url: "/tickets/ticket_details",
                    type: "get",
                    data: { ticket_id: current_ticket },
                    // dataType: 'json',
                    success: function (response) {
                        $("#ticket_detailed_info").html(response);

                        //Refresh the ticket table
                        var self = window.location.href;
                        getOnlyOpen();
                        // $('#ticket_table_all').load(self + ' #ticket_table_all>*', '');
                        $('#ticket_table_body').load(self + ' #ticket_table_body>*', function() {
                            $('#show_open_tickets').prop('checked', true).trigger("click");
                            var val = "closed";
                            $("#ticket_table_body tr").filter(function () {
                                $(this).toggle(
                                    $(this).text().toLowerCase().indexOf(val) <= -1
                                    )
                                });
                                
                            });
                        // getOnlyOpen();
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
    // Upon assigning a watcher, update the db and then refresh the ticket details
    $("div.ticket-details-div").on("click", "button.assign_watcher_li", function () {
        var id = $(this).attr('id');
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

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
                        $("#ticket_detailed_info").html(response);

                        

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
    // Upon assigning a user, update the db and then refresh the ticket details
    $("div.ticket-details-div").on("click", "button.assign_user_li", function () {
        var id = $(this).attr('id');
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

        $.ajax({
            url: "/tickets/assign_user",
            type: "get",
            data: { user_id: id, ticket_id: current_ticket },
            success: function (response) {
                $.ajax({
                    url: "/tickets/ticket_details",
                    type: "get",
                    data: { ticket_id: current_ticket },
                    success: function (response) {
                        $("#ticket_detailed_info").html(response);
                        // $('#ticket_table_all').load(self + ' #ticket_table_all');

                        //Refresh the ticket table
                        var self = window.location.href;
                        // $('#ticket_table_all').load(self + ' #ticket_table_all>*', '');

                        $('#ticket_table_body').load(self + ' #ticket_table_body>*', function () {
                            $('#show_open_tickets').prop('checked', true).trigger("click");
                            var val = "closed";
                            $("#ticket_table_body tr").filter(function () {
                                $(this).toggle(
                                    $(this).text().toLowerCase().indexOf(val) <= -1
                                )
                            });

                        });

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
        getOnlyOpen();
    });



    // Upon assigning a watcher, update the db and then refresh the ticket details
    $("div.ticket-details-div").on("click", "#edit_ticket_button", function () {
        var id = $(this).attr('id');
        var current_ticket = $("#current_ticket_id").attr('ticket_id');
        $.ajax({
            url: "/tickets/edit_ticket",
            type: "get",
            data: { ticket_id: current_ticket },
            success: function (response) {
                window.location.href = "/tickets/new_ticket"
            }
        });
    });
    


    // $("#commit-date-select").datepicker();
    $("div.ticket-details-div").on("change", "#commit-date-select", function () {
        var selected = $(this).val();
        var current_ticket = $("#current_ticket_id").attr('ticket_id');

        console.log(selected);

        $.ajax({
            url: "/tickets/update_commit",
            type: "get",
            data: { commit_date: selected, ticket_id: current_ticket },
            success: function (response) {
                    $.ajax({
                        url: "/tickets/ticket_details",
                        type: "get",
                        data: { ticket_id: current_ticket },
                        success: function (response) {
                            $("#ticket_detailed_info").html(response);
                            // $('#ticket_table_all').load(self + ' #ticket_table_all');

                            //Refresh the ticket table
                            var self = window.location.href;
                            // $('#ticket_table_all').load(self + ' #ticket_table_all>*', '');

                            $('#ticket_table_body').load(self + ' #ticket_table_body>*', function () {
                                $('#show_open_tickets').prop('checked', true).trigger("click");
                                var val = "closed";
                                $("#ticket_table_body tr").filter(function () {
                                    $(this).toggle(
                                        $(this).text().toLowerCase().indexOf(val) <= -1
                                    )
                                });

                            });

                        },
                        error: function (xhr) {
                            //Do Something to handle error
                        }
                    });
               
            }
        });
    });

}); //End on document load

