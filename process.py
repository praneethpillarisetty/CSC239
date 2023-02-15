import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from matplotlib import pyplot
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from random import randrange
import socket
import struct
import os
class Process_Graph():
	def __init__(self):
		self.x_data, self.y_data = [], []
		self.fig = plt.figure(figsize=(9, 6))
		self.axes = [0, 0]
		self.axes[0] = self.fig.add_subplot(1,2,(1,2))
		#plt.yticks(color='w')

	def get_user_name(self, inode):
		fp = open('/etc/passwd')
		lines = fp.readlines()
		username = ''
		for x in lines:
			if inode in x:
				values = x.split(':')
				username = values[0]
				fp.close()
				return username
		fp.close()
		return username

	def get_y_value(self):
		Proc_table_data = [["process_id", "sys mode utiliization", "user mode utilization", \
		"overall utilization", "virtual memory", "physical memory", "Program_Name", "username"]]
		total_utilization = 100
		fp = open('//proc/stat')
		lines = fp.readlines()
		result=[]
		for x in lines:
		    
		    if 'cpu ' in x:
		    	values = list(x.split(' '))
		    	user_utilization = int(values[2])
		    	cpu_utilization = int(values[4])
		    	idle_time = int(values[5])
		    	total_utilization = int(values[5]) + int(values[2]) + int(values[4])
		fp.close()
		plist = os.listdir("//proc")
		#numbered_program_list = [ x for x in plist if x.isdigit() ]
		for program in plist:
			try :
				proc_fd = open("//proc/" + program + "/stat")
				process_read = proc_fd.read().split()
				virtual_mem = float(process_read[22])
				physical_mem = float(process_read[23])
				user_mod = float(process_read[13])
				sys_mod = float(process_read[14])
				user_mod = round((user_mod / total_utilization)*100, 2)
				sys_mod = round((sys_mod / total_utilization)*100, 2)
				total = round(user_mod + sys_mod ,2)
				mem_fd = open("//proc/meminfo","r")
				mem_read = mem_fd.read().split()
				total_memory = float(mem_read[mem_read.index("MemTotal:")+1])
				virtual_mem = round(((virtual_mem * 100) / total_memory) / 1028 ,2)
				physical_mem = round(( physical_mem * 100) /total_memory , 2)
				s = process_read[1]
				proc_name = s[s.find('(')+1:s.find(')')]
				proc_status_fd = open("//proc/" + program + "/status")
				process_status_read = proc_status_fd.read().split()
				inode = process_read[process_status_read.index("Uid:")+1]
				user_name = self.get_user_name(inode)
				Proc_table_data += [[program, sys_mod, user_mod, total, virtual_mem, physical_mem, proc_name, user_name]]
				proc_fd.close()
				mem_fd.close()
				proc_status_fd.close()
				
			except:
				continue

		return Proc_table_data


	def update(self,frame):
	    self.x_data.append(datetime.now())
	    Net_table_data = self.get_y_value()
	    self.axes[0].clear()
	    self.axes[0].set_axis_off()
	    table = self.axes[0].table(cellText = Net_table_data, loc='center')
	    #table.clf()
	    table.scale(1, 2)
	    
	    
	    #line.set_data(x_data, y_data)
	    self.fig.gca().relim()
	    self.fig.gca().autoscale_view()
	    plt.autoscale(False)

	    #plt.tight_layout()
	    #return line,

	def display(self):
		animation_user = FuncAnimation(self.fig, self.update, interval=2000)
		#pyplot.show()

#A = Process_Graph()
#A.display()
#A.get_y_value()

