<script type="text/javascript">
function reloadPage(data)
{
	$.each(data, function(index, value) {
		pin=value.pin
		$("#gpio"+pin+"mode").html(value.mode)
		if (value.state==0){
			$("#gpio"+pin+"state").html('LOW')
			$("#gpio"+pin+"button").attr('value', ' Set to HIGH ');
		}else{
			$("#gpio"+pin+"state").html('HIGH')
			$("#gpio"+pin+"button").attr('value', ' Set to LOW ');
		}
		if (value.mode=="OUT"){
			$("#gpio"+pin+"buttonmode").attr('value', ' Set to INPUT ');
			$("#gpio"+pin+"button").show()
		}else {
			$("#gpio"+pin+"buttonmode").attr('value', ' Set to OUTPUT ');
			$("#gpio"+pin+"button").hide()
		}

	});	

}

function setGPIOmode(pin)
{

	if ($("#gpio"+pin+"buttonmode").val()==" Set to INPUT ")
		mode="IN"
	else
		mode="OUT"

	str="num_pin="+pin+"&alphanum_mode="+mode+"&alphanum_token=@token"
	result=$.post( "/gpio/mode", str, function(data) {
		if (data.error!=0) { 
			alert('Error during process:'+data.errormsg);
		} else {
			reloadPage(data.summary)
		}

	},"json");
}

function setGPIOstate(pin)
{
	if ($("#gpio"+pin+"button").val()==' Set to HIGH ')
		state=1
	else
		state=0
	
        str="num_pin="+pin+"&alphanum_state="+state+"&alphanum_token=@token"

        result=$.post( "/gpio/state", str, function(data) {
                if (data.error!=0) {
                        alert('Error during process:'+data.errormsg);
                } else {
			reloadPage(data.summary)
                }

        },"json");
}


</script><br />
<div class="panel panel-primary" style="width: 80%;margin: auto">
		        <div class="panel-heading">
			          <h3 class="panel-title">GPIO available</h3>
        		</div>
		 <div class="panel-body">
	<img src="/static/images/gpio.png">
	</div>
</div>

<br />
<div class="panel panel-default" style="width: 80%;margin: auto">
  <!-- Default panel contents -->
  <div class="panel-heading">GPIO summary</div>

#if (@summary)
<table class="table" >
    <thead>
    <tr>
       <th width="30px" style="text-align: center">Number</th>
       <th width="30px" style="text-align: center">Mode</th>
       <th width="60px" style="text-align: center">State</th>
       <th style="text-align: center">Comment</th>
       <th width="400px" style="text-align: center">Action</th>
    </tr>
    </thead>
   <tbody>
   #for @gpio in @summary:
   <tr style="text-align:center">
	<td>@gpio.pin</td>
	<td id="gpio@{gpio.pin}mode">@gpio.mode</td>
	<td id="gpio@{gpio.pin}state">
	#if (@gpio.state)
		HIGH
	#else
		LOW
	#end</td>
	<td>@gpio.comment</td>
	<td width="200 px"><center>
		#if (@gpio.mode=="IN")
			<input id="gpio@{gpio.pin}buttonmode" type="button" value=" Set to OUTPUT " onClick="setGPIOmode(@gpio.pin)">&nbsp;
		#else
			<input id="gpio@{gpio.pin}buttonmode" type="button" value=" Set to INPUT " onClick="setGPIOmode(@gpio.pin)">&nbsp;
		#end
		#if (@gpio.state)
			#set @new="LOW" :
		#else
			#set  @new="HIGH" :
		#end
		<input id="gpio@{gpio.pin}button" type="button" value=" Set to @new " onClick="setGPIOstate(@gpio.pin)" class=""></center></td>
		#if (@gpio.mode=="IN")
			<script>$("#gpio@{gpio.pin}button").hide()</script>
		#end
   </tr>
   #end
   </tbody>
</table>
	If you want to stop this module, please click on this button : 
        <button type="button" class="btn btn-default btn-lg" onClick="document.location='/gpio/clean'">
                  <span class="glyphicon glyphicon-stop"></span> Stop
        </button>

	
#else
	You must init the gpio module by clicking on this button :

	<button type="button" class="btn btn-default btn-lg" onClick="document.location='/gpio/init'">
		  <span class="glyphicon glyphicon-ok-sign"></span> Start
	</button>
#end
</div>
