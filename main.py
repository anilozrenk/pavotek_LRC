from ast import Lambda
import math
import string
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
import numpy as np
import pandas as pd
import os.path




#TODO

class ModelMaker:
    def __init__(self):
        self.cap_asy_temp:string
        self.cap_model_temp:string
        
    def capacitor_model(self,name:string,cap,ind,res,dest):    
        with open("./model_template/cap.asy") as f:
            self.cap_asy_temp = f.readlines()
        with open("./model_template/cap.model") as f:
            self.cap_model_temp = f.readlines()
        self.cap_model_temp.format(nameVal=name,capVal=cap,indVal=ind,resVal=res)
        with open(dest+"/%s.model"%name,"w") as f:
            f.writelines(self.cap_model_temp)
        with open(dest+"/%s.asy"%name,"w") as f:
            f.writelines(self.cap_asy_temp)

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

        self.Ind=1/(4*(math.pi**2)*(self.resonance_frequency**2)*self.Cap)

        pass 

    def resistance(self):
        self.Rs=min(self.impedance)
        pass
class Inductor:

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
        self.inductance()
        self.capasitance()
        self.resistance()

        
    def f_resonance(self):
        self.index_resonance = self.impedance.index(max(self.impedance))                                          
        self.resonance_frequency=self.frequency[self.index_resonance]
        pass
    def capasitance(self):
        for i in range(len(self.frequency)):
            self.cap_table.append(abs(1/ (2 * math.pi *complex(0,1)* self.frequency[i] * self.impedance[i] ) )) 
        cap_slope = [0]
        for i in range(1,len(self.cap_table)):
            cap_slope.append( (np.log(self.cap_table[i]) - np.log(self.cap_table[i-1]) )/( (np.log(self.frequency[i]) - np.log(self.frequency[i-1])) ))
        cap_slope[0]=cap_slope[1]
        index_slope = list(map(abs,cap_slope)).index(min(map(abs,cap_slope)),self.index_resonance,len(cap_slope))
        self.Cap=self.cap_table[index_slope]    
                
        
        self.Cap=1/(4*(math.pi**2)*(self.resonance_frequency**2)*self.Ind)

        pass 
    
    def inductance(self):
        for i in range(len(self.frequency)):
            self.induc_table.append(abs(self.impedance[i] / (2 * math.pi * self.frequency[i] ) )) 
        induc_slope = [0]
        for i in range(1,len(self.cap_table)):
            induc_slope.append( (np.log(self.induc_table[i]) - np.log(self.induc_table[i-1])) / ((np.log(self.frequency[i]) - np.log(self.frequency[i-1]))))
        induc_slope[0]=induc_slope[1]
        index_slope = list(map(abs,induc_slope)).index(min(list(map(abs,induc_slope))),0,self.index_resonance)
        self.Ind=self.induc_table[index_slope]
        pass 

    def resistance(self):
        self.Rs=max(self.impedance)
        pass
    
class CmChoke:

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
        self.inductance()
        self.capasitance()
        self.resistance()
        self.Rs=self.Rs*2
        self.Cap=self.Cap/2

        
    def f_resonance(self):
        self.index_resonance = self.impedance.index(max(self.impedance))                                          
        self.resonance_frequency=self.frequency[self.index_resonance]
        pass
    def capasitance(self):
        for i in range(len(self.frequency)):
            self.cap_table.append(abs(1/ (2 * math.pi *complex(0,1)* self.frequency[i] * self.impedance[i] ) )) 
        cap_slope = [0]
        for i in range(1,len(self.cap_table)):
            cap_slope.append( (np.log(self.cap_table[i]) - np.log(self.cap_table[i-1]) )/( (np.log(self.frequency[i]) - np.log(self.frequency[i-1])) ))
        cap_slope[0]=cap_slope[1]
        index_slope = list(map(abs,cap_slope)).index(min(map(abs,cap_slope)),self.index_resonance,len(cap_slope))
        self.Cap=self.cap_table[index_slope]    
        pass
        ##
        self.Cap=1/(4*(math.pi**2)*(self.resonance_frequency**2)*self.Ind)
    
    def inductance(self):
        for i in range(len(self.frequency)):
            self.induc_table.append(abs(self.impedance[i] / (2 * math.pi * self.frequency[i] ) )) 
        induc_slope = [0]
        for i in range(1,len(self.cap_table)):
            induc_slope.append( (np.log(self.induc_table[i]) - np.log(self.induc_table[i-1])) / ((np.log(self.frequency[i]) - np.log(self.frequency[i-1]))))
        induc_slope[0]=induc_slope[1]
        index_slope = list(map(abs,induc_slope)).index(min(list(map(abs,induc_slope))),0,self.index_resonance)
        self.Ind=self.induc_table[index_slope]
        pass 

    def resistance(self):
        self.Rs=max(self.impedance)
        pass
        
        
class Application:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Pavotek LCR")
        self.root.geometry("500x800")
        #self.root.resizable(False,False)
        self.root.configure(background='#f0f0f0')
        #self.root.iconbitmap('icon.ico')

        Label(self.root,text="Pavotek LCR",font=("Helvetica",20),bg="#f0f0f0",fg="#000000",pady=50).pack()
        
        Label(self.root,text="Enter the file destination",bg="#f0f0f0",pady=10).pack()
        self.choicetext = Entry (self.root,width=30)
        self.choicetext.insert(0,"./data/data.csv")
        self.choicetext.pack()

        self.choicebutton = Button (self.root,text="Choose file",command=self.choiceFreqResponseData)
        self.choicebutton.pack()

        Label(self.root,text="Is it csv format or table format",bg="#f0f0f0",pady=10).pack()
        self.csv_or_table = IntVar()
        self.csvradio = Radiobutton(self.root,text="CSV",variable=self.csv_or_table,value=0,bg="#f0f0f0").pack()
        self.tableradio = Radiobutton(self.root,text="Table",variable=self.csv_or_table,value=1,bg="#f0f0f0").pack()

        Label(self.root,text="Is decimal seperator comma or dot",bg="#f0f0f0",pady=10).pack()
        self.decimalsep_comma_or_dot = IntVar()
        self.commaradio = Radiobutton (self.root,text="Decimal Comma",
                                        variable=self.decimalsep_comma_or_dot,value=0,bg="#f0f0f0").pack()
        self.dotradio   = Radiobutton (self.root,text="Decimal Dot",
                                        variable=self.decimalsep_comma_or_dot,value=1,bg="#f0f0f0").pack()
        
        Label(self.root,text="Impedance data type dB or Z(ohm)?",bg="#f0f0f0",pady=10).pack()
        self.db_or_z=IntVar()
        self.dbradio = Radiobutton(self.root,text="dB formatted data",
                                    variable=self.db_or_z,value=0,bg="#f0f0f0").pack()
        self.zradio = Radiobutton(self.root,text="Z formatted data",
                                    variable=self.db_or_z,value=1,bg="#f0f0f0").pack()

        self.component=Combobox(self.root,values=["Capacitor","Inductor","CM Choke"],height=5,width=20,state="readonly")
        self.component.pack()

        self.runbutton = Button (self.root,text="Run",command=self.routine)
        self.runbutton.pack()
        self.solution=Label(self.root,text="",bg="#f0f0f0",pady=10)
    def choiceFreqResponseData(self):
        self.filename = filedialog.askopenfilename(
                                    initialdir = "./",
                                    title = "Select file",
                                    filetypes = (("all files","*.*"),("txt files","*.txt"),("csv files","*.csv")))
        self.choicetext.delete(0,END)
        self.choicetext.insert(0,self.filename)        
        pass


        ##TODO
        ##Plotting
        ##Save to file
    def routine(self):
        
        
        if self.csv_or_table.get()==0:
            df=pd.read_csv(self.filename,sep=",",decimal=".")
            pass
        else:
            if self.decimalsep_comma_or_dot.get()==0:
                df=pd.read_table(self.filename,decimal=",")
                pass
            else:
                df=pd.read_table(self.filename,decimal=".")
                pass
            df=pd.read_table(self.filename,sep="\t",decimal=",")
            pass

        self.frequency=list(df.iloc[:,0])
        self.impedance=list(df.iloc[:,1])  

        if self.db_or_z.get()==0:
            self.impedance=list(map(lambda x: 10**(x/20),self.impedance))
            pass
        elif self.db_or_z.get()==1:
            pass
        else:
            messagebox.showerror("Error","Choose if data is in dB or Z format")
            pass  

        comp=self.component.get()

        self.genButton= Button (self.root,text="Generate",command=self.generate)
        if comp=="Capacitor":
            self.capacitor=Capacitor(self.frequency,self.impedance)
            self.solution=Label(self.root,text="Capacitance: "+str(self.capacitor.Cap)+
                    "\nInductance: "+str(self.capacitor.Ind)+
                    "\nSerial Resistance: "+str(self.capacitor.Rs) +
                    "\nResonance frequency: "+str(self.capacitor.resonance_frequency))                    
            self.solution.pack()
            self.genButton.config(text="Generate Capacitor Model",command=self.generateCapacitor)
            pass
        elif comp=="Inductor":
            self.inductor=Inductor(self.frequency,self.impedance)
            self.solution=Label(self.root,text="Capacitance: "+str(self.inductor.Cap)+
                    "\nInductance: "+str(self.inductor.Ind)+
                    "\nSerial Resistance: "+str(self.inductor.Rs) +
                    "\nResonance frequency: "+str(self.inductor.resonance_frequency))
            self.solution.pack()
            self.genButton.config(text="Generate Inductor Model",command=self.generateInductor)
            pass
        elif comp=="CM Choke":
            self.cmchoke=CmChoke(self.frequency,self.impedance)
            self.solution=Label(self.root,text="Capacitance: "+str(self.cmchoke.Cap)+
                    "\nInductance: "+str(self.cmchoke.Ind)+
                    "\nSerial Resistance: "+str(self.cmchoke.Rs) +
                    "\nResonance frequency: "+str(self.cmchoke.resonance_frequency))
            self.solution.pack()
            self.genButton.config(text="Generate CM Choke Model",command=self.generateCmChoke)

            pass

        pass
        
        def generateCapacitor(self):
            self.destChooser=filedialog.askdirectory(initialdir="./",title="Select destination")
            self.name= simpledialog.askstring("Name","Enter name of generated capacitor model")
            self.modelmaker=ModelMaker().capacitor_model(self.name,self.capacitor.Cap,self.capacitor.Ind,self.capacitor.Rs,self.destChooser)
            pass
        def generateInductor(self):
            self.destChooser=filedialog.askdirectory(initialdir="./",title="Select destination")
            self.name= simpledialog.askstring("Name","Enter name of generated inductor model")
            self.modelmaker=ModelMaker().inductor_model(self.name,self.inductor.Cap,self.inductor.Ind,self.inductor.Rs,self.destChooser)
            pass
        def generateCmChoke(self):
            self.destChooser=filedialog.askdirectory(initialdir="./",title="Select destination")
            self.name= simpledialog.askstring("Name","Enter name of generated cm choke model")
            self.modelmaker=ModelMaker().cmchoke_model(self.name,self.cmchoke.Cap,self.cmchoke.Ind,self.cmchoke.Rs,self.destChooser)
            pass


def main():
         

    root = Tk()
    app = Application(root)

    root.mainloop()
    




main()