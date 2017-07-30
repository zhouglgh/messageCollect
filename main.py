import sys,os 
#The directory we works in
DIR_ORI = os.getcwd()
DIR_LIB = DIR_ORI + '/lib'
DIR_CONF = DIR_ORI + '/config'
#library to be used
sys.path.append(DIR_LIB)
#config dir to used
sys.path.append(DIR_CONF)

#the log system
from mc_logger import mc_logger
#the config system
from config import ConfInfo
#check machine type 
import machine_types as machp
#the command system
from data import CMDFILE
from enviroment import EnvSetting

FILE_CONF = DIR_CONF + '/mc_initial.conf'
FILE_LOG  = DIR_ORI  + '/runlog.txt'
DIR_TOOLS = DIR_ORI  + '/tools'
DIR_INFO_STORED = DIR_ORI + '/information'

#log define
mclog = mc_logger(FILE_LOG).logger


#get the machine type
machine = machp.extract_info(mclog)
OS_TYPE = machine.get_system()
OS_ARC  = machine.get_architecher()
PRODUCT_NAME= machine.get_ProductName()
mclog.info("os type is %s"%OS_TYPE)

#get the configuration
conf    = ConfInfo(FILE_CONF,mclog)
print conf.get_bmc()
mclog.info("read config file from %s"%FILE_CONF)


# if linux do relevant things
def do_linux():
	import get_info_from_linux as gl
	#set the directory the info store in 
	packages_info = conf.get_packages()
	#predoing prepare the enviroment
	envset = EnvSetting(mclog,packages_info)
	linux_exe = gl.linux_process(mclog,DIR_TOOLS,OS_ARC,envset)
	linux_exe.set_dir_info(DIR_INFO_STORED)
	#set the cmdfile to execute
	if( not CMDFILE):
		print "CMDILE is empty.exit."
		exit()
	linux_exe.set_commands(CMDFILE['linux'])
	#set file for base_info
	file4baseinfo = conf.get_file_baseinfo()
	items_info    = conf.get_items()
	bmc_info      = conf.get_bmc()
	linux_exe.set_filename_4baseinfo(file4baseinfo)
	linux_exe.set_ProductName(PRODUCT_NAME)
	linux_exe.set_bmc(bmc_info)
	linux_exe.set_items(items_info)
	#needed in the future
	#level = conf.get_level()

	linux_exe.do_catch()

#if windows do relevant things
def do_windows():
	print "do_windows"

#if nothing do nothing
def do_nothing():
	print "do_nothing"

if( OS_TYPE.lower() == 'linux'):
	do_linux()
elif(OS_TYPE.lower() == 'windows'):
	do_windows()
else:
	do_nothing()
