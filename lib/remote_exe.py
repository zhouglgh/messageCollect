from common import common_process

class RemoteExec(common_process):
	def __init__(self,host,username.password):
		self.host = host
		self.username = username
		self.password = password
	def connect(self):
		connect = "ssh root@100.3.6.18"
		res = self.process_and_return(connect)

