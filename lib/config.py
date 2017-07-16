import ConfigParser
import logging
from mc_logger import mc_logger

class ConfInfo(object):
	def __init__(self,config_file,logger):
		if(config_file == ''):
			logger.error("config file is error:config_file=%s,"%(config_file));	
			exit(-1)
		self.conp = ConfigParser.SafeConfigParser(allow_no_value=True)
		self.conp.read(config_file)
		self.logger = logger
	def get_level(self):
		return self.conp.get('level','mes_lev')
	def get_hardware_info(self):
		return self.conp.items('hardware')
	def get_hardware_ifhave_info(self):
		return self.conp.items('hardware_ifhave')
	def get_OS_info(self):
		return self.conp.items('operating')
	def get_software_info(self):
		return self.conp.items('application')
	def get_file_baseinfo(self):
		return self.conp.items('baseinfo')
		
if __name__ == '__main__':
	print 'This is ConfigParser.'
