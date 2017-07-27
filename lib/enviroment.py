import os

class EnvSetting(object):
	def __init__(self,logger,packages_path):
		self.logger = logger
		self.packages_path = packages_path

	#returning 3 is successed
	#returning 2 is failed at 3 step
	#returning 1 is failed at 2 step
	#returning 0 is failed at 1 step
	def do_test_paramiko(self):
		paramiko_path = self.packages_path['paramiko']
		pycrypto_path = self.packages_path['pycrypto']
		ecdsa         = self.packages_path['ecdsa']
		try:
			import paramiko
		except ImportError:
			res=0
			curdir = os.getcwd()
			if os.path.isdir(ecdsa_path):
				os.chdir(ecdsa_path)
				if os.path.exists('setup.py'):
					if os.system("python setup.py install") == 0:
						res+=1
					else:
						self.logger.warning("error in install 'ecdsa'")
			if os.path.isdir(pycrypto_path):
				os.chdir(pycrypto_path)
				if os.path.exists('setup.py'):
					if os.system("python setup.py install") == 0:
						res+=1
					else:
						self.logger.warning("error in install 'pycrypto'")
			if os.path.isdir(paramiko_path):
				os.chdir(paramiko_path)
				if os.path.exists('setup.py'):
					if os.system("python setup.py install") == 0:
							res+=1
					else:
						self.logger.warning("error in install 'pycrypto' or 'ecdsa'")
			os.chdir(curdir)
			return res
	#for all file in cmd_path exec 'chmod +x  %s'
	def do_chmod_x(self,cmd_path):
		command = "files=$(find %s -type f);for file in $files;do chmod +x $file;done"%cmd_path
		res = os.system(command)
		if res == 0:
			self.logger.info("chmod %s successed"%cmd_path)
		else:
			self.logger.warning("chmod %s failed"%cmd_path)

