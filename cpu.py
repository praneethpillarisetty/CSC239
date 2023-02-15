import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange



class Cpu_Graph():
	def __init__(self):
		self.x_data, self.y_data = [], []
		self.fig = plt.figure(figsize=(9, 6))
		self.axes = [0, 0, 0, 0, 0, 0 ]
		self.axes[3] = self.fig.add_subplot(3,2,(1,3))
		self.axes[4] = self.fig.add_subplot(3,2,5)
		#self.axes[5] = self.fig.add_subplot(3,2,5)
		self.axes[0] = self.fig.add_subplot(3,2,2)
		self.axes[1] = self.fig.add_subplot(3,2,4)
		self.axes[2] = self.fig.add_subplot(3,2,6)
		self.user, self.cpu, self.idle =[],[],[]
		


	def get_y_value(self):
		current_user_value = 0
		current_cpu_value = 0
		current_idle_value = 0
		total_cpu_prev = 0
		table_cpu_values = 0
		table_user_mode = 0
		table_cpu_mode = 0
		table_idle_mode = 0
		table_total_values = 0
		table_current_user_value = 0
		table_current_cpu_value = 0
		table_current_idle_value = 0
		context_switches = 0
		total_table = [['cpu', 'User_time', 'Cpu_time', 'Idle_time', 'Total%']]
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
		    	current_user_value = round(abs(((current_user_value - user_utilization)/(total_utilization))*100), 3)
		    	current_cpu_value = round(abs(((current_cpu_value - cpu_utilization) / (total_utilization))*100), 3)
		    	current_idle_value = round(abs(((current_idle_value - idle_time) / (total_utilization))*100), 3)

		    if 'cpu' in x and 'cpu ' not in x:
		    	values = list(x.split(' '))
		    	table_cpu_values = values[0]
		    	table_user_mode = int(values[1])
		    	table_cpu_mode = int(values[3])
		    	table_idle_mode = int(values[4])
		    	table_total_values = int(values[4]) + int(values[1]) + int(values[3])
		    	actual_total = round(table_total_values/total_utilization * 100,3)
		    	table_current_user_value = round(abs(((table_current_user_value - table_user_mode)/(table_total_values))*actual_total),3)
		    	table_current_cpu_value = round(abs(((table_current_cpu_value - table_cpu_mode) / (table_total_values))*actual_total),3)
		    	table_current_idle_value = round(abs(((table_current_idle_value - table_idle_mode) / (table_total_values))*actual_total),3)
		    	total_table += [[ table_cpu_values, table_current_user_value, table_current_cpu_value, table_current_idle_value, \
		    	actual_total]]
		    if 'ctxt' in x:
		    	values = list(x.split(' '))
		    	context_switches = values[1]

		    if 'intr' in x:
		    	values = list(x.split(' '))
		    	interupts = values[1]
		    	 		

		total_table += [[ 'Total', round(current_user_value, 3), round(current_cpu_value, 3), round(current_idle_value, 3), 100]]
		fp.close()
		return current_user_value, current_cpu_value, current_idle_value, total_table, context_switches, interupts


	def update(self,frame):
	    x_value = datetime.now()
	    self.x_data.append(x_value)
	    user_new, cpu_new, idle_new, table_data, context_switches, interupts = self.get_y_value()
	    
	    self.user.append(user_new)
	    self.cpu.append(cpu_new)
	    self.idle.append(idle_new)
	    
	    self.axes[0].plot(self.x_data, self.user, color="red")
	    self.axes[0].title.set_text("User mode utilization")
	    #self.axes[0].set_xlabel("time", fontsize = 15)
	    #self.axes[0].set_ylabel("user-time", fontsize = 15)
	    #self.axes[0].set_ylim([0, 100])
	    #self.axes[0].set_yticks([user_new])
	    plt.setp(self.axes[0].get_xticklabels(), visible=False)
	    plt.setp(self.axes[0].get_yticklabels(), visible=False)
	    self.axes[0].tick_params(axis='both', which='both', length=0)
	    self.axes[0].legend(labels = [user_new] )
	    
	    

	    self.axes[1].plot(self.x_data, self.cpu, color="gray")
	    self.axes[1].title.set_text("cpu mode utilization")
	    #self.axes[1].set_xlabel("time", fontsize = 15)
	    #self.axes[1].set_ylabel("cpu-time", fontsize = 15)
	    #self.axes[1].set_ylim([0, 100])
	    #self.axes[1].set_yticks([cpu_new])
	    plt.setp(self.axes[1].get_xticklabels(), visible=False)
	    plt.setp(self.axes[1].get_yticklabels(), visible=False)
	    self.axes[1].tick_params(axis='both', which='both', length=0)
	    self.axes[1].legend(labels = [cpu_new] )


	    self.axes[2].plot(self.x_data, self.idle, color="blue")
	    self.axes[2].title.set_text("idle mode utilization")
	    #self.axes[2].set_xlabel("time", fontsize = 15)
	    #self.axes[2].set_ylabel("idle-time", fontsize = 15)
	    #self.axes[2].set_ylim([0, 100])
	    #self.axes[2].set_yticks([idle_new])
	    plt.setp(self.axes[2].get_xticklabels(), visible=False)
	    plt.setp(self.axes[2].get_yticklabels(), visible=False)
	    self.axes[2].tick_params(axis='both', which='both', length=0)
	    self.axes[2].legend(labels = [idle_new] )
	    
	    self.axes[3].clear()
	    table1 = self.axes[3].table(cellText = table_data, loc='center')
	    self.axes[3].set_axis_off()
	    #table.auto_set_font_size(False)
	    table1.scale(1, 3)

	    self.axes[4].clear()
	    table2 = self.axes[4].table(cellText = [[ 'context_switches', 'interupts' ],[ context_switches, interupts ]], loc='center')
	    self.axes[4].set_axis_off()
	    #table2.auto_set_font_size(False)
	    table2.scale(0.7, 3)
	    


	    
	    #plt.subplots_adjust(wspace= 0.25, hspace= 0.25)
	    #line.set_data(x_data, y_data)
	    self.fig.gca().relim()
	    self.fig.gca().autoscale_view()
	    plt.tight_layout()
	    #return line,

	def display(self):
		animation_user = FuncAnimation(self.fig, self.update, interval=2000)
		#pyplot.show()

#A = Cpu_Graph()
#A.display()


