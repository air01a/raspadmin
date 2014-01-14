#if (@connected)
<table border="0" width="100%">
<tr>
  <td>
	&nbsp;
  </td>
  <td>
		<button class="btn btn-primary btn-lg" data-toggle="modal" data-target="#idaddshare">Add package</button>
 </td>
<td style="text-align: right">
       <p style="text-align: right"> <form method="POST" id="stopserviceform"><input type="hidden" name="alphanum_token" value="@token"><input type="hidden" name="alphanum_action" value="stopservice"><button type="submit" class="btn btn-danger">Stop Service</button></p>
        </form>
</td>
</tr>
</table>
<form id="dynaction" method="POST">
<input type="hidden" name="alphanum_token" value="@token">
<input type="hidden" name="alphanum_action" value="" id="dynactioninput">
<input type="hidden" name="id_pid" value="" id="dynactionid">
</form>

<script>

function packageaction(id,action){
	$("#dynactionid").val(id)
	$("#dynactioninput").val(action)
	$("#dynaction").submit()
}
</script>
<br />
<!-- Modal -->
<div class="modal fade" id="idaddshare" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel" style="color:blue;"> Add package </h4>
      </div>
      <div class="modal-body">
		<form action="" method="POST" id="packageform">
			<label for="Name" style="text-align: right">Name : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="text" name="alphanum_name" value=""></p><br />
			<label for="links" style="text-align: right">Name : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<textarea name="str_links" rows="8" column="100" style="width:300px"></textarea></p><br />
<input type="hidden" name="alphanum_token" value="@token">
<input type="hidden" name="alphanum_action" value="addpackage">
	<p style="text-align:center"><button class="btn btn-primary btn-lg" type="submit">Add</button></p>
	</form>	
      </div>
      <div class="modal-footer">
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal  -->
<br />
<div class="panel panel-primary" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Download in progress</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
			<table class="table">
			<thead>
			<tr>
				<th style="text-align: center">Package</th>
				<th style="text-align: center">File</th>
				<th style="text-align: center">State</th>
				<th style="text-align: center">ETA</th>
       			        <th style="text-align: center">Speed</th>
			</tr>
			</thead>
			<tbody>
#for @dwn in @download:
			<tr >
				<td>@dwn.packageName</td>
				<td>@dwn.name</td>
				<td>@dwn.statusmsg</td>
				<td>@dwn.format_eta</td>
				<td>@dwn.format_speed</td>
			<tr>
			<tr>
				<td style="border-top : 0px dotted  ;">@dwn.format_size</td>
#if (@dwn.percent<90)
        #set @ptype=0: 
#else:
        #set @ptype=2:
#end

				<td colspan="4" style="border-top : 0px dotted;">
					<span class="bar" style="width: 100%">
					<span class="progression@ptype one progression" style="width: @dwn.percent%">
                                	<span title="6%" class="precent">@dwn.percent % </span>
                        </span>
                </span>

			</td>
			</tr>
#end
			</tbody>
			</table>
			<br />
		</div>
</div>

<br />
<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Package</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
                        <table class="table">
                        <thead>
                        <tr>
                                <th style="text-align: center">Name</th>
                                <th style="text-align: center">Link</th>
				<th style="text-align: center">Size</th>
				<th style="text-align: center">Action</th>
                        </tr>
                        </thead>
                        <tbody>
#for @download in @queue:
                        <tr>
                                <td>@download.name</td>
                                <td>@download.linksdone / @download.linkstotal</td>
				<td>#if (@download.sizedone==@download.sizetotal)
					<span style="color: green">
				    #else
					 <span style="color: orange">	
	         			#end 
				@download.sizedoneformated / @download.sizetotalformated</span></td>
				<td><a href="#" onClick="packageaction('@download.pid','refresh')"><img src="/static/images/arrow_refresh.png"></a>&nbsp;
					<a onClick="packageaction('@download.pid','delete')"><img src="/static/images/delete.png"></a>
                        </tr>
#end
                        </tbody>
                        </table>
                        <br />
				<form method="post" id="clearfinishd">
					<input type="hidden" name="alphanum_token" value="@token">
					<input type="hidden" name="alphanum_action" value="clearfinished">
					<button type="submit" class="btn btn-danger">Clear finished package</button>
				</form>
			<br />
                </div>
</div>
#else
	The service seems stopped. Please start it.
	<form method="POST" id="">
		<input type="hidden" name="alphanum_token" value="@token">
		<input type="hidden" name="alphanum_action" value="startservice">
		<button type="submit" class="btn btn-danger">Start</button>
	</form>
#end
