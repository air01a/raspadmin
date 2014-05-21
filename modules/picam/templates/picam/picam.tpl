#if (@isActive==0)
&nbsp;<a href="/picam/start"><button type="button" class="btn btn-success btn-lg" data-dismiss="modal">Start</button></a>
<script>
function webservice(action,value) {

}
</script>

#else
<a href="/picam/stop/">
&nbsp;<button type="submit" class="btn btn-danger btn-lg">Stop</button>
</a>
<script>

function loadImage(){
	result=$.get("/picam/getimage",function(data){
                $('#capture').attr('src',"data:image/jpg;base64," + data.image);
        },"json");
}

function webservice(action,value) {
	$.post( "/picam/ws", { "alphanum_token": "@token","alphanum_action":action,'str_value':value }, function( data ) {
		if (data.error!=0) {
			$('#error').html(data.errorstr)
			$('#error').show()
			$('#error').delay(5000).fadeOut()
		}
	});
}

$(document).ready(function() {
	loadImage()
	window.setInterval(loadImage, 1000);
});
</script>
#end




<div class="panel panel-success" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">PiCamera</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
			<div style="margin: auto"><img style="max-width: 80%" src="/static/images/nocapture.png" id="capture"></div>
			<br />
			<button type="button" class="btn btn-success btn-lg" data-dismiss="modal" onclick="webservice('light_inc','')">Bri +</button>
			<button type="button" class="btn btn-success btn-lg" data-dismiss="modal" onclick="webservice('light_dec','')">Bri -</button>
			&nbsp;&nbsp;&nbsp;
                        <button type="button" class="btn btn-primary btn-lg" data-dismiss="modal" onclick="webservice('exposure_inc','')">Exp +</button>
                        <button type="button" class="btn btn-primary btn-lg" data-dismiss="modal" onclick="webservice('exposure_dec','')">Exp -</button>
			<br /><br /> 
			#if (@manageServoX=="1")
				<button type="button" class="btn btn-danger btn-lg" data-dismiss="modal" onclick="webservice('movex_dec','')"><<</button>
				&nbsp;&nbsp;&nbsp;
				<button type="button" class="btn btn-danger btn-lg" data-dismiss="modal" onclick="webservice('movex_inc','')">>></button>
			#end
		</div>

		
</div>
@manageServoX
<br />
<div class="alert alert-danger" id="error"></div>
<script>
$('#error').hide()
</script>
