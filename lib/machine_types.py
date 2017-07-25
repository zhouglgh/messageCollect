import platform
import common

class extract_info(object):
    def __init__(self,logger):
		machine=platform.uname()
		self.operate_system = machine[0]
		self.version        = machine[2]
		self.cputype        = machine[5]
		self.architecher    = machine[4]
		self.allof          = machine
		self.logger         = logger
		self.common_exe     = common.common_process(logger)
    def get_system(self):
		return self.operate_system
    def get_version(self):
		return self.version
    def get_cputype(self):
		return self.cputype
    def get_architecher(self):
		return self.architecher
    def get_ProductName(self):
		command = "dmidecode -t system|grep -i 'product name'|awk '{printf $3}'"
		res     = self.common_exe.process_and_return(command)
		if res[1] and not res[0]:
			self.logger.warning("get_ProductName error!")
		elif res[0]:
			return res[0]
		return ''
    def get_all(self):
		return self.allof
