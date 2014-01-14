[global]

## Browsing/Identification ###
workgroup = @workgroup
server string = @serverstring
netbios name = @netbiosname
dns proxy = no

security = USER

#### Networking ####
bind interfaces only = no

### Access rights ###
create mask = 0660
directory mask = 0770
force create mode = 0660
force directory mode = 0770

#### Debugging/Accounting ####
log file = /var/log/samba/log.%m
max log size = 1000
syslog = 0
panic action = /usr/share/samba/panic-action %d
load printers = no

socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=8192 SO_SNDBUF=8192
usershare allow guests = no

force group = @nasgroup
encrypt passwords = true
passdb backend = tdbsam
obey pam restrictions = yes
unix password sync = no
passwd program = /usr/bin/passwd %u
passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
pam password change = yes
map to guest = bad user


