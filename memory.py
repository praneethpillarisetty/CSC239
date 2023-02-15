import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange



class Memory_Graph():
	def __init__(self):
		self.x_data, self.y_data = [], []
		self.fig = plt.figure(figsize=(9, 6))
		self.axes = [0, 0, 0]
		self.r = 100
		self.axes[2] = self.fig.add_subplot(2,2,(3,4))
		self.axes[0] = self.fig.add_subplot(2,2,1)
		self.axes[1] = self.fig.add_subplot(2,2,2)
		self.used, self.aval, self.total =[],[],[]
		#plt.yticks(color='w')


	def get_y_value(self):
		cur_used_mem_value = 0
		cur_aval_mem_value = 0
		cur_total_mem_value = 0
		prev_used_mem_value = 0
		prev_aval_mem_value = 0
		prev_total_mem_value = 0
		total_cpu_prev = 0
		fp = open('//proc/meminfo')
		lines = fp.readlines()
		mem_dict = {}
		result=[]
		for x in lines:
		    if 'Mem' in x:
		    	values = list(" ".join(x.split()).split(' '))
		    	value = int(values[1])

		    	if 'MemAvailable:' == str(values[0]):
		    		mem_dict["MemAvailable"] = value
		    	elif 'MemFree:' in values:
		    		mem_dict["MemFree"] = value
		    	else:
		    		mem_dict["MemTotal"] = value
		    	
#		cur_aval_mem_value = abs(int(mem_dict["MemAvailable"]) - prev_aval_mem_value)
#		cur_used_mem_value = abs(int(mem_dict["MemFree"]) - prev_used_mem_value)
		cur_aval_mem_value = int(mem_dict["MemAvailable"])
		cur_used_mem_value = int(mem_dict["MemFree"])
		cur_total_mem_value = int(mem_dict["MemTotal"])
		total_table = [[ 'Memory', 'used', 'available', 'total', 'percentage(used)']]
		total_table += [[ 'Memory', str(round(cur_used_mem_value/self.r, 3)) + 'MB', \
		str(round((cur_total_mem_value - cur_used_mem_value)/self.r, 3)) + 'MB',\
		str(round(cur_total_mem_value/self.r, 3)) + 'MB', round(cur_used_mem_value/cur_total_mem_value *100, 2) ]]
		#print(cur_total_mem_value)
		
	   	
		fp.close()
		return cur_aval_mem_value, cur_used_mem_value, cur_total_mem_value, total_table


	def update(self,frame):
	    self.x_data.append(datetime.now())
	    aval_new, used_new, total_new, table_data = self.get_y_value()
	    aval_new = (total_new - used_new)
	    
	    #y_data.append(user)
	    self.used.append(used_new)
	    self.aval.append(aval_new)
	    self.total.append(total_new)
	    
	    self.axes[0].plot(self.x_data, self.used, color="red")
	    self.axes[0].title.set_text("used memory")
	    #self.axes[0].set_xlabel("time", fontsize = 15 )
	    #self.axes[0].set_ylabel("utilized", fontsize = 15)
	    #self.axes[0].set_ylim([0, total_new])
	    #self.axes[0].set_yticks([round(used_new,2)])
	    plt.setp(self.axes[0].get_xticklabels(), visible=False)
	    plt.setp(self.axes[0].get_yticklabels(), visible=False)
	    self.axes[0].tick_params(axis='both', which='both', length=0)
	    self.axes[0].legend(labels = [round(used_new/self.r, 2)] )
	    
	    
	    self.axes[1].plot(self.x_data, self.aval, color="gray")
	    self.axes[1].title.set_text("available memory ")
	    #self.axes[1].set_xlabel("time", fontsize = 15)
	    #self.axes[1].set_ylabel("available", fontsize = 15)
	    #self.axes[1].set_ylim([0, total_new])
	    #self.axes[1].set_yticks([round(aval_new,2)])
	    plt.setp(self.axes[1].get_xticklabels(), visible=False)
	    plt.setp(self.axes[1].get_yticklabels(), visible=False)
	    self.axes[1].tick_params(axis='both', which='both', length=0)
	    self.axes[1].legend(labels = [round(aval_new/self.r,2)] )
	    
	    self.axes[2].clear()
	    table = self.axes[2].table(cellText = table_data, loc='center')
	    self.axes[2].set_axis_off()
	    table.scale(1, 2)
	    
	    
	    #line.set_data(x_data, y_data)
	    #self.fig.gca().relim()
	    self.fig.gca().autoscale_view()

	    plt.tight_layout()
	    #return line,

	def display(self):
		animation_user = FuncAnimation(self.fig, self.update, interval=2000)
		#pyplot.show()

#A = Memory_Graph()
#A.display()
#A.get_y_value()

