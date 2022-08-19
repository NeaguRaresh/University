############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################

from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class adminHome(Frame):

    def __init__(self, parent, userData, dbController, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)



        self.adminName = userData.firstName + " " + userData.lastName
        self.position = userData.position
        self.uid = userData.uid
        self.email = userData.email

        self.dbController = dbController


        self.showUserDetail()
        self.showTasks()
        self.showToDoList()
    
    def showUserDetail(self):

        emptyLabel = Label(self, text="")
        emptyLabel.pack(side="top", pady=5)

        nameLabel = Label(self, text = self.adminName)
        nameLabel.config(font="Courier 25 bold")

        positonLabel = Label(self, text=self.position)
        positonLabel.config(font="Courier 10") 

        emailLabel = Label(self, text=self.email)
        emailLabel.config(font="Courier 10")

        nameLabel.pack(side="top")
        positonLabel.pack(side="top")
        emailLabel.pack(side="top")


    def showTasks(self):

        emptyLabel = Label(self, text="")
        emptyLabel.pack(side="top", pady=10)

        
        reviewsText = str(self.dbController.get_query_count()) + " unseen customer reviews"
        queriesText = str(self.dbController.get_review_count()) + " un answered customer queries"


        reviewLabel = Label(self, text = reviewsText)
        reviewLabel.config(font=("Courier 15"))

        queriesLabel = Label(self, text=queriesText)
        queriesLabel.config(font=("Courier 15"))

        reviewLabel.pack(side="top", pady=10)
        queriesLabel.pack(padx=30)
         
    def showToDoList(self):

        text = "You have nothig in your To Do list now"

        todoNotepad = Text(self, width=50, height=25)
        todoNotepad.insert(END, text)
        todoNotepad.pack(side="top", pady=20)

