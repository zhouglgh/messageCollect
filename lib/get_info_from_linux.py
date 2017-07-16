'''
'This is for linux.
'''
import os
import common


class linux_process(object):
	def __init__(self,logger,dir_tools):
		#log configuration
		self.logger = logger
		#This is for linux
		self.OS_TYPE = 'linux'
		self.CMDS=''
		#The directory to save log in
		self.DIR_INFO = ''
		self.DIR_TOOLS=dir_tools
		self.common_exe = common.common_process(logger)
	#mkdir to save the log files
	def set_dir_info(self,dir_info):
		if(not dir_info):
			self.DIR_INFO = getcwd() + '/information'
		else:
			self.DIR_INFO = dir_info
		if not os.path.exists(self.DIR_INFO):
			os.mkdir(self.DIR_INFO)
	#The file commands stored in
	def set_data_cmd(self,cmds):
		if(cmds):
			self.CMDS= cmds
		else:
			self.logger.error("cmds is empty. Please check the configuration.")
			return -1;
	#get information for the type:raid.
	def get_info_raid(self,dir_tools):
		print 'get_info_raid'
	#get information for the type:type_info.
	def get_info_simple(self,type_info):
		print type_info
		cmdstring = self.CMDS[self.OS_TYPE]
		#check if there is the 'type_info' key
		str_type_info = ''.join(type_info)
		if (not cmdstring.has_key(type_info)):
			self.logger.error("There is no type named %s"%str_type_info)
			return -1;
		self.logger.info("catch info from %s."%str_type_info)
		#mkir for this operation
		dir_type = self.common_exe.check_dir(self.DIR_INFO,type_info)
		what2do = cmdstring[type_info]
		sav = what2do.keys()
		cmd = what2do.values()
		lengths =len(sav)
		lengthc =len(cmd)
		if(lengths != lengthc):
			self.logger.error("extract file from cmdfile error.len(%s)!=len(%s)"%(' '.join(sav),' '.join(cmd)))
			return -1;
		i=0;
		while i < lengths:
			out_ = dir_type + '/' + sav[i];
			cmd_ = cmd[i];
			appended=0
			if (type(cmd_) == type('')):
				self.common_exe.process(cmd_,out_,appended)
			elif (type(cmd_) == type([])):
				for cmd__ in cmd_:
					self.common_exe.process(cmd__,out_,appended)
					appended+=1;
			else:
				self.logger.error("cmd translate error!Please check!")
				exit(-1)
			i+=1;
		#process i times
		return i

