<br />

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Manage user</h4>
      </div>
      <div class="modal-body">
        <form id="alphanum_adduser" method="POST" action="/nasusers/manageuser">
	<div id="dynamicform">
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

<script>
function addUser() {
	var champ = $('<input>');
	champ.attr('type', 'text');
	champ.attr('name', 'test');
	$('#dynamicform').html('<label id="alphanum_lbluser" for="user">User</label>'+
                '<input id="alphanum_user" type="text" name="alphanum_user" value=""><br /><br />'+
                '<label id="alphanum_lblcomment" for="comment">Comment</label>'+
                '<input id="str_comment" type="text" name="str_comment"><br /><br />'+
                '<label id="alphanum_lblpassword" for="password">Password</label>'+
                '<input id="str_password" type="password" name="str_password">'+
		'<input id="alphanum_action" type="hidden" name="alphanum_action" value="add">'+
		'<input id="alphanum_token" type="hidden" name="alphanum_token" value="@token">')
	$("#myModal").modal('show')
}

function changePassword(id,name){
        $('#dynamicform').html('<label id="alphanum_lbluser" for="user">User '+name+'</label>'+
                '<label id="alphanum_lblpassword" for="password">Password</label>'+
                '<input id="str_password" type="password" name="str_password">'+
		'<input id="alphanum_action" type="hidden" name="alphanum_action" value="change">'+
		'<input id="alphanum_token" type="hidden" name="alphanum_token" value="@token">'+
		'<input id="alphanum_name" type="hidden" name="alphanum_name" value="'+name+'">');
        $("#myModal").modal('show')
}

function deleteUser(id,name){
        $('#dynamicform').html('The user '+name+' will be deleted, please confirm<input id="alphanum_name" type="hidden" name="alphanum_name" value="'+name+'">'+
		'<input id="alphanum_action" type="hidden" name="alphanum_action" value="delete">'+
                '<input id="alphanum_token" type="hidden" name="alphanum_token" value="@token">'+
                '<input id="alphanum_name" type="hidden" name="alphanum_name" value="'+name+'">');
        $("#myModal").modal('show')
}


</script>
&nbsp;<button class="btn btn-primary btn-lg" data-toggle="modal" onClick="addUser()">
Add user
</button>
&nbsp;
<br />

<div class="panel panel-info" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Users</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
		<table class="table" >
		    <thead>
   			 <tr>
       				<th width="30px" style="text-align: center">Id</th>
			        <th width="30px" style="text-align: center">Name</th>
				<th width="30px" style="text-align: center">Comment</th>
			        <th width="60px" style="text-align: center">Action</th>
    			</tr>
		    </thead>
		   <tbody>
		   #for @user in @users:
			<tr style="text-align:center">
			        <td>@user.pw_uid</td>
			        <td>@user.pw_name</td>
			        <td>@user.pw_gecos</td>
				<td style="text-align: center;margin: auto">
					<button class="btn btn-success btn-lg" data-toggle="modal"  onClick="changePassword(@user.pw_uid,'@user.pw_name');">
						Change
					</button>

					<button class="btn btn-danger btn-lg" data-toggle="modal" onClick="deleteUser(@user.pw_uid,'@user.pw_name');">
						Delete
					</button>
				</td>
			</tr>
		   #end
		  </tbody>
               </table>

		</div>
</div>
<br />


