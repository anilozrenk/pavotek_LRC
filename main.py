from array import array
import math
from tkinter import *
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
        self.index_resonance = self.impedance.index(min(self.impedance))                                           #np.where(self.impedance==self.impedance.min())
        self.resonance_frequency=self.frequency[self.index_resonance]
        pass
    def capasitance(self):
        for i in range(len(self.frequency)):
            self.cap_table.append(abs(1/ (2 * math.pi * self.frequency[i] * self.impedance[i] ) )) 
        pass 
    
    def inductance(self):
        for i in range(len(self.frequency)):
            self.induc_table.append(abs(self.impedance[i] / (2 * math.pi * self.frequency[i] ) )) 
        pass 

    def resistance(self):
        self.resistance=min(self.impedance)
        pass
    
class Window:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Pavotek LCR")

def main():
    df=pd.read_csv('CAP.csv')   
    frequency=list(df["Frequency[Hz]"])
    impedance=list(df['Impedance[ohm]'])    
    capacitor=Capacitor(frequency,impedance)
    print(capacitor.cap_table)
    print(capacitor.resistance)



    root= Tk()
    gui=Window(root)
    myLabel= Label(root,text="lololo",padx=100)
    myLabel.pack()

    myButton=Button(root,text="click")
    myButton.pack()

    entry=Entry(root,width=50,border=5)
    entry.pack()
    entry.insert(0,"lololo")
    #root.mainloop()




main()