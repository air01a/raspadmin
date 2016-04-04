	
#if (@isFile)
 <button type="button" class="btn btn-default btn-lg" onClick="document.location='/bell/ACK'">
                  <span class="glyphicon glyphicon-ok-sign"></span>ACK 
        </button>

#else
	No File detected, no signal received.
#end
