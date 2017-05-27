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
            // hoverBackgroundColor: hover_colors,
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

    var chart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });

    function updateChart() {
        var i = lowerBound(distribution, currentTime());

        if(distribution[i]) {
            for(var j = 0; j < 8; j++) {
                chart.data.datasets[0].data[j] =
                    parseFloat(distribution[i][1][GENRES[j]]);
            }
            chart.update();
            setTimeout(updateChart, 100);
        }
        else {
            chart.options.tooltips.enabled = true
            chart.data.datasets[0].hoverBackgroundColor = hoverColors;
        }
    }

    updateChart();
}
