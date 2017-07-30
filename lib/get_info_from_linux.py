'''
This is for linux.
modified by zhougl, at 2017-07-05
'''
import os
import common
import threading


class linux_process(object):
	def __init__(self,logger,dir_tools,os_arc,env_set):
		#log configuration
		self.logger  = logger
		self.envset  = env_set
		#This is for linux
		self.os_arc  = os_arc
		self.cmds    =   {}
		self.file4baseinfo=''
		#The directory to save log in
		self.dir_info     = ''
		self.ProductName  = ''
		self.bmc          = ''
		self.items        = []
		self.dir_tools    = dir_tools
		self.common_exe   = common.common_process(logger)
		self.threads      = []
		#install the needed packages and change the mode of executable file
		self.do = {
			"cpu"   :self.do_cpu,
			"mem"   :self.do_mem,
			"nic"   :self.do_nic,
			"bios"  :self.do_bios,
			"disk"  :self.do_disk,
			"driver":self.do_driver,
			"system":self.do_system,
			"raid":self.do_raid,
			"bmc":self.do_bmc,
		}
	#set ProductName
	def set_ProductName(self,name):
		self.ProductName = name
	#set BMC
	def set_bmc(self,bmc):
		self.bmc =  bmc
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
		for thread in self.threads:	
			if thread.isAlive():
				self.logger.info("%s is running, Please wait."%(thread.name))
			thread.join()

	#get information for the type:cpu.
	def do_cpu(self,need_all):
		self.logger.info("catch cpu info...")
		self.do_normal('cpu',need_all)
		if 'k1-910' == self.ProductName.lower():
			if self.bmc:
				thread_do_register = threading.Thread(target=self._do_register,name='do_register')
				self.threads.append(thread_do_register)
				thread_do_register.start()
	def _do_register(self):
		hostname = self.bmc[0]
		user     = self.bmc[1]
		password = self.bmc[2]
		res = self.envset.do_test_paramiko()
		if res != 3:
			self.logger.warning("Installing package 'paramiko' error, can not get the cpu register information!")
			return -1
		else:
			import paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=hostname,username=user,password=password)
		res = client.exec_command("k2_csr_access cpu read 0 0x1380")[1].read()
		filename = 'cpu_register.txt'
		filepath = self.dir_info + '/' + filename
		self.common_exe.save_results_formate(filepath,0,['k2_csr_access',res,''])
		file_all_cpu = self.dir_info + '/cpu_all_csr.txt'
		command = "file=/log/cpu_all_csr;if [ -f $file ];then cat $file;else dump_cpu_csr&&cat $file;fi"
		res = client.exec_command(command,timeout=300)[1].read()
		self.common_exe.save_results_formate(file_all_cpu,0,['dump_cpu_csr',res,''])
		client.close()
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
		mycmds =self.cmds['raid']
		mybaseinfo = mycmds.pop('baseinfo')
		self._do_baseinfo(mybaseinfo)
		types_raid  = mycmds.pop('type')
		tool_megacli = mycmds.pop('tool_megacli')
		if self.os_arc.find('64') != -1:
			tool_megacli = self.dir_tools + '/' + tool_megacli["64"]
		else:
			tool_megacli = self.dir_tools + '/' + tool_megacli["32"]
		cmd_get_raidtype = "lspci |grep -i raid"	
		type_raid        = self.common_exe.process_and_return(cmd_get_raidtype)
		type_ofraid      = ''
		if type_raid[0]:
			for t in types_raid:
				if type_raid[0].find(t) != -1:
					type_ofraid = t
					break
		elif type_raid[1]:
			self.logger.warning("Can not get the type of raid")
			return
		else:
			self.logger.warning("There is no raid or no 'lspci'")
			return
		if not type_ofraid:
			return
		str_to_func = {
			"3108":self.do_raid_3108,
			"2208":self.do_raid_2208,
			"2308":self.do_raid_2308,
			#"3008":self.do_raid_3008,
			"Adaptec" :self.do_raid_adaptec,
		}
		if type_ofraid == '2208':
			cmd_string = mycmds[mycmds[type_ofraid]]
		else:
			cmd_string = mycmds[type_ofraid]
		dir_raid = self.common_exe.check_dir(self.dir_info,'raid%s'%(type_ofraid))
		self.envset.do_chmod_x(self.dir_tools)
		str_to_func[type_ofraid](dir_raid,cmd_string,tool_megacli)
		
	#get raid info for 3108
	def do_raid_3108(self,dir_raid,cmd_string,tool_megacli):
		if self.os_arc.find('64') != -1:
			tool_3108 = cmd_string['tool']['64']
		else:
			tool_3108 = cmd_string['tool']['32']
		tool_3108 = self.dir_tools + '/' + tool_3108
		commands = cmd_string['cmds']
		for cmd2file in commands['tool_3108'].items():
			command = tool_3108 + ' ' + cmd2file[1]
			filename=cmd2file[0]
			file_path = dir_raid + '/' + filename
			self._do_cmd_to_file(command,file_path)
		for cmd2file in commands['tool_megacli'].items():
			command = tool_megacli + ' ' + cmd2file[1]
			filename=cmd2file[0]
			file_path = dir_raid + '/' + filename
			self._do_cmd_to_file(command,file_path)

	#get raid info for 2208
	def do_raid_2208(self,dir_raid,cmd_string,tool_megacli):
		self.do_raid_3108(dir_raid,cmd_string,tool_megacli)
	#get raid info for 2308
	def do_raid_2308(self,dir_raid,cmd_string,tool_megacli):
		tool_ircu =  cmd_string['tool']['sas2ircu']
		tool_ircu = self.dir_tools + '/' + tool_ircu
		tool_flash=  cmd_string['tool']['sas2flash']
		tool_flash= self.dir_tools + '/' + tool_flash
		commands  = cmd_string['cmds']
		commands_prepare = commands['prepare']
		commands_doing   = commands['doing']
		commands_after   = commands['after']
		#prepare	
		tool_prepare = commands_prepare['tool']
		tool_prepare = dir_raid + '/' + tool_prepare
		param_prepare= commands_prepare['param']
		command_prepare=tool_prepare + ' ' + param_prepare
		times        = self.common_exe.process_and_retrun(command_prepare)
		#doing
		cmds_doing = commands_doing['cmds']
		filename   = cmds_doing.items()[0][0]
		file_path  = dir_raid + '/' + filename
		cmds_notreal= cmds_doing[filname]
		cmds_real = []
		i=0
		times = int(times)
		append = -1
		while i < times:
			for cmd_notreal in cmds_notreal:
				cmd_real.append(cmd_notreal%i)
			append+=1
			cmd_and_para = tool_ircu + ' ' + cmd_real[0]
			self.common_exe._do_cmd_to_file(cmd_and_para,filepath,append)
			append+=1
			cmd_and_para = tool_flash + ' ' + cmd_real[1]
			self.common_exe._do_cmd_to_file(cmd_and_para,filepath,append)
			cmd_and_para = tool_ircu + ' ' + cmd_real[2]
			self.common_exe._do_cmd_to_file(cmd_and_para,filepath,append)
			cmd_and_para = tool_flash + ' ' + cmd_real[3]
			self.common_exe._do_cmd_to_file(cmd_and_para,filepath,append)
			
		
	#get raid info for adaptec
	def do_raid_adaptec(self,dir_raid,cmd_string,tool_megacli):
		if self.os_arc.find('64') != -1:
			tool_adaptec = cmd_string['tool']['64']
		else:
			tool_adaptec = cmd_string['tool']['32']
		tool_adaptec = self.dir_tools + '/' + tool_adaptec
		cmds = cmd_string['cmds']
		command = tool_adaptec + ' ' + cmds['param']
		res = self.common_exe.process_and_return(command)
		if res[0].find("successfully") == -1:
			self.logger.warning("Please check the command if it is suiltable!")
			return
		command = cmds['cmd']
		command = command%dir_raid
		res = self.common_exe.process_and_return(command)
		if not res[0] and not res[1]:
			self.logger.info("raid info collect successfully")
	#get information for the type:bmc.
	def do_bmc(self,need_all):
		self.logger.info("catch bmc info...")
		dir_bmc = self.common_exe.check_dir(self.dir_info,'bmc')
		cmds_bmc = self.cmds['bmc']
		items = cmds_bmc['cmd_string'].items()
		self._do_dict(dir_bmc,items)
		if self.os_arc == 'x86_64':
			tool_path = self.dir_tools + '/' + cmds_bmc['tool_x64']
		elif self.os_arc == 'x86':
			tool_path = self.dir_tools + '/' + cmds_bmc['tool']
		else:
			self.logger.warning("Do not support the cpu architecher.")
			self.logger.warning("So can not get the bmc info.")
			return 'error'
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
