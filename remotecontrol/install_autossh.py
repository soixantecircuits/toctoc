
import os
import re
from socket import gethostname

remote_username = 'kan'
remote_hostname = 'ks3326340.kimsufi.com'

# connect to remote
remote = remote_username + '@' + remote_hostname
os.system('ssh-copy-id ' + remote)

# find an unused port
port = 60000
os.system('scp ' + remote + ':.ssh/config .')
configfile =  open("config","a+")
configtext = configfile.read()
regex = re.compile(r'6\d\d\d\d')
numbers = sorted(regex.findall(configtext))
if (len(numbers) > 0):
 port = int(numbers[-1]) + 3
print "Using tunnel port " + str(port)

# Modify files with this new port
os.system("cp autossh_tunnel autossh_tunnel_temp")
os.system("sed -i 's/60000/" + str(port) + "/' autossh_tunnel_temp")
os.system("sed -i 's/kan/" + remote_username + "/' autossh_tunnel_temp")
os.system("sed -i 's/ks3326340.kimsufi.com/" + remote_hostname + "/' autossh_tunnel_temp")
os.system("sed -i 's/minad/" + os.getlogin() + "/' autossh_tunnel_temp")
configfile.write("\nHost " + gethostname())
configfile.write("\n    HostName localhost")
configfile.write("\n    Port " + str(port))
configfile.write("\n    User " + os.getlogin())
configfile.close()

# Send the config file back to remote
os.system('scp config ' + remote + ':.ssh/')

# install autossh daemon
os.system('sudo apt-get install autossh openssh-server')
os.system('sudo mv autossh_tunnel_temp /etc/init.d/autossh_tunnel')
os.system('sudo update-rc.d autossh_tunnel defaults')
os.system('sudo service autossh_tunnel start')

# connect from remote to local
os.system('ssh -t -t ' + remote + ' cat .ssh/id_rsa.pub >> ~/.ssh/authorized_keys')
#os.system('ssh ' + remote + ' ssh ' + gethostname())
