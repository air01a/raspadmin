<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta charset="utf-8">
		<title>RPi Administrator</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">

		<link href="/static/css/bootstrap.css" rel="stylesheet">
		<link rel="stylesheet" href="/static/css/bootstrap-toggle-buttons.css">
		<link href="/static/css/style.css" rel="stylesheet">
		<link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
		<link href="/static/css/bootstrapstyle.css" rel="stylesheet">
                <link href="/static/css/font-awesome.css" rel="stylesheet">
        <script src="/static/js/jquery-1.10.2.min.js"></script>

		<!-- HTML5 Support for IE -->
		<!--[if lt IE 9]>
		<script src="/static/js/html5shim.js"></script>
		<![endif]-->

		<!-- Favicon -->
		<link rel="shortcut icon" href="/static/img/favicon/favicon.ico">
#if ("@includefile"!="None")
        #include("@includefile")
#end
<style>
@font-face {
  font-family: 'Glyphicons Halflings';
  src: url('/static/font/glyphicons-halflings-regular.eot');
  src: url('/static/font/glyphicons-halflings-regular.eot?#iefix') format('embedded-opentype'), url('/static/font/glyphicons-halflings-regular.woff') format('woff'), url('/static/font/glyphicons-halflings-regular.ttf') format('truetype'), url('/static/font/glyphicons-halflings-regular.svg#glyphicons-halflingsregular') format('svg');
}
</style>
	</head>
	<body>
		<div class="navbar navbar-fixed-top navbar-inverse">
			<div class="navbar-inner">
				<div class="container">
					<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse"><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></a>
					<a href="index.php" class="brand" style="font-weight: 600;"><img src="/static/images/sprite.png" alt="rpi"/>&nbsp;<span class="bold">Raspberry Pi</span> Admin</a>
					</div>
				</div>
			</div>
		</div>

		<!-- Main content starts -->
#if (!@NONAV)
		<div class="content">
			<!-- Sidebar -->
			<div class="sidebar">
				<div class="sidebar-dropdown"><a href="#">Navigation</a></div>
				<div class="sidebar-inner">
					<!--- Sidebar navigation -->
					<!-- If the main navigation has sub navigation, then add the class "has_submenu" to "li" of main navigation. -->
					<ul class="navi">
						<!-- Use the class nred, ngreen, nblue, nlightblue, nviolet or norange to add background color. You need to use this in <li> tag. -->
						#for @menu in @menulist:
							<li class="nred"><a href="/@menu.link/"><i class="icon-desktop"></i> @menu.name</a></li>
						#end
							<li class="nred"><a href="/?num_logout=1"><i class="icon-desktop"></i>Logout</a></li>
					</ul>
				</div>
			</div>
			<!-- Sidebar ends -->
<div class="mainbar">
#else
<div class="mainbar" style="margin-left: 0px;">
#end

<br><h1>@pagetitle</h1>
<hr />
#if (@error)
<br /><div class="alert alert-danger">Error @error: @errorstr</div>
#else
        #if (@action)
                <br /><div class="alert alert-success">@action</div>
        #end
#end

