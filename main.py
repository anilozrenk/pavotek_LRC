
import math
from re import M
from tkinter import *
from unicodedata import name
import numpy as np
import pandas as pd


def slope():
    return


class Capacitor:

    def __init__(self,frequency,impedance):
        self.Cap=0
        self.Ind=0
        self.Rs=0
        self.index_resonance=0
        self.resonance_frequency=0
        self.cap_table=[]
        self.induc_table=[]
        self.frequency=frequency
        self.impedance=impedance
        self.f_resonance()
        self.capasitance()
        self.inductance()
        self.resistance()

    def f_resonance(self):
        self.index_resonance = self.impedance.index(min(self.impedance))                                          
        self.resonance_frequency=self.frequency[self.index_resonance]
        pass
    def capasitance(self):
        for i in range(len(self.frequency)):
            self.cap_table.append(abs(1/ (2 * math.pi *complex(0,1)* self.frequency[i] * self.impedance[i] ) )) 
        cap_slope = [0]
        for i in range(1,len(self.cap_table)):
            cap_slope.append( (np.log(self.cap_table[i]) - np.log(self.cap_table[i-1]) )/( (np.log(self.frequency[i]) - np.log(self.frequency[i-1])) ))
        cap_slope[0]=cap_slope[1]
        index_slope = list(map(abs,cap_slope)).index(min(map(abs,cap_slope)),0,self.index_resonance)
        self.Cap=self.cap_table[index_slope]    
        pass 
    
    def inductance(self):
        for i in range(len(self.frequency)):
            self.induc_table.append(abs(self.impedance[i] / (2 * math.pi * self.frequency[i] ) )) 
        induc_slope = [0]
        for i in range(1,len(self.cap_table)):
            induc_slope.append( (np.log(self.induc_table[i]) - np.log(self.induc_table[i-1])) / ((np.log(self.frequency[i]) - np.log(self.frequency[i-1]))))
        induc_slope[0]=induc_slope[1]
        index_slope = list(map(abs,induc_slope)).index(min(list(map(abs,induc_slope))),self.index_resonance,len(induc_slope))
        self.Ind=self.induc_table[index_slope]
        pass 

    def resistance(self):
        self.resistance=min(self.impedance)
        pass
    
class Window:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Pavotek LCR")
        self.root.geometry("800x600")
        self.root.resizable(False,False)
        self.root.configure(background='#f0f0f0')
        self.root.iconbitmap('icon.ico')
        
        
      
        

def main():
    df=pd.read_csv('CAP.csv')   
    frequency=list(df["Frequency[Hz]"])
    impedance=list(df['Impedance[ohm]'])    
    capacitor=Capacitor(frequency,impedance)
    

    
    root= Tk()
    gui=Window(root)
    myLabel= Label(root,text="lololo",padx=100)
    myLabel.pack()

    myButton=Button(root,text="click")
    myButton.pack()

    entry=Entry(root,width=50,border=5,cursor='man')
    entry.pack()
    entry.insert(0,"lololo")
   
    
    canvas=Canvas(root,width=150,height=150,background="#ffffff")
    canvas.pack()
    canvas.create_oval(10,10,140,110,fill="#afafaf")
    
    listbox=Listbox(root,width=10,height=3,selectmode=SINGLE,)
    listbox.pack()
    listbox.insert(END,"lololo1")
    listbox.insert(END,"lololo2")
    listbox.insert(END,"lololo3")
    
    optmenu=OptionMenu(root,'lele',"lololo1","lololo2","lololo3")
    optmenu.pack()
    
    text=Text(root,width=50,height=2)
    text.pack()
    text.insert(END,"lololo")
    
    
    
    

    root.mainloop()
    




main()