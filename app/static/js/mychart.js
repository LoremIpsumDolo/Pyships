var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {

        var jsonfile = JSON.parse(this.responseText);

        var data_1 = [];

        data_1.push(jsonfile.chartData.today);
        data_1.push(jsonfile.chartData.yesterday);
        data_1.push(jsonfile.chartData.weekly);
        console.log(data_1);


        var labels = ['0am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12am', '13pm', '14pm', '15pm', '16pm', '17pm', '18pm', '19pm', '20pm', '21pm', '22pm', '23pm'];
        console.log(labels);
        renderChart1(data_1, labels);
    }
};


xmlhttp.open("GET", "http://buuddy.chickenkiller.com:8000/", true);
xmlhttp.send();

function renderChart1(data_1, labels) {
    var ctx = document.getElementById("myChart1").getContext('2d');

    var gradientFill = ctx.createLinearGradient(0, 0, 0, 290);
    gradientFill.addColorStop(0, "rgba(255,0,211,0.56)");
    gradientFill.addColorStop(1, "rgba(128,37,136,0.24)");

    var myChart1 = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Today',
                    data: data_1[0],
                    backgroundColor: 'rgb(94,49,186)',
                    borderColor: '#17a2b8',
                },
                {
                    label: 'Yesterday',
                    data: data_1[1],
                    backgroundColor: '#116e7f',
                    borderColor: 'rgb(115,39,128)',
                },
                {
                    label: 'Weekly',
                    data: data_1[2],
                    type: 'line',
                    backgroundColor: gradientFill,
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        autoSkip: true
                    }
                }]
            }
        }
    });
}
