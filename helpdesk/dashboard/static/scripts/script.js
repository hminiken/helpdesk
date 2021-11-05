
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
    var total_tickets = data[6]
    var closed_last = data[7]
    var opened_last = data[8]

    //Set header
    $('#total_tickets').text(total_tickets[0]['count']);
    $('#closed_last').text(closed_last[0]['count']);
    $('#opened_last').text(opened_last[0]['count']);
   

    // Ticket By Category
    displayData = []
    displayLabel = []
    displayData = getChartData(cat_tickets, 'count');
    displayLabel = getChartData(cat_tickets, 'category');
    chartCol = '#0A579E';
    var ctx = document.getElementById('tickets_by_category');
    makeChart(displayData, displayLabel, ctx, 'By Category', chartCol);


    // Ticket by SubCat
    displayData = []
    displayLabel = []
    displayData = getChartData(subcat_tickets, 'count');
    displayLabel = getChartData(subcat_tickets, 'subcategory');
    chartCol = '#4bd62f';
    var subcat = document.getElementById('tickets_by_subcategory');
    makeChart(displayData, displayLabel, subcat, 'By Subcategory', chartCol);


    //Ticket by created
    displayData = []
    displayLabel = []
    displayData = getChartData(created_tickets, 'count');
    displayLabel = getChartData(created_tickets, 'created');
    chartCol = '#0A579E';
    var created = document.getElementById('tickets_by_created');
    makeChart(displayData, displayLabel, created, 'By Created', chartCol);


    // Ticket by assigned
    displayData = []
    displayLabel = []
    displayData = getChartData(assigned_tickets, 'count');
    displayLabel = getChartData(assigned_tickets, 'assigned');
    chartCol = '#4bd62f';
    var assigned = document.getElementById('tickets_by_assigned');
    makeChart(displayData, displayLabel, assigned, 'By Assigned', chartCol);
    
    // Ticket by closed
    displayData = []
    displayLabel = []
    displayData = getChartData(closed_tickets, 'count');
    displayLabel = getChartData(closed_tickets, 'closed');
    chartCol = '#4bd62f';
    var closed = document.getElementById('tickets_by_closed');
    makeChart(displayData, displayLabel, closed, 'By Closed', chartCol);


            
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

var makeChart = function(makeData, makeLabel, name, title, chartCol) {
    var chart = new Chart(name,
        {
            type: 'bar',
            data: {
                labels: makeLabel,
                datasets: [{
                    label: title,
                    data: makeData,
                    backgroundColor: chartCol,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
            }
        });
}