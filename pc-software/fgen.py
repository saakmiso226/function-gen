#!/usr/bin/env python3

# File: main file for pc interface for function generator
# Author: Tuomas Nylund (tuomas.nylund@gmail.com)
# Website: http://tuomasnylund.fi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import io
import math

from tkinter import *
#from tkinter import ttk
from fgenio import FgenIO


class FgenFselect(Frame):
    def __init__(self,root,callback,expmin,expnum):
        Frame.__init__(self,bg="black")
        self.root = root
        self.expmin = expmin
        self.expnum = expnum

        self.callback = callback

        self.value = 0000

        self.num = []
        self.var = []

        offset = 0
        
        self.imageup = PhotoImage(file="icons/arrow_up.gif")
        self.imagedown = PhotoImage(file="icons/arrow_down.gif")

        #for i in range(0,10):
        while len(self.var)<self.expnum:
            self.var.append(IntVar())
            if not (self.expnum+1+self.expmin - len(self.var)) % 3:
                if len(self.var) > 1:
                    if self.expnum+self.expmin+1 == len(self.var):
                        Label(self,text='.',bg="black",fg="red").grid(column=len(self.var)+offset,row=1)
                    else:
                        Label(self,text=',',bg="black",fg="red").grid(column=len(self.var)+offset,row=1)
                    offset += 1

            #this has to be the most horrible looking code I've done in ages
            Button(self, image=self.imageup, relief="flat",highlightbackground="black",bd=0,width=12,height=12,bg="black", command= lambda pos=self.expnum+self.expmin-len(self.var): self.btnCallback(pos,1)).grid(column=len(self.var)+offset,row=0)
            Label(self,textvariable=self.var[len(self.var)-1],bg="black",fg="white").grid(column=len(self.var)+offset,row=1)
            Button(self, image=self.imagedown, relief="flat",highlightbackground="black",bd=0,width=12,height=12,bg="black", command= lambda pos=self.expnum+self.expmin-len(self.var): self.btnCallback(pos,-1)).grid(column=len(self.var)+offset,row=2)

        Label(self,text='Hz',bg="black",fg="white").grid(column=len(self.var)+offset+1,row=1)

        self.setDigits()

    def btnCallback(self,exp,change):
        self.value += math.pow(10,exp)*change
        if self.value < 0:
            self.value = 0
        self.setDigits()
        print (self.value)
        self.callback(self.value)

    def setDigits(self):
        valstr = str(self.value)
        for i in range (0,self.expnum):
            self.var[i].set(int(self.value/math.pow(10,self.expnum+self.expmin-1-i)%10))



class FgenPselect(Frame):
    def __init__(self,root,callback):
        Frame.__init__(self)
        self.root = root
        self.callback = callback

        self.columnconfigure(1,weight=1)

        self.var = DoubleVar()
        Label(self, textvariable=self.var,width=5).grid(column=0,row=0,sticky=W)
        Scale(self, variable=self.var, command=self.scaleCallback, from_=0, to=360,orient=HORIZONTAL,length=120,showvalue=0).grid(column=2,row=0,sticky=E)

    def scaleCallback(self,event):
        self.callback(self.var.get())

class FgenMode(Frame):
    def __init__(self,root,callback):
        Frame.__init__(self)
        self.root = root
        self.callback = callback
        self.var = StringVar()
        self.var.set("Off")

        Label(self,text="Mode:").grid(sticky=W,column=0,row=0)
        self.columnconfigure(1,weight=1)
        Radiobutton(self,command=self.btnCallback,text="Off"     ,variable=self.var,value="Off"     ).grid(column=2,row=0)
        Radiobutton(self,command=self.btnCallback,text="Sine"    ,variable=self.var,value="Sine"    ).grid(column=3,row=0)
        Radiobutton(self,command=self.btnCallback,text="Triangle",variable=self.var,value="Triangle").grid(column=4,row=0)
        Radiobutton(self,command=self.btnCallback,text="Square"  ,variable=self.var,value="Square"  ).grid(column=5,row=0)

    def btnCallback(self):
        print (self.var.get())
        self.callback(self.var.get())





class FgenFMode(Frame):
    def __init__(self,root,callback):
        Frame.__init__(self)
        self.root = root
        self.callback = callback
        self.var = StringVar()
        self.var.set("1")

        Label(self,text="Frequency:").grid(sticky=W,column=0,row=0)
        self.columnconfigure(1,weight=1)
        Radiobutton(self,command=self.btnCallback,text="Freq1",variable=self.var,value="1").grid(column=2,row=0)
        Radiobutton(self,command=self.btnCallback,text="Freq2",variable=self.var,value="2").grid(column=3,row=0)
        Radiobutton(self,command=self.btnCallback,text="FSK"  ,variable=self.var,value="m").grid(column=4,row=0)

    def btnCallback(self):
        self.callback(self.var.get())
        
        
class FgenPMode(Frame):
    def __init__(self,root,callback):
        Frame.__init__(self)
        self.root = root
        self.callback = callback
        self.var = StringVar()
        self.var.set("Phase1")

        Label(self,text="Phase:").grid(sticky=W,column=0,row=0)
        self.columnconfigure(1,weight=1)
        Radiobutton(self,command=self.btnCallback,text="Phase1",variable=self.var,value="1").grid(column=2,row=0)
        Radiobutton(self,command=self.btnCallback,text="Phase2",variable=self.var,value="2").grid(column=3,row=0)
        Radiobutton(self,command=self.btnCallback,text="PSK",variable=self.var,value="m").grid(column=4,row=0)
        
    def btnCallback(self):
        self.callback(self.var.get())


def test(var,var2):
    print(var,var2)


fgen = FgenIO()
fgen.open("/dev/ttyACM0")

root = Tk()
root.title("FGen controller")
root.grid()
root.columnconfigure(1,weight=1)

Label(root,text="Frequency 1:").grid(column=0,row=0)
fsel1 = FgenFselect(root,lambda val:fgen.setFreq(1,val),-2,9).grid(column=0,row=1,padx=5)

Label(root,text="Frequency 2:").grid(column=2,row=0)
fsel2 = FgenFselect(root,lambda val:fgen.setFreq(2,val),-2,9).grid(column=2,row=1,padx=5)

Label(root,text="Phase 1:").grid(column=0,row=2)
psel1 = FgenPselect(root,lambda val:fgen.setPhase(1,val)).grid(column=0,row=3,sticky=W+E)

Label(root,text="Phase 2:").grid(column=2,row=2)
psel2 = FgenPselect(root,lambda val:fgen.setPhase(2,val)).grid(column=2,row=3,sticky=W+E)

msel = FgenMode (root,fgen.setMode    ).grid(column=0,columnspan=3,row=5,sticky=E+W)
fsel = FgenFMode(root,fgen.setFreqOut ).grid(column=0,columnspan=3,row=7,sticky=E+W)
psel = FgenPMode(root,fgen.setPhaseOut).grid(column=0,columnspan=3,row=9,sticky=E+W)

Label(root,text="Modulation Frequency").grid(column=0,row=10)
mfsel = FgenFselect(root,fgen.setModFreq,0,6).grid(column=0,row=11,padx=5)
#mfsel = FgenMFselect(root,fgen.setModFreq).grid(column=0,row=11,sticky=W+E)

root.mainloop()
