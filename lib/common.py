'''
author: zhougl
time :  2017-01-12
'''
import json
import os
from subprocess import Popen, PIPE

class common_process(object):
	def __init__(self,logger):
		self.logger = logger

	'''
	run a command of linux
	parameter1: the command to execute
	parameter2: the file that store the result
	'''
	def process(self,cmd_str,filename,appended):
		self.logger.info("[%s] will run"%cmd_str)
		res=Popen(cmd_str,shell=True,stdout=PIPE,stderr=PIPE)
		resstr = res.stdout.read()
		reserr = res.stderr.read()
		print resstr + ' --- ' + reserr
		if resstr:
			self.logger.info("[%s] complete successfully "%cmd_str)
			write_content = cmd_str+ '\n{\n' + resstr + '\n}\n'
			#file opened in mode 'mode'
			mode = ''
			if(appended == 0):
				mode = 'w'
			else:
				mode = 'a'
			with open(filename,mode) as f:
				f.write(write_content)
		elif reserr:
			self.logger.error("error from %s"%reserr)

		'''
		function check if the file 'p2' is existed in 'p1'
		dirname : p2
		directory: p1
		'''
	def check_dir(self,directory,dirname):
		if os.path.exists(directory):
			lst = os.listdir(directory)
		else:
			self.logger.error("There is no directory named %s"%directory);
			exit(-1)
		newdir = directory+'/'+dirname
		if not dirname in lst:
			os.mkdir(newdir)
			self.logger.info("mkdir %s"%newdir)
		return newdir

