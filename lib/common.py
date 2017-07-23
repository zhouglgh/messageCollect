'''
author: zhougl
time :  2017-01-12
modified: zhougl; time: 2017-07-03
	In 'process' function, add a path to 'cmd_str' for the program from other's.
'''
import json
import os
from subprocess import Popen, PIPE

class common_process(object):
	def __init__(self,logger):
		self.logger = logger

	'''
	process a command and return the result.
	And the result includes stdout and stderr.
	'''
	def process_and_return(self,cmd_str):
		self.logger.info("execute command %s"%cmd_str)
		res=Popen(cmd_str,shell=True,stdout=PIPE,stderr=PIPE)
		resstr = res.stdout.read()
		reserr = res.stderr.read()
		if reserr and not resstr:
			self.logger.warning("execute command %s failed, error message is %s."%(cmd_str,reserr))
		self.logger.info("execute command %s successfully!"%cmd_str)
		results = [resstr,reserr]
		return results

	'''
	save sting to file
	return the number of characters write in the file,
	or return 0 when it is failed.
	'''
	def save_results_formate(self,filename, appended, cmd_res):
		cmd_str = cmd_res[0]
		resstr  = cmd_res[1]
		reserr  = cmd_res[2]
		if resstr:
			write_content = cmd_str+ '\n{\n' + resstr + '\n}\n'
			#file opened in mode 'mode'
			mode = ''
			if(appended == 0):
				mode = 'w'
			else:
				mode = 'a'
			with open(filename,mode) as f:
				begin = f.tell()
				f.write(write_content)
				end = f.tell()
				return begin - end
		elif reserr:
			self.logger.error("error from %s"%reserr)
			return 0
		else:
			return 0
			
	'''
	run a command of linux
	parameter1: the command to execute
	parameter2: the file that store the result
	appended=0 file is in 'write' mode
	appended>=1 file is in 'append' mode
	'''
	def process_and_save(self,cmd_str,filename,appended):
		cmd_res = self.process_and_return(cmd_str)
		cmd_res.insert(0,cmd_str)
		res = self.save_results_formate(filename,appended,cmd_res)
		return res

		'''
		function check if the dir 'p2' is existed in 'p1'
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

	'''
	function check if the file 'p2' is existed in 'p1'
	dirname : p2
	directory: p1
	'''
	def check_file(self,directory,filename):
		if os.path.exists(directory):
			lst = os.listdir(directory)
		else:
			self.logger.error("There is no directory named %s"%directory);
			exit(-1)
		if not filename in lst:
			self.logger.warning("There is no file named %s."%filename)
			return 0
		return 1
	def copy_files_to_dir(self,source,destination):
		self.logger.info("copy files %s..."%source)
		if os.path.isdir(destination): 
			cmd_string = 'cp -rf %s %s'%(source,destination)
			res = self.process_and_return(cmd_string)
			if res[1]:
				return -1
			else:
				return 0
		else:
			self.logger.error("Please check if %s is a directory!"%destination)
			return -2

