'use strict';

(function() {
    $(document).on('click', '#examples-table h2', function(e) {
        $audio = $('audio');
        $audio[0].src = 'examples/' + e.target.id + '.mp3';

        $.ajax({
            url: 'examples/' + e.target.id + '.json',
            type: 'GET',
            success: function(response) {
                // hide examples table
                $('#examples-table').hide()
                // show new header
                $('#index-header').hide()
                $('#play-header').show()

                distributions = response;
                showChart();
            },
            error: function() {
                window.location.replace('/');
                window.alert('Oops! An error occured');
            }
        })
    });
})();
