#if (@error==1)
	<form method="POST" id="stopserviceform"><input type="hidden" name="alphanum_token" value="@token"><input type="hidden" name="alphanum_action" value="startservice"><button type="submit" class="btn btn-danger">Start Service</button></form>
#stop
#end
        <form method="POST" id="stopserviceform"><input type="hidden" name="alphanum_token" value="@token"><input type="hidden" name="alphanum_action" value="stopservice"><button type="submit" class="btn btn-danger">Stop Service</button></form>

<!-- Modal -->
<div class="modal fade" id="idadddownload" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Add Package</h4>
      </div>
      <div class="modal-body">
		 <form role="form" enctype="multipart/form-data" method="POST" action="/nzbget/adddownload">
		<div class="form-group">
    			<label for="Name">Package name</label>
    			<input type="text" class="form-control" placeholder="Packagename" name="str_name">
  		</div>
  		<div class="form-group">
    		<label for="InputFile">File input</label>
    		<input type="file" name="nzbd" width="400px" style="display: inline;width: 400px">
	  	</div>
                <div class="form-group">
		<label for="InputFile">Add to top</label>
		<input type="hidden" name="alphanum_token" value="@token">
      		<input type="checkbox" name="alphanum_addtotop">
 	 	</div>
	
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-primary">Apply change</button>
	</form>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
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
                                                        <div class="datas-text pull-right"><span class="bold">#if (@status.ServerPaused) Pause #else Running #end</span> Status</div>
                                                        <div class="clearfix"></div>
						</li>
                                                <li class="bgreen">
                                                        <div class="pull-left"><i class="icon-tasks"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">@status.RemainingSizeLoFormated</span> Remaining</div>
                                                        <div class="clearfix"></div>
                                                </li>
                                                <li class="blightblue">
                                                        <div class="pull-left"><i class="icon-bolt"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">@status.DownloadRateFormated</span> Dwn rate</div>
                                                        <div class="clearfix"></div>
                                                </li>
                                                <li class="bviolet">
                                                        <div class="pull-left"><i class="icon-save"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">@status.DownloadedSizeLoFormated</span> Saved</div>
                                                        <div class="clearfix"></div>
                                               </li>
	                                      <li class="borange">
                                                        <div class="pull-left"><i class="icon-bolt"></i></div>
                                                        <div class="datas-text pull-right"><span class="bold">@status.AverageDownloadRateFormated</span> Avrg dnw rate</div>
                                                        <div class="clearfix"></div>
                                                </li><br />
                                                <br />
                                                        <div class="clearfix"></div>
                                                </li>

                            			<div class="clearfix"></div>
                                        </ul>
                                </div>
			</div>
		</div>
	</div>
</div><br />
<form id="dyn" method="POST" action="/nzbget/deletepackage">
<input type="hidden" name="alphanum_token" value="@token">
<input type="hidden" name="id_id" value="" id="iddelete">
</form>
<script>
actionInProgress=0
function deletepackage(id) {
	$("#iddelete").val(id)
	$("#dyn").submit()
}

$('#idadddownload').on('show.bs.modal', function (e) {
	actionInProgress=1
})

$('#idadddownload').on('hide.bs.modal', function (e) {
        actionInProgress=0
})


function reload() {
	if (actionInProgress==0){
		location.reload()
	}

}

$( document ).ready(function() {
	window.setInterval(reload, 60000);
});

</script>
<div class="panel panel-danger" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Current Download</h3>
                        </div>
			<table class="table table-striped">
			<tr>
				<th>Name</th>
				<th>Destination</th>
				<th>Health</th>
				<th>Downloaded</th>
				<th>Action</th>
			</tr>
#for @dwn in @listgroups:
			<tr>
				<td>@dwn.NZBNicename</td>
				<td>@dwn.DestDir</td>
				<td>@dwn.Health (critical=@dwn.CriticalHealth)</td>
				<td><span style="color: green">@dwn.DownloadedFormated </span>/ <span style="color: red">@dwn.FileSizeLoFormated</td>
				<td><button class="btn btn-danger" onClick="deletepackage('@dwn.LastID')">Delete</button></td>
			</tr>
#end			
			</table>
                 <div class="panel-body" style="margin: auto;text-align:center;">
			<button class="btn btn-primary btn-lg" data-toggle="modal" data-target="#idadddownload">Add Download</button>
		 </div>
</div>
<br />
<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Post Queue</h3>
                        </div>
                        <table class="table table-striped">
                        <tr>
                                <th>Name</th>
                                <th>ProgressLabel</th>
				<th>Progress</th>
                        </tr>
#for @dwn in @postqueue:
                        <tr>
                                <td>@dwn.NZBName</td>
                                <td>@dwn.ProgressLabel</td>
                                <td width="50%">
<div class="progress progress-striped">
  <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: @dwn.StageProgress%">
    <span class="sr-only">@dwn.StageProgress % Complete</span>
  </div>
</div>
</td>
                        </tr>
#end
                        </table>
</div>

<br />
<div class="panel panel-success" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">History</h3>
                        </div>
                        <table class="table table-striped">
                        <tr>
                                <th>Name</th>
				<th>Dir</th>
				<th>Size</th>
                                <th>Status</th>
                        </tr>
#for @dwn in @history:
                        <tr>
                                <td>@dwn.NZBNicename</td>
                                <td>@dwn.DestDir</td>
				<td>@dwn.FileSizeLoFormated</td>
				<td><span style="color:#if (@dwn.status=="Success") green #else red #end">@dwn.status</span></td>
                        </tr>
#end
                        </table>
</div>
<br />
