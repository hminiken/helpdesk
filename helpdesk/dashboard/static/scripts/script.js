
// // const Chart = require('chart.js');



function onPageLoad(data)
{
    
    console.log("JS FILE");
    console.log( data );
    
    var tickets = data[0]
    var cat_tickets = data[1]
    var subcat_tickets = data[2]
    var assigned_tickets = data[3]
    var created_tickets = data[4]
    var closed_tickets = data[5]
   
    displayData = []
    displayLabel = []

    displayData = getChartData(cat_tickets, 'count');
    displayLabel = getChartData(cat_tickets, 'category');

    var ctx = document.getElementById('tickets_by_category');
    makeChart(displayData, displayLabel, ctx);
    
            
}

var dynamicColors = function () {
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    return "rgb(" + r + "," + g + "," + b + ")";
};

var getChartData =  function(array, keyword) {
    console.log(array);

    chartData = []
    for (let i = 0; i < array.length; i++) {
        chartData[i] = array[i][keyword];
    }
    console.log("RETURNING");
    console.log(chartData);
    return chartData;
};

var getChartLabel = function(array) {
    chartLabel = []
    for (let i = 0; i < array.length; i++) {
        chartLabel[i] = array[i]['category'];
    }

    return chartLabel
}

var makeChart = function(makeData, makeLabel, name) {
    var chart = new Chart(name,
        {
            type: 'bar',
            data: {
                labels: makeLabel,
                datasets: [{
                    label: 'NPI Assemblies',
                    data: makeData,
                    backgroundColor: '#0A579E',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
            }
        });
}