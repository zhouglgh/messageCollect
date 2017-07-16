from common import common_process

'''
catch the system info, besides
base info
extra info
'''
class SysMessage():
	def __init__(self,logger,cmds,file4baseinfo,dir4system):
		self.name          = "systeminfo"
		self.cmds          = cmds
		self.logger        = logger
		self.file4baseinfo = file4baseinfo
		if self.logger:
			self.process = common_process(self.logger)
		else:
			print "error in SysMessage.__init__, logger should not be null!"
	def _get_baseinfo_from_command(self,cmd):
		return self.process.process_and_return(cmd)
	def catch_fileinfo(self):
		self.logger.info("fileinfo running...")
		items = self.cmds['save2dir'].items()
		cmds = []
		for item in items:
			item[0]
			cmdstr='cp ' +item[1]+' ' +dirs
			cmds.append()
		
	def catch_baseinfo(self):
		self.logger.info("baseinfo running...")
		commands = self.cmds['baseinfo']['cmds']
		title    = ITEM%self.name
		content  = ''
		for command in commands:
			res = _get_baseinfo_from_command(self,command)
			#0 represent stdout, and 1 represent stderr
			if res[0]:
				res_format = FORMAT_RES_A%res[0]
			elif res[1]:
				res_format = FORMAT_RES_A%res[1]
			content += res_format
		with open(self.file4baseinfo,'a') as f:
			f.write(title+content)
				
