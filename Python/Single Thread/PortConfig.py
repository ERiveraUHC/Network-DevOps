from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import time
import datetime
import sys
import getpass

buffer = []
password= getpass.getpass(prompt='Enter Password for admin:')
timestr = time.strftime("%Y%m%d-%H%M")
print('Enter IP of Devices, type DONE when complete')

while True:
    IP = sys.stdin.readline().rstrip('\n')
    if (IP == "DONE"):
        break
    else:
        buffer.append(IP)

print("This is the list of Devices that will be backed up:")
print(buffer)

print("Begin Connection")

for device in buffer:
    print ('\n  '+ device.strip() + ' \n' )
    RTR = {
    'ip':   device,
    'username': 'admin',
    'password': password,
    'device_type': 'cisco',
    }

    try:
        net_connect = ConnectHandler(**RTR)
    except NetMikoTimeoutException:
        print ('Device not reachable.')
        continue
    except AuthenticationException:
        print ('Authentication Failure.')
        continue
    except SSHException:
        print ('Make sure SSH is enabled in device.')
        continue

    print ('Initiating Show Loop Config')
    output = net_connect.send_command(' sh int', delay_factor = 20)

    SAVE_FILE = open("Loop_"+device.strip() +'_'+ str(timestr) + ".txt", 'w+')
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print ('Finished Loop Config Info')
