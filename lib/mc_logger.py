#/usr/bin/python
# -*- coding:utf-8 -*-  
'''
author: zhougl
time:   2017.06.01 
modified at 2017.06.20 by zhougl.
'''
import logging
import sys
import os


'''
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s 用户输出的消息
'''


class mc_logger(object):
    def __init__(self,file_log):
		#define the log name
		if not 'app_name' in dir():
			app_name = 'mc_log'
		else:
			if not app_name:
				app_name = 'mc_log'

		#define the log formate
		if not 'formatter' in dir():
			formatter_str =  '%(asctime)s %(levelno)-8s: %(message)s'
		else:
			if not formatter_str:
				formatter_str = '%(asctime)s %(levelno)-8s: %(funcName)s :%(message)s'

		#define the log path
		if not file_log:
			print "the log file initial error！the process will exit！"
			exit(-1)
		base_dir = os.getcwd()
		if not 'log_file' in dir():
			log_file = file_log
		else:
			if not log_file:
				log_file = base_dir + '/runlog.txt'
		self.logger = logging.getLogger(app_name)
		formatter= logging.Formatter(formatter_str)
		file_handler = logging.FileHandler(log_file)
		file_handler.setFormatter(formatter)
		console_handler = logging.StreamHandler(sys.stdout)
		console_handler.formatter = formatter
		self.logger.addHandler(file_handler)
		self.logger.addHandler(console_handler)
		self.logger.setLevel(logging.INFO)
        #Logging有如下级别: DEBUG，INFO，WARNING，ERROR，CRITICAL
        #默认级别是WARNING，logging模块只会输出指定level以上的log。
if __name__ == '__main__':
	tmplog = mc_logger()
	tmplog.logger.setLevel(logging.INFO)
	tmplog.logger.info('This is mc_logger')      
                
