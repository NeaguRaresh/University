############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################

import json
from tkinter import *
from tkinter import messagebox

import adminDashboard
import dbController

class admin:

    def __init__(self, userData):

        self.uid = userData[0][1]
        self.firstName = userData[0][1]
        self.lastName = userData[0][2]
        self.position = userData[0][3]
        self.email = userData[0][4]
        self.passwd = userData[0][5]


class LoginWindow:

    def __init__(self):
        
        self._frame = ""
        self._root =  Tk()
        self.dbController = dbController.dbController()        

        self._root.title("Administrator Login AAT")

        self.initLoginFrame()

        self._root.mainloop()



    
    #Propery used to chage the frame easier
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value
        self._frame.tkraise()
    


    #Show login window
    def initLoginFrame(self):
       

        #Create login Widow Frame
        loginWindow = Frame(self._root, width=600, height=300)
        loginWindow.grid(row=0, column =0, sticky="news")
        
        
        
        #Place Labels 
        title = Label(loginWindow, text = "Staff Login", font=80)
        uid_label = Label(loginWindow, text= "Used ID ")
        passwd_label = Label(loginWindow, text="Password ")

        #Chagnge title label font and size
        title.config(font=("Courier", 30))

        #place labels 
        title.grid(row=2, column=2,padx=30, pady=20)
        uid_label.grid(row = 3, column=1, padx = 20, pady=5)
        passwd_label.grid(row = 4, column=1, padx = 20, pady=20)

        #Place textBoxes
        uid_string = StringVar()
        self.uid_box = Entry(loginWindow, width = 30, textvariable = uid_string)

        passwd_string = StringVar()
        self.passwd_box = Entry(loginWindow, width = 30, textvariable = passwd_string, show = "*")

        self.uid_box.grid(row = 3, column = 2)
        self.passwd_box.grid(row = 4, column = 2)
        
        #Place buttons

        login_button = Button(loginWindow, text = "Login", command = lambda: self.checkCredentials())
        login_button.grid(row= 5, column = 2, padx=0, pady=20)

        #return window
        self._frame = loginWindow
        

    #check validity
    def checkCredentials(self):
        
        # #Open and load the json file 
        # #Use sql later
        # with open("/home/vrdmprt/Desktop/Project_1811/Done/staff.json", "r") as r_file:

        #     data = json.loads(r_file.read())

        uid = self.uid_box.get()
        passwd = self.passwd_box.get()
        
        userData = self.dbController.check_user_login(uid, passwd)
       

        #Check if provided credentials are good
        if userData is not None:
            
            self._root.destroy()
            self.user = admin(userData)
            adminDashboard.staffWindow(self._frame, self.user,  self.dbController)

        else:

            #raise an error message
            messagebox.showinfo("LOGIN ERROR!", "Please enter valid uid or password", icon="warning")
            self.uid_box.delete('0', 'end')
            self.passwd_box.delete('0', 'end')


# a = LoginWindow