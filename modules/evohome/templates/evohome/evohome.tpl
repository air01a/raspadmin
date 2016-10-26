#if (@weather!="None")
<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Weather</h3>
                        </div>
			<div class="panel-body" style="margin: auto;text-align:center;">
				<table class="table" style="border:0px">
                        		<tr><td><img src="@weather.icon"></td><td>@weather.status</td></tr>
					<tr><td>Temp : @weather.temperature C</td><td>Wind: @weather.wind.speed (@weather.wind.deg deg)</td></tr>
					<tr><td>Humidity : @weather.humidity</td><td>Pressure : @weather.pressure.press</td></tr>
					<tr><td>Sunrise : @weather.sunrise</td><td>Sunset : @weather.sunset</td></tr>
				</table>
			</div>
</div>
<br />
<br />
#end
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
<div style="width:100%;height:40%">
<canvas id="myChart" width="100%" height="40%"></canvas>
</div>
<script src="/static/js/chart/Chart.js"></script>
<script>
colors={};
colorsList=["#DC143C","#00008B","#006400","#8B008B","#483D8B","#FFD700","#00FFFF","#FF7F50","#ADFF2F","#663399","#778899"];

function getRandomColor(data) {
    if (data in colors)
	return colors[data];

    if (colorsList.length>0) {
		color = colorsList[0];
		colorsList.splice(0,1);
    } else {

	    var letters = '0123456789ABCDEF'.split('');
   	    var color = '#';
    	    for (var i = 0; i < 6; i++ ) {
        	color += letters[Math.floor(Math.random() * 16)];
    	    }
    }
    colors[data]=color;
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
            borderColor: getRandomColor("@data"),
            pointHoverBackgroundColor: getRandomColor("@data"),
            pointHoverBorderColor: getRandomColor("@data"),
            pointBorderColor: getRandomColor("@data"),
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

