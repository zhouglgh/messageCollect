'''
This is for linux.
modified by zhougl, at 2017-07-05
'''
import os
import common


class linux_process(object):
	def __init__(self,logger,dir_tools,os_arc):
		#log configuration
		self.logger = logger
		#This is for linux
		self.os_arc    = os_arc
		self.cmds    =   {}
		self.file4baseinfo=''
		#The directory to save log in
		self.dir_info = ''
		self.items    = []
		self.dir_tools=dir_tools
		self.common_exe = common.common_process(logger)
		self.do = {
			"cpu"   :self.do_cpu,
			"mem"   :self.do_mem,
			"nic"   :self.do_nic,
			#"net"   :self.do_net,
			"bios"  :self.do_bios,
			"disk"  :self.do_disk,
			"driver":self.do_driver,
			#"kernel":self.do_kernel,
			"system":self.do_system,
			"raid":self.do_raid,
			"bmc":self.do_bmc,
			#"config":self.do_config,
			#"fs"    :self.do_fs
		}
	#set filename saving base information
	def set_filename_4baseinfo(self,filename):
		self.file4baseinfo = filename
		basefile = self.dir_info+'/'+self.file4baseinfo
		if os.path.exists(basefile):
			with open(basefile,'w') as f:
				f.write('')
		self.file4baseinfo = basefile
			
	#mkdir to save the log files
	def set_dir_info(self,dir_info):
		if(not dir_info):
			self.dir_info = os.getcwd() + '/information'
		else:
			self.dir_info = dir_info
		if not os.path.exists(self.dir_info):
			os.mkdir(self.dir_info)
	#The file commands stored in
	def set_items(self,items):
		if(items):
			self.items = items
		else:
			self.logger.error("items is empty. Please check the configuration.")
			exit(-1)

	#set commands
	def set_commands(self,CMDS):
		if CMDS:
			self.cmds = CMDS
		else:
			self.logger.error("commands is empty. Please check the configuration.")
			exit(-1)
	#catch the info from the config file.
	def do_catch(self):
		for item in self.items:
			catagory = item[0]
			need_all = item[1]
			self.do[catagory](need_all)

	#get information for the type:cpu.
	def do_cpu(self,need_all):
		self.logger.info("catch cpu info...")
		self.do_normal('cpu',need_all)
	#get information for the type:mem.
	def do_mem(self,need_all):
		self.logger.info("catch memory info...")
		self.do_normal('mem',need_all)
	#get information for the type:bios.
	def do_bios(self,need_all):
		self.logger.info("catch bios info...")
		self.do_normal('bios',need_all)
	#get information for the type:disk.
	def do_disk(self,need_all):
		self.logger.info("catch disk info...")
		self.do_normal('disk',need_all)
	#get information for the type:driver.
	def do_driver(self,need_all):
		self.logger.info("catch driver info...")
		self.do_normal('driver',need_all)
	#get information for the type:nic.
	def do_nic(self,need_all):
		self.logger.info("catch nic info...")
		self.do_normal('nic',need_all)
	#get information for the type:raid.
	def do_raid(self,need_all):
		self.logger.info("catch raid info...")
		self.do_normal('raid',need_all)
	#get information for the type:bmc.
	def do_bmc(self,need_all):
		self.logger.info("catch bmc info...")
		dir_bmc = self.common_exe.check_dir(self.dir_info,'bmc')
		cmds_bmc = self.cmds['bmc']
		items = cmds_bmc['cmd_string'].items()
		self._do_dict(dir_bmc,items)
		if self.os_arc == 'x86_64':
			tool_path = self.dir_tools + '/' + cmds_bmc['tool_x64']
		elif os_arc == 'x86':
			tool_path = self.dir_tools + '/' + cmds_bmc['tool']
		else:
			self.logger.error("Do not support the cpu architecher.")
			exit()
		command = tool_path + ' ' + cmds_bmc['tool_cmd']
		filename = cmds_bmc['tool_file']
		file_path = dir_bmc + '/' + filename
		self._do_cmd_to_file(command,file_path)

	#get information for the type:system.
	def do_system(self,need_all):
		self.logger.info("catch system info...")
		name = 'system'
		#base info
		mycmds =self.cmds['system']
		mybaseinfo = mycmds.pop('baseinfo')
		self._do_baseinfo(mybaseinfo)
		if not need_all:
			return 0
		dir_system = self.common_exe.check_dir(self.dir_info,name)
		#extra info
		items = mycmds['save2dir']
		for key in items.keys():
			dir_each = key
			dir_item = self.common_exe.check_dir(dir_system,dir_each)
			for childitem in items[key]:
				res = self.common_exe.copy_files_to_dir(childitem,dir_item)
				if res == 0:
					self.logger.info("copy files %s successfully!"%childitem)
		items = mycmds['exe_and_save'].items()
		self._do_dict(dir_system,items)

	#get information for the type:*. Normal.
	def do_normal(self,type_normal,need_all):
		mycmds =self.cmds[type_normal]
		mybaseinfo = mycmds.pop('baseinfo')
		self._do_baseinfo(mybaseinfo)
		if not need_all:
			return 0
		items = mycmds.items()
		write_mode = 0
		for item in mycmds.items():
			file_tosave = self.dir_info + '/' + item[0]
			self._do_cmd_to_file(item[1],file_tosave,write_mode)

	#save results of the 'command' to the 'filename', append = 0 in default.
	def _do_cmd_to_file(self,command,file_path,append=0):
		if type(command) == type(''):
			self.common_exe.process_and_save(command,file_path,append)
		elif type(command) == type([]):
			append = 0
			for each_command in command:
				self.common_exe.process_and_save(each_command,file_path,append)
				append += 1
	def _do_dict(self,dir_private,items):
		for item in items:
			filename = item[0]
			command  = item[1]
			file_path = dir_private + '/' + filename
			append = 0
			self._do_cmd_to_file(command,file_path,append)
		
	#get information for baseinfo
	def _do_baseinfo(self,yourbaseinfo):
		title = yourbaseinfo.keys()[0]
		write_title = title+':\n'
		with open(self.file4baseinfo,'a') as f:
			f.write(write_title)
		for cmd in yourbaseinfo.values()[0]:
			self.common_exe.process_and_save(cmd,self.file4baseinfo,1)
			
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
		#mkdir for this operation
		dir_type = self.common_exe.check_dir(self.dir_info,type_info)
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

