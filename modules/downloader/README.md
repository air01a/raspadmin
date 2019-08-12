To use with alldebrid, you must create a token related to an application name. Use your webbrowser and go to :
https://api.alldebrid.com/pin/get?agent=mySoft

Replace mySoft by the name you want to use (ex raspadmin). Get the check & pin code.

Then, go to the alldebrid interface and reference the pin code :
https://alldebrid.fr/pin/

Then, go to the following link to get the token :
https://api.alldebrid.com/pin/check?agent=mySoft&check=KEY&pin=PIN


Put the agent name you used and the token in the config file
