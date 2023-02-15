from tkinter import *
from tkinter import ttk
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import cpu as cpu_class
import memory as memory_class
import I_O_stats as i_o_class
import net_stats as net_class
import process as process_class
time_interval = 2000
class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x900")
        self.frame = Frame(self.master, width=600, height=800)
        self.frame.pack()
        self.current_frame = "cpu"
        self.create_buttons(self.frame)
        self.cpu()
    
    def restart_gui(self):
    	for i in self.master.winfo_children():
            i.destroy()
    	if self.current_frame == "cpu":
    		self.cpu()
    	if self.current_frame == "memory":
    		self.memory()
    	if self.current_frame == "io":
    		self.io()	
    	if self.current_frame == "net":
    		for i in self.net_root.winfo_children():
    			i.destroy()
    		self.net_root.destroy()
    		self.net()
    	if self.current_frame == "proc":
    		for i in self.proc_root.winfo_children():
    			i.destroy()
    		self.proc_root.destroy()
    		self.process()

    def text_event(self):
    	global time_interval
    	try:
    		time_interval = int(self.text_box.get())
    		self.text_box.insert(0,str(time_interval))
    		self.restart_gui()
    		return True
    	except:
    		time_interval = 2000
    		self.restart_gui()
    		return False
        	
    def create_buttons(self,framex):
    	global time_interval
    	self.cpu_btn = ttk.Button(framex, text="cpu", command=self.cpu)
    	self.cpu_btn.pack(side=LEFT)
    	self.memory_btn = ttk.Button(framex, text="memory", command=self.memory)
    	self.memory_btn.pack(side=LEFT)
    	self.io_btn = ttk.Button(framex, text="I/O", command=self.io)
    	self.io_btn.pack(side=LEFT)
    	self.net_btn = ttk.Button(framex, text="NET", command=self.net)
    	self.net_btn.pack(side=LEFT)
    	self.proc_btn = ttk.Button(framex, text="process", command=self.process)
    	self.proc_btn.pack(side=LEFT)
    	self.label = Label(framex, text="Interval").pack(side=LEFT)
    	self.sv = StringVar()
    	self.text_box = Entry(framex, textvariable = self.sv, validate="focusout", validatecommand = self.text_event)
    	self.text_box.insert(0,str(time_interval))
    	self.text_box.pack(side=LEFT)
    	self.exit_button = Button(framex, text="Exit", command=self.master.destroy)
    	self.exit_button.pack(side=LEFT)

        
    def cpu(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame1 = Frame(self.master, width=600, height=800)
        self.frame1.pack()
        self.create_buttons(self.frame1)
        self.current_frame = "cpu"
        cpu = cpu_class.Cpu_Graph()
        fig = cpu.fig
        ax = cpu.axes
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        anim = animation.FuncAnimation(fig, cpu.update, interval = time_interval)
        
        
        tkinter.mainloop()
    
    def memory(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=600, height=800)
        self.frame2.pack()
        self.create_buttons(self.frame2)
        self.current_frame = "memory"
        memory = memory_class.Memory_Graph()
        fig = memory.fig
        ax = memory.axes
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        anim = animation.FuncAnimation(fig, memory.update, interval = time_interval)

        tkinter.mainloop()

    def io(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame3 = Frame(self.master, width=600, height=800)
        self.frame3.pack()
        self.create_buttons(self.frame3)
        self.current_frame = "io"
        io = i_o_class.IO_Graph()
        fig = io.fig
        ax = io.axes
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        anim = animation.FuncAnimation(fig, io.update, interval = time_interval)

        tkinter.mainloop()

    def closing_net(self):
    	self.net_root.destroy()
    	self.cpu()
    
    def update_net_list(self):
    	
    	#net = net_class.Net_Graph()
    	data, net_utilization = self.net_c.get_y_value()
    	data = data[1:]
    	data.sort(key=lambda row:row[-2])
    	net_utilization = str(round(time_interval * net_utilization, 2))+"Kb/s"
    	self.net_usage_text_box.delete(0,"end")
    	self.net_usage_text_box.insert(0,str(net_utilization))
    	for child in self.net_tree.get_children():
    		self.net_tree.delete(child)
    	for i in data:
    		self.net_tree.insert('', 'end', text="1", values=tuple(i))
    	self.net_root.after(time_interval, self.update_net_list)
        

    def net(self):
        for i in self.master.winfo_children():
            i.destroy()
            
        self.net_root = Tk()
        self.current_frame = "net"
        self.net_root.geometry("800x800")
        self.net_root.title("Network Manager")
        self.net_root.protocol("WM_DELETE_WINDOW", self.closing_net)
        self.frame4 = Frame(self.net_root, width=500, height=800)
        self.frame4.pack()
        self.label = Label(self.frame4, text="Interval").pack(side=LEFT)
        self.sv = StringVar()
        self.text_box = Entry(self.frame4, textvariable = self.sv, validate="focusout", validatecommand = self.text_event)
        self.text_box.insert(0,str(time_interval))
        self.text_box.pack(side=LEFT)
        scroll=Scrollbar(self.net_root)
        scroll.pack(fill=Y,side=RIGHT)
        self.net_c = net_class.Net_Graph()
        data, net_utilization = self.net_c.get_y_value()
        net_utilization = str(round(time_interval * net_utilization, 2)) + "Kb/s"
        self.v = StringVar( )
        self.label2 = Label(self.frame4, text="Total Network Utilization").pack(side=LEFT)
        self.net_usage_text_box = Entry(self.frame4, textvariable = self.v, width=35)
        self.net_usage_text_box.insert(0,str(net_utilization))
        self.net_usage_text_box.pack(side=LEFT)
        headings = data[0] 
        data = data[1:]
        data.sort(key=lambda row:row[-2])
        data = [headings] + data
        tree_branches = []
        for i in data:
        	tree_branches += [i[-1]]
        tree_branches = list(set(tree_branches))
        self.net_tree = ttk.Treeview(self.net_root, column=("c1", "c2", "c3","c4","c5","c6","c7",), show='headings', height=20)
        for i in range(1,8):
        	self.net_tree.column("# "+str(i), anchor=CENTER)
        	self.net_tree.heading("# "+str(i), text=data[0][i-1])
        for i in data[1:]:
        	self.net_tree.insert('', 'end', text="1", values=tuple(i))
        
        scroll.config(command=self.net_tree.yview)
        self.net_tree.config(yscrollcommand=scroll.set)
        self.net_tree.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        self.update_net_list()
        tkinter.mainloop()

    def mixs(self, num):
    	try:
    		ele = int(num[0])
    		ele = [[ele] + num[1:]]
    		return (0, ele, '')
    	except ValueError:
    		return (1, num, '')

    def closing_proc(self):
    	self.proc_root.destroy()
    	self.cpu()

    def update_proc_list(self):
    	
    	proc = process_class.Process_Graph()
    	data = proc.get_y_value()
    	data = data[1:]
    	data.sort(key = self.mixs)
    	
    	for child in self.proc_tree.get_children():
    		self.proc_tree.delete(child)
    	for i in data:
    		self.proc_tree.insert('', 'end', text="1", values=tuple(i))
    	self.proc_root.after(time_interval, self.update_proc_list)


    def process(self):
        for i in self.master.winfo_children():
            i.destroy()
            
        self.proc_root = Tk()
        self.current_frame = "proc"
        self.proc_root.geometry("800x800")
        self.proc_root.title("Process Manager")
        self.proc_root.protocol("WM_DELETE_WINDOW", self.closing_proc)
        self.frame5 = Frame(self.proc_root, width=500, height=800)
        self.frame5.pack()
        self.label = Label(self.frame5, text="Interval").pack(side=LEFT)
        self.sv = StringVar()
        self.text_box = Entry(self.frame5, textvariable = self.sv, validate="focusout", validatecommand = self.text_event)
        self.text_box.insert(0,str(time_interval))
        self.text_box.pack(side=LEFT)
        scroll=Scrollbar(self.proc_root)
        scroll.pack(fill=Y,side=RIGHT)
        proc = process_class.Process_Graph()
        data = proc.get_y_value()
        headings = data[0] 
        data = data[1:]
        data.sort(key = self.mixs)

        data = [headings] + data
        tree_branches = []
        for i in data:
        	tree_branches += [i[-1]]
        tree_branches = list(set(tree_branches))
        self.proc_tree = ttk.Treeview(self.proc_root, column=("c1", "c2", "c3","c4","c5","c6","c7","c8"), show='headings', height=20)
        for i in range(1,9):
        	self.proc_tree.column("# "+str(i), anchor=CENTER)
        	self.proc_tree.heading("# "+str(i), text=data[0][i-1])
        for i in data[1:]:
        	self.proc_tree.insert('', 'end', text="1", values=tuple(i))
        
        scroll.config(command=self.proc_tree.yview)
        self.proc_tree.config(yscrollcommand=scroll.set)
        self.proc_tree.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        self.update_proc_list()
        tkinter.mainloop()


root = Tk()
tk = root
root.title("Task Manager")
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )
test = app(root)
root.mainloop()


