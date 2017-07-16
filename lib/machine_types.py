import platform

class extract_info(object):
    def __init__(self):
		machine=platform.uname()
		self.operate_system = machine[0]
		self.version        = machine[2]
		self.cputype        = machine[5]
		self.architecher    = machine[4]
		self.allof          = machine
    def get_system(self):
		return self.operate_system
    def get_version(self):
		return self.version
    def get_cputype(self):
		return self.cputype
    def get_architecher(self):
		return self.architecher
    def get_all(self):
		return self.allof
