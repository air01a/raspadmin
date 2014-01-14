<br />
<div class="panel panel-primary" style="width: 80%;margin: auto">
                        <div class="panel-heading">
                                  <h3 class="panel-title">Modify share</h3>
                        </div>
                 <div class="panel-body" style="margin: auto;text-align:center;">
			<div class="panel panel-default">Current Directory: @pathtxt</div>
			<form action="" method="POST" id="shareform">
			<label for="modify" style="text-align: right">Share name : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="text" name="alphanum_name" value="@name"></p><br />
			<label for="modify" style="text-align: right">Comment : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="text" name="str_comment" value="@comment"></p><br />
                        <label for="modify" style="text-align: right">Read only : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="checkbox" name="alphanum_readonly" @readonly></p><br />
			<label for="modify" style="text-align: right">Public : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="checkbox" name="alphanum_public" @public></p><br />
			<label for="modify" style="text-align: right">Writable : </label> <p style="text-align: left">&nbsp;&nbsp;&nbsp;<input type="checkbox" name="alphanum_writable" @writable></p><br />
			<label for="read"  style="text-align: right">Reader list :</label><br />
			<p style="text-align: center"><table border="0" style="margin: auto;">
			<tr>
				<td style="width: 30%">
					<SELECT multiple name="alphanum_notselected" id="reader_ns">
					#for @user in @alluserread:
						<OPTION>@user</OPTION>
					#end
					</SELECT>
				</td>
				<td>
					<button id="reader_add" class="btn btn-info btn-lg" data-toggle="modal" style="width: 120px">Add User</button><br />
					<button id="reader_remove" class="btn btn-danger btn-lg" data-toggle="modal" style="width: 120px" >Remove User</button>
				</td>
				<td style="width:30%">
		                        <SELECT multiple name="alphanum_reader" id="reader_se">
					#for @user in @validusers:
                                                <OPTION>@user</OPTION>
                                        #end
		                        </SELECT><br >
				</td>
			</tr>
			</table></p>
			<label for="read" style="text-align: right">Write list :</label><br />
                        <p style="text-align: center"><table border="0" style="margin: auto;">
                        <tr>
                                <td style="width: 30%">
                                        <SELECT multiple name="alphanum_notselected" id="writer_ns">
					#for @user in @alluserwrite:
                                                <OPTION>@user</OPTION>
                                        #end
                                        </SELECT>
                                </td>
                                <td>
                                        <button id="writer_add" class="btn btn-info btn-lg" data-toggle="modal" style="width: 120px">Add User</button><br />
                                        <button id="writer_remove" class="btn btn-danger btn-lg" data-toggle="modal" style="width: 120px" >Remove User</button>
                                </td>
                                <td style="width:30%">
                                        <SELECT multiple name="alphanum_reader" id="writer_se">
					#for @user in @writelist:
                                                <OPTION>@user</OPTION>
                                        #end
                                        </SELECT><br >
                                </td>
                        </tr>
                        </table></p>


			<br /><br />
			<input type="hidden" name="alphanum_token" value="@token">
			<input type="hidden" name="base64_path" value="@path">
			<input type="hidden" name="str_reader" value="" id="str_reader">
			<input type="hidden" name="str_writer" value="" id="str_writer">
			<input type="hidden" name="alphanum_action" value="modifiy">
			<button id="submitform" class="btn btn-info btn-lg" data-toggle="modal" style="width: 120px">Submit</button><br />
			</form>	
		</div>
</div>
<br />

<script>

  $("#reader_add").click(function() {
  	$("#reader_ns"+" option:selected").map(function() { 
			toprint=this.text
			$("#reader_se").append($('<option>',{ value:this.value,text:toprint }));
		    this.remove();	     
	});
  });

  $("#reader_remove").click(function() {
          $("#reader_se"+" option:selected").map(function() {
                     $("#reader_ns").append($("<option>",{ value:this.value,text:this.text }));
                     this.remove();
        });
  });

  $("#writer_add").click(function() {
        $("#writer_ns"+" option:selected").map(function() {
                        toprint=this.text
                        $("#writer_se").append($('<option>',{ value:this.value,text:toprint }));
                    this.remove();
        });
  });

  $("#writer_remove").click(function() {
          $("#writer_se"+" option:selected").map(function() {
                     $("#writer_ns").append($("<option>",{ value:this.value,text:this.text }));
                     this.remove();
        });
  });


  $("#submitform").click(function() {
	user=""
	$("#reader_se"+" option").map(function(){
		if (this.text!="")
			user+=this.text+","
	});
	$("#str_reader").val(user)

	user=""
       $("#writer_se"+" option").map(function(){
		if (this.text!="")
                	user+=this.text+","
        });
        $("#str_writer").val(user)


	$("#shareform").submit()
   });

</script>
