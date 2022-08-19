############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from queries import *
from salesReport import *
from discount import *
from adminHome import *


class staffWindow:

    def __init__(self, frame, user, dbCountroller):
        


        self._root = Tk()
        self._frame = frame
        self.user = user
        self.dbController = dbCountroller

        self._root.title("Admin Dashboard")

        self.initFrames()
        self._root.mainloop()


    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value
        self._frame.tkraise()


    def initFrames(self):

        
        self.tabControl = ttk.Notebook(self._root)

        self.home = adminHome(self.tabControl, self.user, self.dbController)
        self.queries = queriesTab(self.tabControl,self.user, self.dbController)
        self.data = salesReport(self.tabControl,  self.dbController)
        self.scheme = discountScheme(self.tabControl,  self.dbController)

        self.tabControl.add(self.home,    text ="Home")
        self.tabControl.add(self.queries, text="Queries & Reviews")
        self.tabControl.add(self.data,    text="Sales Reports")
        self.tabControl.add(self.scheme,  text ="Discount schemes" )
        self.tabControl.pack()
        

    def initHome(self):

        homeFrame = ttk.Frame(self.tabControl, width=800, height=800)
        homeFrame.grid(row=0, column =0, sticky="news")

        

        return homeFrame


