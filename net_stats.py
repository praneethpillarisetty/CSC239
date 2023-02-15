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
class Net_Graph():
	def __init__(self):
		self.x_data, self.y_data = [], []
		self.fig = plt.figure(figsize=(9, 6))
		self.axes = [0, 0]
		self.axes[0] = self.fig.add_subplot(1,2,(1,2))
		self.previous_speed = 0
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
		Net_table_data = [["connection", "source_ip", "source_port", "destination_ip", "destination_port", "username", "Program_Name"]]
		for type_connection in ["tcp","udp"]:
			fp = open("//proc/net/" + type_connection)
			lines = fp.readlines()
			lines = lines[1:]
			temp_values = [["connection", "source_ip", "source_port", "destination_ip", "destination_port", "username","sock-fd"]]
			sock_fd_list = []
			temp_values2 = [["Soc_fd","pname"]]
			for x in lines:
			    values = x.split()
			    if True :#if values[3] == "01":
				    s = values[1].split(":")
				    Source_Address = socket.inet_ntoa(struct.pack("!L",int(s[0],16)))
				    Source_Port = str(int(s[1],16))
				    r = values[2].split(":")
				    Remote_Address = socket.inet_ntoa(struct.pack("!L",int(r[0],16)))
				    Remote_Port = str(int(r[1],16))
				    Program_Name = ''
				    """
				    try:
				    	Source_Address,a,l=socket.gethostbyaddr(Source_Address)
				    except:
				    	Source_Address = Source_Address
				    try:
				    	Remote_Address,a,l=socket.gethostbyaddr(Remote_Address)
				    except:
				    	Remote_Address = Remote_Address
				    """			    
				    inode = values[7]
				    sock_fd = int(values[9])
				    User_Name = self.get_user_name(inode)
				    temp_values += [[type_connection, Source_Address, Source_Port, Remote_Address, Remote_Port, User_Name,sock_fd]]
				    sock_fd_list += [sock_fd]
			plist = os.listdir("//proc")
			numbered_program_list = [ x for x in plist if x.isdigit() ]
			for program in numbered_program_list:
				try :
					sd = os.listdir("//proc/"+program+"/fd")
					if len(sd) == 0:
						continue
					try :
						program_fd = os.popen("ls -l //proc/"+program+"/fd")
						list_discriptors = program_fd.readlines()
						for fd in list_discriptors:
							if 'socket' in fd:
								socket_discriptors = int(fd[fd.find('[')+1:fd.rfind(']')])
								if socket_discriptors in sock_fd_list:
									try:
										comm_data= open("//proc/"+program+"/comm")
										comm_data=comm_data.read()
										temp_values2 += [[socket_discriptors, comm_data]]
										comm_data.close()
									except:
										continue
						program_fd.close()
					except:
						continue
				except :
					continue
			for i in temp_values:
				for j in temp_values2:
					if i[6] == j[0]:
						Net_table_data+=[[i[0],i[1],i[2],i[3],i[4],i[5],j[1]]]
			fp.close()
		fp=open("//proc/net/dev", "r")
		read = fp.read()
		net_data = read.split(":")
		net_speed = net_data[1].split()
		total = int(net_speed[0])+int(net_speed[8]) * 8
		fp.close()
		fp = os.popen("ethtool ens33| grep -i speed")
		read = fp.read()
		band_speed = read.split()
		x = band_speed[1]
		band_width = int(x[0:x.find("M")])*100
		Net_Utilization = total/(band_width)
		Net_Utilization -= self.previous_speed
		self.previous_speed = total/(band_width)
		fp.close()
		return Net_table_data, Net_Utilization


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

#A = Net_Graph()
#A.display()
#A.get_y_value()

