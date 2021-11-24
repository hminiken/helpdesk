/************************************************************ /
* Author: Hillary Miniken
* Email: hminiken@outlook.com
* Date Created: 2021-11-18
* Filename: create_ticket.js
*
* Description: Implementation for javascript in the
                tickets/create_ticket.html page
************************************************************/


$(document).ready(function () {

    // ======
    // Submit the new ticket
    // TO DO: Verify if this can be deleted with the new WTForms method
    $("#submit_new_ticket").submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.
        var form = $(this);
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
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


    // ======
    // Load the open tickets under that customer when a new customer is selected in the dropdown
    let cust_select = document.getElementById('customer');
    cust_select.onchange = function () {
        cust = customer.value;
        $.ajax({
            type: "GET",
            url: '/tickets/already_created',
            data: {
                cust: cust
            },
            success: function (response) {
                $("#current_open_ticket_list").html("");
                $("#current_open_ticket_list").html(response);
            },
            error: function (error) {
            },
        });
    }


    // ======
    // If user selected a new category, load the relevant subcategories in the drop down
    document.getElementById('category').onchange = function () {
        cust = category.value;
        subcat_select = document.getElementById('subcat');

        fetch('/tickets/new_ticket/' + category.value).then(function (response) {
            response.json().then(function (data) {
                let optionHTML = ''
                for (let subcat of data.subcats) {
                    optionHTML += '<option value="' + subcat.id + '">' + subcat.subcategory_name + '</option>';
                    subcat_select.innerHTML = optionHTML;
                }
            })
        });
    }

}); //End document ready