'use strict';

var GENRES = ['blues', 'country', 'disco', 'hiphop', 'metal', 'pop', 'reggae', 'rock'];

var GENRE_TO_COLOR = {
    'blues': 'rgba(105, 105, 105, 0.8)',
    'country': 'rgba(193, 66, 0, 0.8)',
    'disco': 'rgba(144, 93, 0, 0.8)',
    'hiphop': 'rgba(190, 202, 0, 0.8)',
    'metal': 'rgba(0, 131, 2, 0.8)',
    'pop': 'rgba(32, 178, 170, 0.8)',
    'reggae': 'rgba(0, 7, 213, 0.8)',
    'rock': 'rgba(144, 0, 123, 0.8)'
};

var GENRE_TO_HOVER_COLOR = {
    'blues': 'rgb(105, 105, 105)',
    'country': 'rgb(193, 66, 0)',
    'disco': 'rgb(144, 93, 0)',
    'hiphop': 'rgb(190, 202, 0)',
    'metal': 'rgb(0, 131, 2)',
    'pop': 'rgb(32, 178, 170)',
    'reggae': 'rgb(0, 7, 213)',
    'rock': 'rgb(144, 0, 123)'
};

var GLOBAL = {
    timeouts: [], // global timeout ids array
    setTimeout: function(code, number){
        this.timeouts.push(setTimeout(code, number));
    },
    clearAllTimeouts: function(){
        for (var i=0; i<this.timeouts.length; i++) {
            window.clearTimeout(this.timeouts[i]); // clear all the timeouts
        }
        this.timeouts= []; // empty the ids array
    }
};

var chart, $audio, distributions;

function lowerBound(array, element) {
    var begin = 0;
    var end = array.length - 1;
    while(begin < end) {
        var m = Math.floor((begin + end) / 2);

        if(array[m][0] == element) return m;

        if(array[m][0] > element)
            end = m - 1;
        else
            begin = m + 1;
    }
    return begin;
}

function drawChart(canvasId, distribution, currentTime) {
    var colors = GENRES.map(function(genre) {
        return GENRE_TO_COLOR[genre];
    });

    var hoverColors = GENRES.map(function(genre) {
        return GENRE_TO_HOVER_COLOR[genre];
    });

    var data = {
        labels: GENRES,
        datasets: [{
            backgroundColor: colors,
            borderColor: 'rgba(50, 0, 30, 0.7)',
            data: [0, 0, 0, 0, 0, 0, 0, 0] 
        }]
    };

    var ctx = document.getElementById(canvasId).getContext('2d');
    var options = {
        easing: 'linear',
        duration: 10,
        legend: {
            labels: {
                fontColor: 'white',
                fontSize: 15
            },
            onClick: function(event, legendItem) {}
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    var label = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                    var datasetLabel = data.labels[tooltipItem.index];
                    return datasetLabel + ': ' + label;
                }
            },
            enabled: false
        }
    };
    
    if(!chart) {
        chart = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: options
        });
    }
    else {
        chart.data.datasets.data = data.datasets.data;
    }

    function updateChart() {
        var i = lowerBound(distribution, currentTime());
        var timeoutId;

        for(var j = 0; j < 8; j++) {
            chart.data.datasets[0].data[j] =
                parseFloat(distribution[i][1][GENRES[j]]);
        }
        chart.update();
        
        if(i < distribution.length - 1) {
            GLOBAL.setTimeout(updateChart, 100);
        }
        else {
            GLOBAL.clearAllTimeouts();
            chart.options.tooltips.enabled = true
            chart.data.datasets[0].hoverBackgroundColor = hoverColors;
            $('.jump-to-end-btn').removeClass('active');
            $('.play-btn').removeClass('active');
        }
    }

    updateChart();
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
