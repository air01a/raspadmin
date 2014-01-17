raspadmin Installation guide
============================


1. Clone the repository
-----------------------
git clone https://github.com/air01a/raspadmin.git


2. Install the software
-----------------------
cd raspadmin
sudo ./installer


Please enter the default home directory for user [ /opt/raspadmin ] :
Please enter the port [ 443 ] :
Use SSL [y/n] :
Do you have your own certificate [y/n] :

If you decide to use your own certificate, the installer will ask you the path to the certificate and the key. Otherwise, it will generates you a self-signed certificate, that will be used for the SSL server. In this case, your browser will warn you each time your try to connect...

If you choose this option, you will be ask few questions :

Use SSL [y/n] :y
Do you have your own certificate [y/n] :n
Generating RSA private key, 1024 bit long modulus
......++++++
....++++++
e is 65537 (0x10001)
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:     _Yourcountry_
State or Province Name (full name) [Some-State]:  _Your state_
Locality Name (eg, city) []:   _Your city_
Organization Name (eg, company) [Internet Widgits Pty Ltd]:  _Your organisation (what you want)_
Organizational Unit Name (eg, section) []: _not needed_
Common Name (e.g. server FQDN or YOUR name) []: _The URL or IP of your raspberry pi_
Email Address []: _Nothing_

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:   _LEAVE IT BLANK_
An optional company name []:  _LEAVE IT BLANK_
Signature ok
subject=/C=FR/ST=Nord/L=Lille/O=ParlonsSecurite/CN=www.parlonssecurite.com
Getting Private key


3. Install modules
------------------

cd modules
./installer

The installer will display the list of the available module and will ask you if you want to install them. Please visit the modules wikipage to understand what are the roles of the different modules, and theirs requirements...

4. Run it
---------
sudo service raspadmin start

By default, only the user pi is authorized to use the webinterface. You can configure this in the file /etc/raspadmin/raspadmin.conf

