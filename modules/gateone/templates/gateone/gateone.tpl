<script type="text/javascript">
window.onload = function() {
	jsonauth=@jsonauth
	GateOne.init({url: "https://@servername:@port/",
		      auth: jsonauth,
		      autoConnectURL: "ssh://pi@192.168.0.20:22",
                      fillContainer:true,
                      colors:'gnome-terminal'});
	}
</script>
<div id="gateone_container" style="position: relative; width: 80em; height: 40em;">
        <div id="gateone"></div>
    </div>
