


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


    //code to get login info
    // $("#submit_user_login").submit(function (e) {

    //     e.preventDefault(); // avoid to execute the actual submit of the form.

    //     var form = $(this);
    //     var url = form.attr('action');
    //     $.ajax({
    //         type: "POST",
    //         url: url,
    //         // data: form.serialize(), // serializes the form's elements.
    //         data: {

    //         },
    //         success: function (data) {
    //             alert(data); // show response from the php script.
    //         }
    //     });
    // });

});
