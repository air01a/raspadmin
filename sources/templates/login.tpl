<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    	<link href="/static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection" />
	<link href="/static/css/login.css" type="text/css" rel="stylesheet" media="screen,projection" />
</head>
<body>
<h1 style="text-align:center;color: white;">RaspAdmin - Authentication</h1>
#if (@error)
	<div id="error" style="Width: 300px">
		Authentication : Invalid login/password
	</div><br />
#end

<form method="POST" action="" name="alphanum_authent" id="authentication" style="min-height: 250px">
	<p><br /><br /></p>
	<p><label for="user" style="font-size: 15px">User :&nbsp;</label><input type="text" name="alphanum_login" style="font-size: 15px">
	</p><br />
        <p>
	<label for="Password"  style="font-size: 15px">Password :</label>
	<input type="password" name="str_password" style="font-size: 15px"></p><br />
	<p style="text-align: center" >
		<input type="submit" name="alphanum_submit" value="Authenticate">
	</p>
	<input type="hidden" name="alphanum_token" value="@token">
</form>
</body>
</html>
