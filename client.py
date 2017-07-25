import paramiko


hostname = '100.3.6.18'
username = 'root'
password = 'superuser'


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname,username=username,password=password)
res = client.exec_command('k2_csr_access cpu read 0 0x1380')[1].read()
print res
