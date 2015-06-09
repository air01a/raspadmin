<script src="/static/app/status.js"></script>
<div ng-controller="StatusCtrl" id="mainCtrl">
<br /><div class="panel panel-primary" style="width: 80%;margin: auto">
		        <div class="panel-heading">
			          <h3 class="panel-title">Information</h3>
        		</div>
		 <div class="panel-body">

                <div class="container-fluid">
                        <div class="row-fluid">
                                <div class="span12" style="margin: auto;">
                                        <ul class="today-datas" style="margin:auto;text-align: center">
                                                <li class="bred">
                                                        <div class="pull-left"><i class="icon-fire"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.temperature}}</span> CPU Temp.</div>
                                                        <div class="clearfix"></div>
						</li>
                                                <li class="bgreen">
                                                        <div class="pull-left"><i class="icon-tasks"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.la1}}</span> CPU Load</div>
                                                        <div class="clearfix"></div>
                                                </li>
                                                <li class="blightblue">
                                                        <div class="pull-left"><i class="icon-bolt"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.cpufrequency}}</span> CPU Freq.</div>
                                                        <div class="clearfix"></div>
                                                </li>
                                                <li class="bviolet">
                                                        <div class="pull-left"><i class="icon-save"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.memory.free}}</span> Free RAM</div>
                                                        <div class="clearfix"></div>
                                                </li>
                                                <li class="borange">
                                                        <div class="pull-left"><i class="icon-hdd"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.freespace}}</span> Free Disk</div>
                                                        <div class="clearfix"></div>
                                                </li><br />
	                                         <li class="bwhile">
	                                                <div class="pull-left"><i class="icon-hdd"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.hostname}}</span> Hostname</div>
                                                        <div class="clearfix"></div>
                                                </li>
						<li class="bblack">
                                                        <div class="pull-left"><i class="icon-hdd"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">{{data.uptime}}</span> Uptime</div>
                                                        <div class="clearfix"></div>
                                                </li>
						<li class="byellow">
                                                        <div class="pull-left"><i class="icon-hdd"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">
#for @i in @ip:
        @i
#end
</span> IP</div>
                                                        <div class="clearfix"></div>
                                                </li>

                            			<div class="clearfix"></div>
                                        </ul>
                                </div>
			</div>
		</div>
	</div>
</div><br />

<script type="text/javascript">
var HttpGraphId = [];
var HttpGraphPtr = [];
function HttpGraphStart(func, index)
{
	func();
}

window.onload = function () {
	for (var i = 0; i < HttpGraphId.length; i++) {
		HttpGraphId[i]();
	}
};

</script>

<script type="text/javascript">
function initHTTPGraphchart52()
{
            var chart52 = new RGraph.Pie('chart52', [@memory.usedraw,@memory.freeraw,@memory.bufferraw,@memory.cachedraw])
                .Set('strokestyle', 'white')
                .Set('colors', ['red','green','#31B404','#00FF00'])
                .Set('linewidth', 3)
                .Set('exploded', 10)
                .Set('shadow', true)
                .Set('shadow.offsetx', 0)
                .Set('shadow.offsety', 0)
                .Set('shadow.blur', 20)
                .Set('labels', ['Used','Free','Buffer','Cached'])
		.Set('tooltips', ['Used','Free','Buffer','Cached'])
                .Set('labels.sticks', [true])
                .Set('labels.sticks.length', 0)
                .Set('chart.labels.ingraph',true)
		.Set('chart.labels.ingraph.specific', ['@memory.used','@memory.free','@memory.buffers','@memory.cached'])
 
           RGraph.Effects.Pie.RoundRobin(chart52)
	   HttpGraphPtr['mem']=chart52
}
HttpGraphId.push(initHTTPGraphchart52)


function initHTTPGraphchart5b()
{
            var chart5b = new RGraph.Gauge('chart5b', 0, 100, 0)
                .Set('scale.decimals', 0)
                .Set('tickmarks.small', 50)
                .Set('tickmarks.big',5)
                .Set('title.top', '')
                .Set('title.top.size', 24)
                .Set('title.top.pos', 0.15)
                .Set('title.bottom', '')
		.Set('chart.text.size',6)
                .Set('title.bottom.color', '#aaa')
                .Set('chart.colors.ranges',[[0,30, 'red'], [30, 70,'yellow'], [70,100,'green']])
		.Set('centerpin.color', '#666')
		.Set('needle.size', [null, 50])
                .Set('border.outer', 'Gradient(white:white:white:white:white:white:white:white:white:white:#aaa)')
                .Draw();
		
		chart5b.value = @cpuusage.average; RGraph.Effects.Gauge.Grow(chart5b);
		HttpGraphPtr['5b']=chart5b
}
//HttpGraphId.push(initHTTPGraphchart5b)


function initHTTPGraphLoadAvg()
{
            var chart1 = new RGraph.Gauge('loadvg1', 0, @numcpu, 0)
                .Set('scale.decimals', 0)
                .Set('tickmarks.small', 50)
                .Set('tickmarks.big',5)
                .Set('title.top', '')
                .Set('title.top.size', 24)
                .Set('title.top.pos', 0.15)
                .Set('title.bottom', '')
                .Set('chart.text.size',6)
                .Set('title.bottom.color', '#aaa')
                .Set('chart.colors.ranges',[[0,@numcpu*0.4, 'green'], [@numcpu*0.4, @numcpu*0.8,'yellow'], [@numcpu*0.8,@numcpu,'red']])
                .Set('centerpin.color', '#666')
                .Set('needle.size', [null, 50])
                .Set('border.outer', 'Gradient(white:white:white:white:white:white:white:white:white:white:#aaa)')
                .Draw();

                chart1.value = @loadavg.la1; RGraph.Effects.Gauge.Grow(chart1);
                HttpGraphPtr['loadvg1']=chart1



	            var chart2 = new RGraph.Gauge('loadvg2', 0, @numcpu, 0)
                .Set('scale.decimals', 0)
                .Set('tickmarks.small', 50)
                .Set('tickmarks.big',5)
                .Set('title.top', '')
                .Set('title.top.size', 24)
                .Set('title.top.pos', 0.15)
                .Set('title.bottom', '')
                .Set('chart.text.size',6)
                .Set('title.bottom.color', '#aaa')
                .Set('chart.colors.ranges',[[0,@numcpu*0.4, 'green'], [@numcpu*0.4, @numcpu*0.8,'yellow'], [@numcpu*0.8,@numcpu,'red']])
                .Set('centerpin.color', '#666')
                .Set('needle.size', [null, 50])
                .Set('border.outer', 'Gradient(white:white:white:white:white:white:white:white:white:white:#aaa)')
                .Draw();

                chart2.value = @loadavg.la2; RGraph.Effects.Gauge.Grow(chart2);
                HttpGraphPtr['loadvg2']=chart2


            var chart3 = new RGraph.Gauge('loadvg3', 0, @numcpu, 0)
                .Set('scale.decimals', 0)
                .Set('tickmarks.small', 50)
                .Set('tickmarks.big',5)
                .Set('title.top', '')
                .Set('title.top.size', 24)
                .Set('title.top.pos', 0.15)
                .Set('title.bottom', '')
                .Set('chart.text.size',6)
                .Set('title.bottom.color', '#aaa')
                .Set('chart.colors.ranges',[[0,@numcpu*0.4, 'green'], [@numcpu*0.4, @numcpu*0.8,'yellow'], [@numcpu*0.8,@numcpu,'red']])
                .Set('centerpin.color', '#666')
                .Set('needle.size', [null, 50])
                .Set('border.outer', 'Gradient(white:white:white:white:white:white:white:white:white:white:#aaa)')
                .Draw();

                chart3.value = @loadavg.la3; RGraph.Effects.Gauge.Grow(chart3);
                HttpGraphPtr['loadvg3']=chart3

}
HttpGraphId.push(initHTTPGraphLoadAvg)



</script>
<div class="panel panel-success" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Load Average 1 / 5 / 15 minutes</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
	 <canvas id="loadvg1" width="250" height="170" style="display: inline">[No canvas support]</canvas>
	 <canvas id="loadvg2" width="250" height="170" style="display:inline">[No canvas support]</canvas>
	 <canvas id="loadvg3" width="250" height="170" style="display:inline">[No canvas support]</canvas><br />
		</div>
</div>
<br />
<div class="panel panel-info" style="width: 80%;margin: auto;">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Memory Usage</h3>
                        </div>
                 <div class="panel-body" style="magin:auto;text-align:center;">

     <canvas id="chart52" width="500" height="300" style="">[No canvas support]</canvas>
	<ip class="status_info>Swap Free <br />
	<span class="bar_big">
#set @percent=100 - @memory.swpercent : 
#if (@percent<50)
        #set @ptype=0 :
#else
        #set @ptype=4 :
#end


	<span class="progression@ptype one progression" style="width: @percent%">
                                <span title="6%" class="precent">@percent%</span>
                        </span>
                </span>
	Swap Free
</p>
</div>
</div>
<br />

<div class="panel panel-warning" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Partitions</h3>
                        </div>
                 <div class="panel-body">

<table class="bordered" style="width: 80%;margin: auto">
    <thead>
    <tr>
       <th>Mount Point</th>
       <th>Device</th>
       <th>Fs Type</th>
       <th>Total (Gb)</th>
       <th>Free</th>
       <th>Used</th>
       <th>Percent</th>
    </tr>
    </thead>
   <tbody>
#for @part in @disk:
   <tr >
	<td>@part.mountpoint</td>
	<td>@part.device</td>
	<td>@part.fstype</td>
	<td>@part.total</td>
	<td>@part.free</td>
	<td>@part.used</td>
	<td>#if (@part.percent<90)
        #set @ptype=4 :
#else:
        #set @ptype=0 :
#end
<span class="bar">
<span class="progression@ptype one progression" style="width: @part.percent%">
				<span title="6%" class="precent">@part.percent</span>
			</span>
		</span>
</td>
   </tr>
#end
   </tbody>
</table>
</div></div><br />

</div>
