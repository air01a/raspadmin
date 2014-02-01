<script type="text/javascript">
window.onload = function() {
	jsonauth=@jsonauth
	GateOne.init({url: "https://@servername:@port/",
		      auth: jsonauth,
		      autoConnectURL: "ssh://pi\@@autoconnect:22",
                      fillContainer:true,
		      theme: 'white',
                      colors:'gnome-terminal'});
	}
</script>
<div id="gateone_container" style="position: relative; width: 80em; height: 40em;">
        <div id="gateone"></div>
    </div>
