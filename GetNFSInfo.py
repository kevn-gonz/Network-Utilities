import paramiko
import csv
import os
import sys
from getpass import getpass
from datetime import datetime

# Getting the list of servers to which the script will connect from the servers.txt file.
with open(os.path.join(sys.path[0], "servers.txt"), "r") as f: 
    hosts = [line.strip() for line in f]
f.close()
hosts.sort()

# SSH Session information
port = 22
username = input("Username: ")
password = getpass()

# Command to get the mounted nfs drives
#command = "df -hT | grep \"data\" | awk '{ print $1\",\"$7\",\"$3\",\"$4 }'"
command = "df -hT | awk '{ print $1\",\"$7\",\"$3\",\"$4 }'"
# Header for the CSV file
header = ['Hostname', 'Filesystem', 'Mounted on', 'Size', 'Used']
client = None

now = datetime.now()
# Variable used to name the resultant csv file
dt_string = now.strftime("%d.%m.%Y.%H.%M.%S")

with open(os.path.join(sys.path[0],f'SERVERS_Storage_{dt_string}.csv'), 'a', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer = csv.writer(f)
    #Connecting to the list of hosts, one by one
    for host in hosts:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password)

            # Running the command
            stdin, stdout, stderr = client.exec_command(command)
            lines = stdout.readlines()
        
        # If the connection fails to the host (not reachable or invalid credentials or something)
        except:
            failure=host+",ERR"+",ERR"+",ERR"+",ERR"
            writer.writerow(failure.split(","))
        
        # If the connection works fine, proceed to log the nfs drives information in the csv file
        else:
            converted_list = []
            for element in lines:
                converted_list.append(element.strip())

            for i in converted_list:
                i=host+","+i
                writer.writerow(i.split(","))
        
        # Finally, no matter what happens, close the SSH connection.
        finally:
            if client:
                client.close()

# Close the csv file
f.close()