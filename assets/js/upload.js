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
                var songPath = 'uploads/' + data.filename
                $('audio').attr('src', songPath)
                // pills(songPath, data.json_data);
                var distributions = JSON.parse(data.json_data);
                drawChart('genres-chart', distributions, function() {
                    return $('audio').get(0).currentTime;
                });
                $('#chart-container').show();
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
