#for @temperature in @temperatures:
<div class="panel panel-primary" style="width: 20%;margin-left: 10px;margin-right: 10px; float:left">
		        <div class="panel-heading">
			          <h3 class="panel-title" style="text-align:center">@temperature.name</h3>
        		</div>
		 <div class="panel-body" style="text-align:center">
			@temperature.temperature
		</div>
</div>
#end
<div style="width:800px;height:400px">
<canvas id="myChart" width="800" height="400"></canvas>
</div>
<script src="/static/js/chart/Chart.js"></script>
<script>
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
var ctx = document.getElementById("myChart");

var data = {
    labels: @history.abs,
    datasets: [
#for @data in @history:
#if (@data!='abs')
        {
            label: "@data",
            fill: false,
            lineTension: 0.1,
            borderColor: getRandomColor(),
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointBorderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: @history.get(@data),
            spanGaps: false,
        },
#end
#end
    ]
};


var myLineChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        scales: {
            xAxes: [{
                display: true
            }]
        }
    }
});


</script>

