############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################


from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class query(Button):

    def __init__(self, parent,userData, dbController, queryData, *args, **kwargs):
        Button.__init__(self, parent, *args, **kwargs)
    
        self.queryData = queryData
        self.userData = userData
        self.configure(text="Query from " + self.queryData['customer'], command= lambda: self.open())
        self.pack(side="top", fill="both")

        self.dbController = dbController

    def open(self):
        self.newWindow = Tk()
        self.newWindow.title("Query Response")
        frame = Frame(self.newWindow)

        customerLabel = Label(frame, text=self.queryData['customer'])
        customerLabel.configure(font="Courier 15 bold")
        
        dateLabel = Label(frame, text=self.queryData['date'])
        dateLabel.configure(font="Couriner 10")
        
        textLabel = Label(frame, text=self.queryData['text'])
        textLabel.configure(font="Courier 12")

        customerLabel.pack(side="top", fill="both", padx=10)
        dateLabel.pack(side="top", fill="both", padx=10)
        Label(frame, pady=10).pack(side="top")
        textLabel.pack(side="top", fill="both", padx=10)
        Label(frame, pady=10).pack(side="top")
        
        self.responseText = Text(frame, width=80, height=10, padx=10)

        saveButton = Button(frame, text="Save response", command=lambda: self.updateResponse())



        self.responseText.pack(side="top")
        saveButton.pack(side="top")

        frame.pack()

    def updateResponse(self):
        

        responseData = (self.queryData['id'], self.userData.uid, self.responseText.get("1.0",'end-1c'))

        self.dbController.updateQueryResponse(responseData)
        self.newWindow.destroy()
        self.destroy()

class review(Button):

    def __init__(self, parent, userData, dbController, reviewData, *args, **kwargs):
        Button.__init__(self, parent, *args, **kwargs)

        self.userData = userData
        self.dbController = dbController
        self.reviewData = reviewData

        self.configure(text="Review from "+self.reviewData['customer'], command= lambda: self.open())
        self.pack(side="top", fill="both")

    def open(self):
        self.newWindow = Tk()
        self.newWindow.title("Review For "+self.reviewData['product'])
        frame = Frame(self.newWindow)

        customerLabel = Label(frame, text=self.reviewData['customer'])
        customerLabel.configure(font="Courier 15 bold")
        
        dateLabel = Label(frame, text=self.reviewData['date'])
        dateLabel.configure(font="Couriner 10")
        
        productLabel = Label(frame, text=self.reviewData['product'])
        productLabel.configure(font="Courier 10")

        textLabel = Label(frame, text=self.reviewData['text'])
        textLabel.configure(font="Courier 12")

        customerLabel.pack(side="top", fill="both", padx=10)
        dateLabel.pack(side="top", fill="both", padx=10)
        productLabel.pack(side="top", fill="both", padx=10)
        Label(frame, pady=10).pack(side="top")
        textLabel.pack(side="top", fill="both", padx=10)
        Label(frame, pady=10).pack(side="top")
        
        self.responseText = Text(frame, width=80, height=10, padx=10)

        saveButton = Button(frame, text="Save response", command=lambda: self.updateResponse())


        self.responseText.pack(side="top")
        saveButton.pack(side="top")

        frame.pack()

    def updateResponse(self):
        

        responseData = (self.reviewData['id'], self.userData.uid, self.responseText.get("1.0",'end-1c'))

        self.dbController.updateReviewResponse(responseData)
        self.newWindow.destroy()
        self.destroy()


class queriesTab(Frame):

    def __init__(self, parent, userData, dbController, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        emptyLabel = Label(self, text="")
        emptyLabel.pack(side="top",pady=5)

        titleLabel = Label(self, text="Queries and Reviews")
        titleLabel.config(font="Courier 25 bold")

        titleLabel.pack(side="top")


        self.dbController = dbController
        self.itemList=[]
        self.userData = userData

        self.addWidgets()
        

    def addWidgets(self):
        

        self.canvas = Canvas(self, height=600, width=280)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvasFrame = Frame(self.canvas, height=30, width=80)
        self.canvas.create_window((0,0), window=self.canvasFrame, anchor='nw')
        
        self.getItemsToShow()
        self.refreshItems()

        self.canvasFrame.update()
        self.canvas.configure(yscrollcommand=self.scrollbar.set, scrollregion="0 0 0 %s" % self.canvasFrame.winfo_height())

        self.canvas.pack(side="left", anchor="ne")
        self.scrollbar.pack(side="right", fill=Y)


    def getItemsToShow(self):
        
        self.queries = self.dbController.get_query_list()
        self.reviews = self.dbController.get_review_list()
    
    
    def refreshItems(self):
    
        for i in self.queries:

            item = query(self.canvasFrame, self.userData,self.dbController, i)
            self.itemList.append(item)

        for i in self.reviews:
            item = review(self.canvasFrame, self.userData, self.dbController, i)



         
