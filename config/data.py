#command need to be executed

CMDFILE={
"linux" : 
    {
	 "cpu":
        {
			"baseinfo" : {"cpu":["lscpu"]},
			"cpu_dmidecode.txt":"dmidecode -t processor",
			"cpuinfo.txt":"cat /proc/cpuinfo"
        },
	 "mem":
		{
			 "baseinfo" : {"memory":["cat /proc/meminfo"]},
			 "memory_dmidecode.txt":"dmidecode -t memory",
			 "memory_free.txt":"free"
		},
	 "bios":
		{
             "baseinfo":{"bios":["dmidecode -t bios"]}
		},
	 "disk":
		{
			"baseinfo" : {"disk":["lsblk","lsscsi","df -h","mount"]},
			"disklist.txt":"smartctl --scan",
			 "fdisk_l.txt":"fdisk -l",
			 "parted_disk.txt":"a=`smartctl --scan|awk '{print $1}'`;for b in $a;do parted $b print;done",
			 "sys_block.txt":"ls -l /sys/block/sd*",
			"devSmart.txt":"a=`ls /dev/sd[a-z]`;for b in $a;do smartctl -a $b;done;"
		},
	 "driver":
		{
			 "baseinfo":{"modle":["lsmod"]},
			 "modinfo.txt":"a=$(lsmod|awk '{print $1}'|sed '1d');for b in $a;do modinfo $b;done 2> /dev/null"
		},
	 "nic"   :
		{
			"baseinfo":{"nic":["ifconfig","lspci |grep net"]},
			"ethtool.txt":"a=`ip a|grep mtu|awk -F':' '{print $2}'|grep -v 'lo'`; for b in $a;do echo -e 'ethool '$b '{\n';ethtool $b;echo -e '\n}';done"
		},
     "bmc"   :
        {
			"tool"     : "BMCtool/lxRW/lxRW",
			"tool_x64" : "BMCtool/lxRW/lxRW_x64",
			"tool_cmd" : "p2a dump 1e600000 190000",
			"tool_file" : "bmcreg.txt",
        	"cmd_string":
				{
            		"chassis_power_status.txt"      :     "ipmitool chassis power status        ",
					"chassis_status.txt"      :     "ipmitool chassis status              ",  
					"bmc_customid.txt"      :     "ipmitool raw 0x3a 0x9a               ", 
					"power_status.txt"      :     "ipmitool power status                ", 
					"fru.txt"      :     "ipmitool fru list                    ", 
					"mc_info.txt"      :     "ipmitool mc info                     ", 
					"mc_getenables.txt"      :     "ipmitool mc getenables               ", 
					"mc_guid.txt"      :     "ipmitool mc guid                     ", 
					"mc_selftest.txt"      :     "ipmitool mc selftest                 ", 
					"mc_watchdog_get.txt"      :     "ipmitool mc watchdog get             ", 
					"sensor_list_all.txt"      :     "ipmitool sensor list all             ", 
					"sensor.txt"      :     "ipmitool sensor                      ", 
					"sdr_elist_all.txt"      :     "ipmitool sdr elist all               ", 
					"sdr_list_all.txt"      :     "ipmitool sdr list all                ", 
					"sdr.txt"      :     "ipmitool sdr                         ", 
					"sel_elist.txt"      :     "ipmitool sel elist                   ", 
					"sel_list.txt"      :     "ipmitool sel list                    ", 
					"sel.txt"      :     "ipmitool sel                         ", 
					"sel.bin"      :     "ipmitool sel writeraw                ", 
					"bmctime.txt"      :     ["ipmitool sel time get","ipmitool raw 0x0a 0x48"], 
					"lan_print_1.txt"      :     "ipmitool lan print 1                 ", 
					"lan_print_8.txt"      :     "ipmitool lan print 8                 ", 
					"lan_print.txt"      :     "ipmitool lan print                   ", 
					"channel_getaccess_1.txt"      :     "ipmitool channel getaccess 1         ", 
					"channel_getaccess_8.txt"      :     "ipmitool channel getaccess 8         ", 
					"channel_getciphers_ipmi.txt"      :     ["ipmitool channel getciphers ipmi 1", "ipmitool channel getciphers ipmi 8","ipmitool channel getciphers ipmi"],
					"channel_getciphers_sol.txt"       :     ["ipmitool channel getciphers sol 1", "ipmitool channel getciphers sol 8","ipmitool channel getciphers sol"],
					"channel_info.txt"          :    "ipmitool channel info                  ", 
					"firewall_info_1.txt"          :    "ipmitool firewall info 1               ", 
					"firewall_info_8.txt"          :    "ipmitool firewall info 8               ", 
					"mestatus"          :    ["ipmitool -b 0x06 -t 0x2c raw 0x06 0x04 ","ipmitool -b 0x00 -t 0x2c raw 0x06 0x04 "],
					"medeviceinfo.txt"          :    ["ipmitool -b 0x06 -t 0x2c raw 0x06 0x01 ","ipmitool -b 0x00 -t 0x2c raw 0x06 0x01 "],
					"session_info_active.txt"          :    "ipmitool session info active           ", 
					"session_info_all.txt"          :    "ipmitool session info all              ", 
					"sol_info.txt"          :    ["ipmitool sol info","ipmitool sol info 0","ipmitool sol info 1","ipmitool sol info 2","ipmitool sol info 3","ipmitool sol info 4","ipmitool sol info 5","ipmitool sol info 6","ipmitool sol info 7"], 
					"sol_payload_status.txt"          :    "ipmitool sol payload status            ", 
					"user_list_1.txt"          :    "ipmitool user list 1                   ", 
					"user_list_8.txt"          :    "ipmitool user list 8                   ", 
					"8480fpga.txt"          :    "ipmitool raw 0x3a 0xe5                 ", 
					"8460cpld.txt"          :    "ipmitool raw 0x2e 0x10               ",	
					"psucount.txt"          :    "ipmitool raw 0x3a 0x72                 ", 
					"psu0.txt"          :    "ipmitool raw 0x3a 0x71 0x00            ", 
					"psu1.txt"          :    "ipmitool raw 0x3a 0x71 0x01            ", 
					"psu2.txt"          :    "ipmitool raw 0x3a 0x71 0x02            ", 
					"psu3.txt"          :    "ipmitool raw 0x3a 0x71 0x03            ", 
        	},
        },
	 "raid" :
		{
			"baseinfo":{"raid":["lspci -v |grep RAID -A1"]}		
		},
	 "system" :		
		{
			"baseinfo":
				{
					"system":["hostname","dmidecode -t baseboard|grep 'Base Board Information' -A12","cat /proc/sys/kernel/osrelease","if [ -f /etc/os-release ];then cat /etc/os-release;fi"]
				},
			"save2dir":
				{
				"log":["/var/log/mcelog*","/var/log/syslog*","/var/log/boot*","/var/log/dmesg*","/root/.bash_hstory","/var/log/maillog*","/var/log/message*","/var/log/cron*","/var/log/secure*"],
				"proc":["/proc/interrupts","/proc/filesystems","/proc/self/maps","/proc/self/smaps","/proc/self/numa_maps","/proc/iomap","/proc/ioports","/proc/swaps","/proc/slabinfo","/proc/slabinfo","/proc/locks","/proc/modules","/proc/mounts","/proc/version","/proc/stat","/proc/schedstat","/proc/zoneinfo","/proc/config.gz","/proc/kallsyms"," /proc/mtrr","/proc/vmstat","/proc/buddyinfo","/proc/cmdline","/proc/devices","/proc/diskstats","/proc/iomem","/proc/keys","/proc/key-users","/proc/dma"],
				"etc":["/etc/syslog.conf","/etc/resolv.conf","/etc/nsswitch.conf","/etc/hosts","/etc/services","/etc/network/interfaces","/etc/udev/rules.d/70-persistent-net.rules","/etc/exports","/etc/fstab","/etc/sysctl.conf","/etc/inittab","/etc/ntp.conf","/etc/ntp/step-tickers","/etc/ntp/ntpservers","/etc/yp.conf","/proc/kallsyms"],
				"config":["/boot/config*"],
				"grub":["/boot/grub/device.map","/boot/grub/menu.lst"],
				"grub2":["/boot/grub2/device.map","/boot/grub2/menu.lst"],
				},
			 "exe_and_save":
				{
					"dmesg.txt":["dmesg"],
					"dumpi_list.txt":["du -ah /var/crash"],
					"others.txt":["lsof","last","ulimit -a","ipcs -a","ipcs -l","sysctl -a","uptime","iostat","top -n 1","vmstat","service --status-all","uname -a","ps auwx","hostid","rpm -qa","printenv","cat /etc/issue","lsb_release -a","chkconfig --list"],
				}
		},
	 "sysconfig" : {}
    },
"windows" :
{}
}
