import netmiko
from netmiko import ConnectHandler, file_transfer
import csv
import concurrent.futures as cf
import time
import pwinput

password = pwinput.pwinput(prompt='Enter password for the admin account: ', mask="*")

'''
Function to read device data from CSV file and
return device list data to main.
'''

def read_devices(devicefile):
    with open(devicefile) as dfh:
        csv_reader = csv.DictReader(dfh)
        for device in csv_reader:
            yield device
            
'''
Function to connect to device using netmiko
after connection sucessful, it calls function to
collect data
'''


def connect_device(device_data):
    try:
        rtr = ConnectHandler(device_type=device_data['dtype'],
                             ip=device_data['ip'],
                             username=device_data['user'],
                             password=password)
    except Exception as error:
        print(error)
    goget_data(rtr, device_data)
    
'''
Supplying commands to be collected and write
output to file.
'''


def goget_data(rtr, device_data):
    cmds = ['download image 10.250.210.192 update.xos']
    for cmd in cmds:
        update = rtr.send_command(cmd)
        print(update)
    rtr.disconnect()
    
'''
Main function
filename formatting
Multithreading code
'''

starttime = (time.time())

outputfildir = '.\OutputFiles'
timestr = time.strftime("%Y%m%d-%H%M")
device_data = read_devices('device-update-file.csv')
print(type(device_data))

'''
Creating threads to connect to devices simultaneously.
'''
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    ex.map(connect_device, device_data)

print('Done collecting data')
print('Total time:', time.time()-starttime)