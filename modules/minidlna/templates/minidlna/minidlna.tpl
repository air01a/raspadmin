<br />
#if (@status!=0)
					<form method="POST" >
						<input type="hidden"  name="alphanum_action" value="1">
						<input type="hidden"  name="alphanum_servicestart" value="1">
						<input type="hidden" name="alphanum_token" value="@token">
					<INPUT type="Submit" value="Start Service" class="btn btn-success btn-lg"  >
					</form>
#else
					<form method="POST" >
                                                <input type="hidden"  name="alphanum_action" value="1"><input type="hidden"  name="alphanum_servicereload" value="1"><input type="hidden" name="alphanum_token" value="@token"><INPUT type="Submit" value="Reload Service" class="btn btn-success btn-lg"  > </form><form method="POST" >
                                                <input type="hidden"  name="alphanum_action" value="1">
                                                <input type="hidden"  name="alphanum_servicestop" value="1">
                                                <input type="hidden" name="alphanum_token" value="@token">
                                        <INPUT type="Submit" value="Stop Service" class="btn btn-danger btn-lg"  >
                                        </form>
#end
<br /><br />
<!-- Modal -->
<div class="modal fade" id="deleteshare" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel" style="color:red;">Delete share</h4>
      </div>
      <div class="modal-body">
        <div id="deleteshare">
        </div>
		Are you sure ?
      </div>
      <div class="modal-footer">
        <form method="POST" action="delete"><input id="hiddendeleteshare" type="hidden" name="base64_path" value=""><input type="hidden" name="alphanum_token" value="@token"><input id="hiddendeletetype" type="hidden" name="alphanum_type" value="">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button><button type="submit" class="btn btn-primary">Delete It</button>
        </form>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal  -->


<!-- Modal -->
<div class="modal fade" id="dirbrowser" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel" style="color:blue;"> Select the directory to share :</h4>
      </div>
      <div class="modal-body">
        <div id="dynbrowser">
        </div>

      </div>
      <div class="modal-footer">
        <form method="POST" action="modify"><input id="hiddenshare" type="hidden" name="base64_path" value=""><input type="hidden" name="alphanum_token" value="@token">
	<label for="alphanum_type">Type of share :</label><br />
	<p style="text-align: center"><SELECT name="alphanum_type" style="margin: 0px">
		<OPTION value="music">Music</OPTION>
		<OPTION value="photo">Photo</OPTION>
		<OPTION value="video">Video</OPTION>
		<OPTION value="all">All</OPTION>
	</SELECT></p><br /><br /><br />
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button><button type="submit" class="btn btn-primary">Share It</button>
        </form>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal  -->



<script>
function deletepath(path,type){
	$("#hiddendeleteshare").val(path)
	$("#hiddendeletetype").val(type)
	$("#deleteshare").modal('show')
}

 function decode_base64(s) {
    var e={},i,k,v=[],r='',w=String.fromCharCode;
    var n=[[65,91],[97,123],[48,58],[43,44],[47,48]];

    for(z in n){for(i=n[z][0];i<n[z][1];i++){v.push(w(i));}}
    for(i=0;i<64;i++){e[v[i]]=i;}

    for(i=0;i<s.length;i+=72){
    var b=0,c,x,l=0,o=s.substring(i,i+72);
         for(x=0;x<o.length;x++){
                c=e[o.charAt(x)];b=(b<<6)+c;l+=6;
                while(l>=8){r+=w((b>>>(l-=8))%256);}
         }
    }
    return r;
    }

function browse(dir,name) {
        result=$.get( "browse?base64_file="+dir,  function(data) {

                html='<div class="panel panel-default">Current Directory: '+decode_base64(dir)+'</div>';


                data.forEach(function(entry) {
                        html=html+'<a href="#" onClick="javascript:browse('+"'"+entry.link+"','"+entry.pathname+"'"+')">'+entry.pathname+'</a><br/>'
                });
                $('#hiddenshare').val(dir)
                $("#dynbrowser").html(html);
        },"json");

}


function browsedir(){
        $("#dirbrowser").modal('show')
        browse('','');
}


</script>

<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">DLNA Share</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
			<table class="table">
			<thead>
			<tr>
				<th style="text-align: center">Path</th>
				<th style="text-align: center">Type</th>
				<th style="text-align: center">Action</th>
			</tr>
			</thead>
			<tbody>
#for @share in @shares:
			<tr>
				<td>@share.path</td>
				<td>@share.type</td>
				<td><button class="btn btn-danger btn-lg" data-toggle="modal"  style="margin: auto" onclick="javascript:deletepath('@share.b64path','@share.type')">Delete</button>				</td>
			</tr>
#end
			</tbody>
			</table>
			<br />
			<button class="btn btn-success btn-lg" data-toggle="modal"  style="margin: auto" onClick="browsedir()">Add share </button>
		</div>
</div>
