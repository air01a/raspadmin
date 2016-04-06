#if (@isOpen)
Service is Running <br />
#else
Service is Not Running <br />
<a href="/bell/RLD">
<button type="button" class="btn btn-success btn-lg" data-dismiss="modal">Start</button>
</a>
<br />
#end	
#if (@isFile)
 <button type="button" class="btn btn-default btn-lg" onClick="document.location='/bell/ACK'">
                  <span class="glyphicon glyphicon-ok-sign"></span>ACK 
        </button>

#else
	No File detected, no signal received.
#end
