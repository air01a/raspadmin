raspadmin Installation guide
============================

1. Install debian package
-------------------------

sudo apt-get install python-pip python-dev

2. Install python packages
--------------------------

sudo pip install quik
sudo pip install netifaces
sudo pip install RPi.GPIO
sudo pip install metlog-psutils

3. Install the latest psutil
----------------------------

Download the last version of psutil available at the address https://code.google.com/p/psutil/ (currently, the version is 1.2.1)

wget --no-check-certificate https://code.google.com/p/psutil/psutil-1.2.1.tar.gz
tar xzf psutil-1.2.1.tar.gz

cd psutil-1.2.1

python setup.py build

sudo python setup.py install

4. Install the software
-----------------------
git clone https://github.com/air01a/rpi_admin.git

cd rpi_admin

sudo ./installer

5. Run it
---------
sudo service raspadmin start

By default, only the user pi is authorized to use the webinterface. You can configure this in the file /etc/raspadmin/raspadmin.conf

