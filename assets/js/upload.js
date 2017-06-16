'use strict';

(function() {
    var songPath;

    function sendForm($form, url) {
        $.ajax({
            url: url,
            type: 'POST',
            // ajax callbacks
            beforeSend: function(data) {
                // hide upload form and start loading animation
                $('#upload').fadeOut(300, function() {
                    $('.spinner').show();
                });
            },
            success: function(response) {
                // stop loading animation
                $('.spinner').hide()

                // show new header
                $('#index-header').hide()
                $('#play-header').show()

                // source song
                songPath = 'uploads/' + response.filename
                $audio = $('audio');
                $audio[0].src = songPath;
                // uncomment next line for autoplay
                // togglePlay($audio)
                // warning: autoplay is buggy, causes an error in Chrome occassionally

                distributions = JSON.parse(response.json_data);
                showChart();
            },
            error: function(error) {
                $('.spinner').hide()
                if (error.status == 415) {
                    window.location.replace('/');
                    window.alert(error.responseText);
                }
                else {
                    window.location.replace('/error');
                }
            },
            // form data
            data: new FormData($form),
            // ignore contentType and skip processData
            cache: false,
            contentType: false,
            processData: false
        });
    }

    // upload forms submission
    $(document).on('submit','form[name=upload-form]',function(e){
        e.preventDefault();
    });

    $(document).on('change', '.upload-input', function() {
        sendForm($('form[name=upload-form]')[0], '/upload');      
    });

    $(document).on('submit','form[name=yt-form]',function(e){
        e.preventDefault();
        sendForm($('form[name=yt-form]')[0], '/yt_download');
    });
})();
