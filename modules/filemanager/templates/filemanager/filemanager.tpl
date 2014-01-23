<div class="alert alert-danger" id="dynerror"></div>
<div class="alert alert-success" id="dynaction"></div>
<script>
  $('#dynaction').hide()
  $('#dynerror').hide()
</script>
<br />

<br />
<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">File Manager</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
<div id="DynTable">
</div>

                </div>
</div>

<!-- Modal -->
<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Deletion</h4>
      </div>
      <div class="modal-body">
	Your ask to delete the file/directory <span id="deleteModalFile" style="color: red"></span><br />
       	Once you've deleted a file, you cannot get it back. Are you really sure of what you're doing ?
      </div>
      <div class="modal-footer">
	<input type="hidden" id="deleteModalFileToDelete" value="" >
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" onClick="confirm_delete()">Yes, delete !</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->


<!-- Modal -->
<div class="modal fade" id="actionModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Wait for action to complete</h4>
      </div>
      <div class="modal-body">
	<div id="actionresult2"></div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal" id="actionclose">Close</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->



<script>
global_filter=[[2,0],[1,0]]
global_path=""
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

function load_dir(path) 
{
        $.post( "filemanager/", { "alphanum_token": "@token","alphanum_action":'listdir','base64_dir':path }, function( data ) {

                if (data.error==0) {
			global_path=path
			files=data.data
			html='<table id="myTable" class="tablesorter"><thead><tr>    <th></th><th>File</th><th>Type</th> <th>Size</th><th style="text-align:center;width: 300px">Action</th></tr></thead><tbody>'
			subdir=""
			for(var i= 0; i < files.length; i++)
			{	
				if (files[i].name=='..')
					subdir=files[i].link

				html+="<tr><td width='16px'>"
				if (files[i].type=="dir"){
					html+="<img width='14px' src='/static/images/directory.png'></td><td>"
					html+="<a href='javascript:void(0);' onclick='load_dir("+'"'+files[i].link+'"'+")'>"+files[i].name+"</a>"
				}
				else {
					html+="<img width='14px' src='/static/images/file.png'></td><td>"
					html+=files[i].name
				}
				
				html+="</td>  <td>"+files[i].type+"</td> <td>"+files[i].size+"</td> <td style='text-align:center'> "
				if (files[i].name!='..') {
					if (files[i].type=="file")
						html+="<a href='/filemanager/download?base64_file="+files[i].link+"' target='_blank'><span class='badge'>Download</span></a>&nbsp;"

					html+="<a href='javascript:void(0);' onClick='copy_file("+'"'+files[i].link+'","'+files[i].name+'"'+")'><span class='badge'>Copy</span></a> "
					html+="<span class='badge'>Rename</span> "
					html+="<a href='javascript:void(0);' onClick='delete_file("+'"'+files[i].link+'","'+files[i].name+'"'+")'><span class='badge alert-danger'>Delete</span></a> "
				}
				html+="</td></tr>"
			}
			if (subdir!="")
				header='<div class="panel panel-default"><a href="javascript:void(0);" onclick="load_dir('+"'"+subdir+"'"+')"><img src="/static/images/subfolder.png" width="18px"></a> Current Directory: '+decode_base64(path)+' </div>'
			else
				header=""
			html+="</tbody></table>"
			$("#DynTable").html(header+html)
			//DOc : http://mottie.github.io/tablesorter/docs/
		        $("#myTable").tablesorter({
        		        theme : 'blue',
		                sortList: global_filter,
                		headers: {
                			0: {
        	                		sorter: false
                			},
        	        		4: {
                  			      	sorter: false
	                   		}
        	        	}
		        });
		        $("#myTable").on("sortEnd", function(event) {
                		global_filter=event.target.config.sortList;
		        });

                }
                else {

                }

        }, "json");

}

$(document).ready(function() 
    {
	$("#newdirbutton").click(new_dir)
	$("#copybutton").click(copy_file_action)
	$("#movebutton").click(move_file_action)
	$("#resetbutton").click(function(event){
		$("#dynselect")
			.find('option')
			.remove()
			.end()

	});
	load_dir('')
    } 
); 

function show_result(action)
{
	$('#dynaction').html(action)
	$('#dynaction').show()
	$('#dynaction').delay(5000).fadeOut()

}

function show_error(error)
{
	$('#dynerror').html(error)
        $('#dynerror').show()
        $('#dynerror').delay(5000).fadeOut()

}


function send_command(vars, action,msg,callback)
{
	vars['alphanum_token']='@token'
	vars['alphanum_action']=action

	$.post("/filemanager",vars,function(data){
                if (data.error==0){
                        show_result(msg)
                        load_dir(global_path)
			if (callback!='undefined')
				callback()
                }
                else {
                        show_error(data.errorstr+"("+data.error+")")
			result=false
		}
        },'json');
}

function confirm_delete()
{
	path=$("#deleteModalFileToDelete").val()
	$('#deleteModal').modal('hide')
	$("#deleteModalFileToDelete").val("")

	send_command({'base64_path':path},'delete','File deleted')
}	

function new_dir()
{
	if (!validate())
		return false
	send_command({'base64_path':global_path,'filename_dir':$("#newdir").val()},'createdir','Directory created',new_dir_end)
	
}

function new_dir_end()
{
       $("#newdir").val("")
       $("#validateerror").html("<span style='color:Green'>Directory created</span>")
	$("#validateerror").show()
       $("#validateerror").delay(5000).fadeOut()
	

}

function delete_file(path,filename)
{
	$("#deleteModal").modal()
	$("#deleteModalFile").html(filename)
	$("#deleteModalFileToDelete").val(path)
	
	
}

function copy_file(path,filename)
{
	if ($("#"+"dynselect option[value='"+path+"']").length > 0)
		return false

	$("#dynselect").append($('<option>',{value:path,text:decode_base64(path)}));
}

function copy_mv_action(action)
{
	$("#actionclose").hide()
	$("#actionModal").modal()
//	if (action=='copy')
//		$("#actionresult").html("<b>Copying files in directory "+decode_base64(global_path)+"</b><br /><br />")
//	else
//		$("#actionresult").html("<b>Moving files in directory "+decode_base64(global_path)+"</b><br /><br />")
	

        $("#dynselect"+" option:selected").map(function() {
                $("#actionresult2").html(action+" "+(this.text)+" : in progress<br />")
		$("#actionresult").html(action+" "+(this.text)+" : in progress <br/>"+$("#actionresult").html())
		vars={'alphanum_token':'@token','alphanum_action':action,'base64_src':this.value,'base64_dst':global_path}
		
		$.ajax({type: 'POST',async:true,url:'/filemanager',data:vars,success:function(data){
			if (data.error==0) {
				$("#actionresult").html(data.data.action+" "+data.data.src+" to "+data.data.dst+" [<span style='color:green'>OK</span>]<br />"+$("#actionresult").html())
			} else {
				$("#actionresult").html(data.action+" "+data.data.src+" to "+data.data.dst+"[<span style='color:red'>KO</span>] ("+data.errorstr+"("+data.error+")<br />"+$("#actionresult").html())
			}
		},dataType:'json'});
                this.remove();
        });
//	load_dir(global_path)
	$("#actionresult2").html($("#actionresult2").html()+"<br />See history to view when operation are done")
	$("#actionclose").show()


}

function copy_file_action()
{
        $('#actionModal').on('shown.bs.modal',copy_action_trig)
        $("#actionModal").modal()

}

function copy_action_trig()
{
	copy_mv_action('copy')
}


function move_action_trig()
{
	copy_mv_action('move')
}

function move_file_action()
{
	$('#actionModal').on('shown.bs.modal',move_action_trig)
        $("#actionModal").modal()
}

function validate()
{
	permit="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
	field=$("#newdir").val()
	
	for(var i=0;i<field.length;i++) {
		if (permit.indexOf(field[i])<0) {
			$("#validateerror").html("<span style='color:red'>Error, char "+field[i]+" not valid</span>")
		        $("#validateerror").show()

			return false	
		}

	}
	$("#validateerror").html("")
	
	return true

}

</script>
<br />
<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Operations</h3>
                        </div>
                 	<div class="panel-body" style="margin: auto;text-align:center;"><center>
			<table border="0" style="text-align: center">
                        <tr>
                                <td><input type="text" id="newdir" onChange="validate()"></td>
                                <td><button class="btn btn-danger btn-lg" id="newdirbutton" >Create Dir</button></td>
                        </tr>
			<tr>
				<td colspan="2"><div id="validateerror"></div>
				</td>

                        <tr>
				<td>    
					<SELECT MULTIPLE size="8" style="min-width: 300px" id="dynselect">
					</SELECT>
		
				</td>
				<td><button class="btn btn-info btn-lg" id="copybutton" >Copy</button>&nbsp;&nbsp;
				    <button class="btn btn-danger btn-lg" id="movebutton">Move</button><br /><br />
				    <button class="btn btn-success btn-lg" id="resetbutton">Reset</button>
				</td>
			</tr>
			</table>
			</center>
                </div>
		
</div>
<br />

<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">History</h3>
                        </div>
                        <div class="panel-body" style="margin: auto;text-align:center;">
				<div id="actionresult"></div>
			</div>
</div>

