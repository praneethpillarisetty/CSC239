import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange



class IO_Graph():
	def __init__(self):
		self.x_data, self.y_data = [], []
		self.fig = plt.figure(figsize=(9, 6))
		self.axes = [0, 0, 0, 0]
		self.r = 1000
		self.axes[0] = self.fig.add_subplot(2,2,(1,2))
		self.axes[1] = self.fig.add_subplot(2,2,(3,4))
		self.previous_table_values = [["I/O", "Number of Disk Reads", "Number of Block Reads", "Number of Disk Writes","Number of Block Writes"]]
		prev_disk_read = 0
		prev_disk_write = 0
		prev_block_read = 0
		prev_block_write = 0
		cur_disk_read = 0
		cur_disk_write = 0
		cur_block_read = 0
		cur_block_write = 0
		fp = open('//proc/diskstats')
		lines = fp.readlines()
		count = 0
		for x in lines:
		    if 'sda' in x:
		    	values = list(" ".join(x.split()).split(' '))
		    	values = values[2:]
		    	name = values[0]
		    	prev_disk_read = int(values[1])/2
		    	prev_block_read = int(values[3])/2 
		    	prev_disk_write = int(values[5])/2 
		    	prev_block_write = int(values[7])/2
		    	#table_values = [int(values[1]), int(values[3]), int(values[5]), int(values[7])]
		    	cur_disk_read = round((abs(prev_disk_read - cur_disk_read)/2), 2)
		    	cur_block_read = round((abs(prev_block_read - cur_block_read)/2), 2)
		    	cur_disk_write = round((abs(prev_disk_write - cur_disk_write)/2), 2)
		    	cur_block_write = round((abs(prev_block_write - cur_block_write)/2), 2)
		    	self.previous_table_values += [[name, cur_disk_read, cur_block_read, cur_disk_write, cur_block_write]]
		fp.close()
		#l = self.cal_total(self.previous_table_values)
		#self.previous_table_values += [l]
		#print(self.previous_table_values)
		self.dr, self.dw, self.br, self.bw =[],[],[],[]
		#plt.yticks(color='w')

	def cal_total(self,IO_table_data):
		total_disk_read = 0
		total_disk_write = 0
		total_block_read = 0
		total_block_write = 0
		for i in IO_table_data[1:]:
			total_disk_read += i[1]
			total_block_read += i[2]
			total_disk_write += i[3]
			total_block_write += i[4]
		l = ["total", round(total_disk_read, 2), round(total_block_read, 2), round(total_disk_write, 2), round(total_block_write, 2)]
		return l
	
	def get_y_value(self):
		prev_disk_read = 0
		prev_disk_write = 0
		prev_block_read = 0
		prev_block_write = 0
		cur_disk_read = 0
		cur_disk_write = 0
		cur_block_read = 0
		cur_block_write = 0
		fp = open('//proc/diskstats')
		lines = fp.readlines()
		mem_dict = {}
		result=[]
		temp_tabel = [["I/O", "Number of Disk Reads", "Number of Block Reads", "Number of Disk Writes","Number of Block Writes"]]
		IO_table_data = [["I/O", "Number of Disk Reads", "Number of Block Reads", "Number of Disk Writes","Number of Block Writes"]]
		for x in lines:
		    if 'sda' in x:
		    	values = list(" ".join(x.split()).split(' '))
		    	values = values[2:]
		    	name = values[0]
		    	prev_disk_read = int(values[1])/2
		    	prev_block_read = int(values[3])/2 
		    	prev_disk_write = int(values[5])/2 
		    	prev_block_write = int(values[7])/2
		    	#table_values = [int(values[1]), int(values[3]), int(values[5]), int(values[7])]
		    	cur_disk_read = round((abs(prev_disk_read - cur_disk_read)/2), 2)
		    	cur_block_read = round((abs(prev_block_read - cur_block_read)/2), 2)
		    	cur_disk_write = round((abs(prev_disk_write - cur_disk_write)/2), 2)
		    	cur_block_write = round((abs(prev_block_write - cur_block_write)/2), 2)
		    	IO_table_data += [[name, cur_disk_read, cur_block_read, cur_disk_write, cur_block_write]]
		    	temp_tabel += [[name, cur_disk_read, cur_block_read, cur_disk_write, cur_block_write]]
		
		for i in IO_table_data[1:]:
			for j in self.previous_table_values[1:]:
				if i[0] == j[0]:
					i[1] = round(abs(i[1] - j[1]), 2)
					i[2] = round(abs(i[2] - j[2]), 2)
					i[3] = round(abs(i[3] - j[3]), 2)
					i[4] = round(abs(i[4] - j[4]), 2)
		self.previous_table_values = temp_tabel

		fp.close()
		return IO_table_data


	def update(self,frame):
	    self.x_data.append(datetime.now())
	    IO_table_data = self.get_y_value()
	    l = self.cal_total(IO_table_data)
	    IO_table_data += [l]
	    cur_disk_read, cur_block_read, cur_disk_write, cur_block_write = IO_table_data[-1][1:]
	    cur_disk_read = round(cur_disk_read, 2)
	    cur_block_read = round(cur_block_read, 2)
	    cur_disk_write = round(cur_disk_write, 2)
	    cur_block_write = round(cur_block_write, 2)
	    colors = [['white']*len(IO_table_data[0])] * (len(IO_table_data)-1)

	    colors += [["white","red","blue", "green","gray"]]
	    
	    self.axes[0].clear()
	    table = self.axes[0].table(cellText = IO_table_data, cellColours=colors, loc='center')
	    #table = self.axes[0].table(cellText = IO_table_data, loc='center')
	    self.axes[0].set_axis_off()
	    table.scale(1, 3)
	    
	    self.dr.append(cur_disk_read)
	    self.dw.append(cur_disk_write)
	    self.br.append(cur_block_read)
	    self.bw.append(cur_block_write)

	    self.axes[1].plot(self.x_data, self.dr, color="red")
	    self.axes[1].plot(self.x_data, self.br, color="blue")
	    self.axes[1].plot(self.x_data, self.dw, color="green")
	    self.axes[1].plot(self.x_data, self.bw, color="gray")
	    self.axes[1].title.set_text("disk utilization")
	    #self.axes[1].set_xlabel("time", fontsize = 15)
	    #self.axes[1].set_ylabel("cpu-time", fontsize = 15)
	    #self.axes[1].set_ylim([0, 100])
	    #self.axes[1].set_yticks([cpu_new])
	    plt.setp(self.axes[1].get_xticklabels(), visible=False)
	    plt.setp(self.axes[1].get_yticklabels(), visible=False)
	    self.axes[1].tick_params(axis='both', which='both', length=0)
	    self.axes[1].legend(labels = ['dr = '+str(cur_disk_read), 'br = '+str(cur_block_read), 'dw = '+str(cur_disk_write), 'bw = '+str(cur_block_write)] )
	    
	    
	    #line.set_data(x_data, y_data)
	    self.fig.gca().relim()
	    #table.auto_set_font_size(False)
	    self.fig.gca().autoscale_view()

	    #plt.tight_layout()
	    #return line,

	def display(self):
		animation_user = FuncAnimation(self.fig, self.update, interval=2000)
		#pyplot.show()

#A = IO_Graph()
#A.display()


