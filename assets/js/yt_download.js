  'use strict';

(function() {

    function sendYTForm() {
        var formData = new FormData($('form[name=yt-form]')[0]);
        $.ajax({
            url: '/yt_download',
            type: 'POST',

            // Ajax events
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
                // pills(songPath, data.json_data);
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

            data: formData,

            // Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    }

    $(document).on('submit','form[name=yt-form]',function(e){
        e.preventDefault();
        sendYTForm();
    });

})();
