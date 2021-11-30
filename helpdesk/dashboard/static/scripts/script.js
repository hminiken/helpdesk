
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ///////////////////////////// DAILY IDS //////////////////////////////////////


$(document).ready(function () {


    const $tableID = $('#table'); const $BTN = $('#export-btn'); const $EXPORT = $('#export');
    
const newTr = `
    <tr class="">
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    <td class="pt-3-half" contenteditable="true"> </td>
    
    </tr>`;
    

$('.table-add').on('click', 'i', () => {
    console.log("ADD");
    
    if ($tableID.find('tbody tr').length
    === 0) {
        $('tbody').append(newTr);
    } 
    
    const $clone = $tableID.find('tbody tr').last().clone(true).removeClass('hide table - line');
    
    $tableID.find('table').append(newTr).removeClass('hide table - line');

});








    
    
//     
    
    
  
// $tableID.on('click', '.table-remove', function () { $(this).parents('tr').detach();

// });
// $tableID.on('click', '.table-up', function () {
//     const $row = $(this).parents('tr');
    
//     if
//     ($row.index() === 0) { return;
        
//     } $row.prev().before($row.get(0));
// });

// $tableID.on('click',
// '.table-down', function () {
//     const $row = $(this).parents('tr');
//     $row.next().after($row.get(0));
// });

// // A few jQuery helpers for exporting only jQuery.fn.pop
// =[].pop;

// jQuery.fn.shift = [].shift;

// $BTN.on('click', () => {
//     const $rows =
//     $tableID.find('tr:not(:hidden)');
    
//     const headers = [];
    
//     const data = [];
    
//     // Get the headers
//     (add special header logic here) $($rows.shift()).find('th:not(:empty)').each(function () {
//         headers.push($(this).text().toLowerCase());
//     });
    
//     // Turn all existing rows into a loopable
//     array $rows.each(function () {
//         const $td = $(this).find('td');
        
//         const h = {};
        
//         // Use the
//         headers from earlier to name our hash keys headers.forEach((header, i) => {
//             h[header] =
//             $td.eq(i).text();
//         });
        
//         data.push(h);
//     });
    
//     // Output the result
//     $EXPORT.text(JSON.stringify(data));
    
// });

});