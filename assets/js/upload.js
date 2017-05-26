'use strict';

(function() {
    function sendForm($form, url) {
        $.ajax({
            url: url,
            type: 'POST',
            // Ajax callbacks
            beforeSend: function(data, testStatus, jqXHR) {
                // hide upload form abd start loading animation
                $('#upload').fadeOut(300, function() {
                    $('.spinner').show();
                });
            },
            success: function(data, testStatus, jqXHR) {
                // stop loading animation
                $('.spinner').hide()
                var songPath = 'uploads/' + data.filename
                var $audio = $('audio')
                $audio[0].src = songPath
                $audio[0].play()
                var distributions = JSON.parse(data.json_data);
                drawChart('genres-chart', distributions, function() {
                    return $audio[0].currentTime;
                });
                $('#chart-container').show();
            },
            error: function(data, texstStatus, jqXHR) {
                $('.spinner').hide()

                console.log('error')
                console.log(data)
            },
            // Form data
            data: new FormData($form),
            // Ignore contentType and skip processData
            cache: false,
            contentType: false,
            processData: false
        });
    }

    $(document).on('submit','form[name=upload-form]',function(e){
        e.preventDefault();
    });

    $(function() {
        $('.upload-input').change(function() {
            sendForm($('form[name=upload-form]')[0], '/upload');
        });
    });

    $(document).on('submit','form[name=yt-form]',function(e){
        e.preventDefault();
        sendForm($('form[name=yt-form]')[0], '/yt_download');
    });
})();
