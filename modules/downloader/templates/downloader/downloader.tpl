<script src="/static/app/downloader.js"></script>
<div ng-controller="downloadCtrl" id="mainCtrl">
<br /><div class="panel panel-primary" style="width: 80%;margin: auto">
		        <div class="panel-heading">
			          <h3 class="panel-title">Downloader</h3>
        		</div>
		 <div class="panel-body">

                <div class="container-fluid">
                        <div class="row-fluid">
                                <div class="span12" style="margin: auto; text-align: center">
					<form method="POST" action="/downloader">
						<p style="text-align: left">
							Links to download :
						</p>	
						<p>
						<textarea rows="4" cols="100" id="ta_to_download" name="str_download"></textarea></p>
						<input type="hidden" name="alphanum_token" value="@token">
						<p><input type="submit" class="btn btn-info btn-lg" id="uploadbutton"></p>
					</form>
                                </div>
			</div>
		</div>
	</div>
</div><br />

<div class="panel panel-danger wordbreak" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Current Download</h3>
                        </div>
			<div class="panel-body" style="magin:auto;text-align:center;">
                        	<table class="table table-striped">
                        	<tr>
                                	<th style="text-align: center">File</th>
					<th style="text-align: center">State</th>
                               		 <th style="text-align: center">Downloaded</th>
                       		 </tr>
                       	 	<tbody ng-repeat="dwn in result | filter : currentFilter">
					<tr>
					  	<td>{{dwn.filename}}</td>
                        	        	<td>{{dwn.state}}</td>
                        	        	<td><span style="color: green">{{dwn.progression}} </span>/ <span style="color: red">{{dwn.length}} <span style="color: green">({{dwn.bandwidth}})</span>
							<div class="progress progress-striped" ng-if="dwn.state=='d'">
								<div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" style="width: {{dwn.percent}}%">
    									<span class="sr-only">{{dwn.percent}} % Complete</span>
  								</div>
							</div>
						</td>
					<tr>
						<td colspan="3" style="text-align: right; color:#E6E6E6">{{dwn.url}}</td>
                	        	</tr>
				</tbody>
            	            </table>
			</div>
</div>
<br />
<div class="panel panel-info" style="width: 80%;margin: auto;">
                        <div class="panel-heading">
                                  <h3 class="panel-title">History</h3>
                        </div>
                 <div class="panel-body" style="magin:auto;text-align:center;">
			<table class="table table-striped">
                        <tr>
				<th style="text-align: center">Name</th>
                                <th  style="text-align: center">State</th>
                                <th  style="text-align: center">Size</th>
                        </tr>
                        <tbody ng-repeat="dwn in result | filter : historyFilter">
                        	<tr>	
			        	<td>{{dwn.filename}}</td>
                               		 <td> <span style="color: red" ng-if="dwn.state=='e'">Failed</span>
					      <span style="color: green" ng-if="dwn.state!='e'">Ok</span>
					 </td>
                                	<td>{{dwn.progression}} </span>/ <span style="color: red">{{dwn.length}}</td>
				</tr>
				<tr>
					<td colspan="3" style="text-align: right; color:#E6E6E6">{{dwn.url}}</td>
                        	</tr>
			</tbody>
                        </table>
		
		</div>
</div>
<br />
