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
	def get_file_baseinfo(self):
		return self.conp.get('file_base','name')
	def get_items(self):
		return self.conp.items('items')
	def get_bmc(self):
		host = self.conp.get('bmc','host')
		username = self.conp.get('bmc','username')
		password = self.conp.get('bmc','password')
		return [host,username,password]
		
if __name__ == '__main__':
	print 'This is ConfigParser.'
