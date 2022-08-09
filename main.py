
import math
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
import numpy as np
import pandas as pd





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
    
class Application:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Pavotek LCR")
        self.root.geometry("800x600")
        #self.root.resizable(False,False)
        self.root.configure(background='#f0f0f0')
        #self.root.iconbitmap('icon.ico')
        self.choicetext = Entry (self.root,width=30)
        self.choicetext.insert(0,"./data/data.csv")
        self.choicetext.pack()

        self.choicebutton = Button (self.root,text="Choose file",command=self.choiceFreqResponseData)
        self.choicebutton.pack()

        self.db_or_z=IntVar()
        self.dbradio = Radiobutton(self.root,text="dB formatted data",variable=self.db_or_z,value=0).pack()
        self.zradio = Radiobutton(self.root,text="Z formatted data",variable=self.db_or_z,value=1).pack()

        self.component=Combobox(self.root,values=["Capacitor","Inductor","CM Choke"])
        self.component.pack()

        self.runbutton = Button (self.root,text="Run",command=self.routine)
        self.runbutton.pack()

    def choiceFreqResponseData(self):
        self.filename = filedialog.askopenfilename(
                                    initialdir = "./",
                                    title = "Select file",
                                    filetypes = (("csv files","*.csv"),("txt files","*.txt"),("all files","*.*")))
        self.choicetext.delete(0,END)
        self.choicetext.insert(0,self.filename)
        
        pass

    def choiceComponent(self):
        pass

        ##TODO
        ##Protect against emty file
        ##Protect against wrong file type
        ##dB to Z conversion
        ##
        ##Plotting
        ##Save to file
    def routine(self):
        comp=self.component.get()

        df=pd.read_csv(self.filename)   

        self.frequency=list(df.iloc[:,0])
        self.impedance=list(df.iloc[:,1])  

        #self.frequency=list(df["Frequency[Hz]"])
        #self.impedance=list(df['Impedance[ohm]'])  


        if comp=="Capacitor":
            self.capacitor=Capacitor(self.frequency,self.impedance)
            self.solution=Label(self.root,text="Capacitance: "+str(self.capacitor.Cap)+
                    "\nInductance: "+str(self.capacitor.Ind)+
                    "\nSerial Resistance: "+str(self.capacitor.resistance) +
                    "\nResonance frequency: "+str(self.capacitor.resonance_frequency))                    
            self.solution.pack()
            pass

        elif comp=="Inductor":
            pass
        elif comp=="CM Choke":
            pass

        pass


    

def main():
         

    root = Tk()
    app = Application(root)


    
   
    
    #chart = FigureCanvasTkAgg(figure, root)

    root.mainloop()
    




main()