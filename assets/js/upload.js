'use strict';

(function() {

    function sendForm() {
        var formData = new FormData($('form[name=upload-form]')[0]);
        $.ajax({
            url: '/upload',
            type: 'POST',

            // Ajax events
            beforeSend: function(data, testStatus, jqXHR) {
                // hide upload button
                $('#upload').fadeOut(300, function() {
                    // wave.start();
                    $('body').addClass('loading');
                });
            },
            success: function(data, testStatus, jqXHR) {
                // stop loading animation
                // wave.stop()
                $('body').removeClass('loading')

                console.log(data)

                // redirect to play.html
                // window.location.href = window.location.href.replace(/[^\/]*$/,
                //         'play.html#' + JSON.parse(data));
            },
            error: function(data, texstStatus, jqXHR) {
                // wave.stop()

                console.log('error')
                console.log(data)

                $('body').removeClass('loading')
            },

            data: formData,

            // Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    }

    $(function() {
        $('#upload input').change(sendForm);
    });

})();
