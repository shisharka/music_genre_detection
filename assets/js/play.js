'use strict';

var GENRES = ['blues', 'country', 'disco', 'hiphop', 'metal', 'pop', 'reggae', 'rock'];

var GENRE_TO_COLOR = {
    'blues': '#0033cc',
    'country': '#cc6600',
    'disco': '#ff66cc',
    'hiphop': '#660066',
    'metal': '#999966',
    'pop': '#00cc66',
    'reggae': '#ffcc66',
    'rock': '#cc0000'
};

function lowerBound(array, element) {
    var begin = 0;
    var end = array.length;
    while(begin < end) {
        var m = Math.floor((begin + end) / 2);
        if(array[m][0] >= element)
            end = m;
        else
            begin = m + 1;
    }
    return begin;
}

function drawChart(canvasId, distribution, timeFn) {
    var startValue = 0;
    // var data = GENRES.map(function(genre) {
    //     var color = GENRE_TO_COLOR[genre];
    //     return {
    //         responsive: true,
    //         value: startValue,
    //         color: color,
    //         highlight: color,
    //         label: genre
    //     };
    // });
    var data = {
        labels: GENRES,
        // datasets: [{
        //     fillColor: GENRES.map(function(genre) {
        //         return GENRE_TO_COLOR[genre];
        //     }),
        //     data: [0, 0, 0, 0, 0, 0, 0, 0]
        // }]
        datasets: GENRES.map(function(genre) {
            var color = GENRE_TO_COLOR[genre];
            return {
                backgroundColor: color,
                borderColor: color,
                data: [startValue]
            };
        })
    };

    console.log(data)

    var context = document.getElementById(canvasId).getContext('2d');
    var options = {
        responsive: true,
        easing: 'linear',
        duration: 10
    };
    // var chart = new Chart(context, {
    //     type: 'pie',
    //     data: data,
    //     options: options
    // });
    // var chart = new Chart(context).Bar(data, options);
    var chart = new Chart(context, {
        type: 'bar',
        data: data,
        options: options
    });

    function updateChart() {
        var i = lowerBound(distribution, timeFn());

        if(distribution[i]) {
            for(var j = 0; j < 8; j++) {
                chart.data.datasets[j].data[0] =
                // chart.bars[j].value =
                    parseFloat(distribution[i][1][GENRES[j]]);
            }
            chart.update();
            setTimeout(updateChart, 100);
        }
    }

    updateChart();
}

// (function() {


//     $(function() {
//         var filename = window.location.hash.substr(1);
//         var songPath = 'uploads/' + filename;
//         var jsonPath = 'uploads/' + filename + '.json';
//         $.ajax({
//             url: jsonPath,
//             success: function(result) {
//                 // pills(songPath, result);
//                 drawChart('#genres-chart', result, function() {
//                     return $('audio').get(0).currentTime;
//                 });
//                 $('#chart-container').show();
//             }
//         });
//     });
// })();

