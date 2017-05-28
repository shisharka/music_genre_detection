'use strict';

(function() {
    var distributions, songPath, $audio;

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
                $audio[0].src = songPath
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

    function showChart(end = false) {
        drawChart('genres-chart', distributions, function() {
            if (end) {
                $audio[0].currentTime = $audio[0].duration;
                $audio[0].pause();
                return $audio[0].duration;
            }
            else
                return $audio[0].currentTime;
        });
        $('#chart-container').show();
    }

    function togglePlay() {
        if (!$audio) return;

        if ($audio[0].paused) {
            $audio[0].play();
            $('.play-btn .fa-play').hide();
            $('.play-btn .fa-pause').show();
        }
        else {
            $audio[0].pause();
            $('.play-btn .fa-pause').hide();
            $('.play-btn .fa-play').show();
        }
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

    // header button events
    $(document).on('click', '.play-btn.active', function() {
        togglePlay($audio);
    });

    $(document).on('click', '.upload-new-btn', function() {
        window.location = '/';
    });

    $(document).on('click', '.jump-to-end-btn.active', function() {
        if (!$audio) return;

        showChart(true);
        $('.jump-to-end-btn').removeClass('active');
        $('.play-btn').removeClass('active');
    });
})();
