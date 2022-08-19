############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

class salesReport(Frame):

    def __init__(self, parent,dbController, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        title = Label(self, text="Sales Reports", padx=200, pady=30)
        title.config(font=("Courier", 20))

        title.pack(side="top")

        self.months=[]
        self.dbController = dbController

        self.addWidgets()

    def addWidgets(self):
        
        productsLabel = LabelFrame(self, text="Products: ", font="Courier 15 bold")
        monthsLabel = LabelFrame(self, text="Months: ", font="Courier 15 bold")

        graphLabel = LabelFrame(self, text="Graph type: ", font="Courier 15 bold")


        productsLabel.pack(side="top")
        self.addProducts(productsLabel)
        monthsLabel.pack(side="top")
        self.addMonths(monthsLabel)
        graphLabel.pack(side="top")
        self.addGraph(graphLabel)

        self.createButton = Button(self, text="Create Chart", command= lambda: self.createGraph())
        self.createButton.pack(side="top")
    
    def addProducts(self, frame):

        products = self.dbController.getProductIdName()
  

        self.productsButtons = []

        for product in products:
            var1 = IntVar()
            btn = Checkbutton(frame, text=product[1], variable=var1, onvalue=1, offvalue=0, font="Courier 10")
            btn.pack(side="top")
            self.productsButtons.append((var1, product[1]))

        var2 = IntVar()
        btn = Checkbutton(frame, text="All products", variable = var2,font="Courier 10")
        btn.pack(side="top")
        self.productsButtons.append((var2,"All products"))

    def addMonths(self,frame):
        
        months = ['JAN', 'FEB', 'MAR' ,'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.monthsButtons = []
        for month in months:
            var1 = IntVar()
            btn = Checkbutton(frame, text=month, variable=var1, onvalue=1, offvalue=0, font="Courier 10")
            btn.pack(side="left")
            self.monthsButtons.append((var1, month))

        var2 = IntVar()
        btn = Checkbutton(frame, text="All months", variable=var2, font="Courier 10")
        btn.pack(side="left")
        self.monthsButtons.append((var2, "All months"))

    def addGraph(self, frame):

        graphs = ["Barchart", "Linechart", "Piechart"]
        self.graphsButtons = []

        count=0
        self.graphType= IntVar()
        for graph in graphs:
            count+=1
            btn = Radiobutton(frame, variable=self.graphType, value=count, text=graph, font="Courier 10")
            btn.pack(side="left")


    def createGraph(self):
        
        #Get products
        self.selectedProducts = []
        forAll = 0

        #if all products is checked
        if self.productsButtons[len(self.productsButtons)-1][0].get():
            forAll = 1

        for product in self.productsButtons[:-1]:
            
            if forAll or product[0].get():
                self.selectedProducts.append(product[1])
            


    

        #Get months
        self.selectedMonths = []
        forAll = 0

        if self.monthsButtons[len(self.monthsButtons)-1][0].get():
            forAll = 1
        for month in self.monthsButtons[:-1]:

            if month[0].get() or forAll:
                
                self.selectedMonths.append(month[1])

        if len(self.selectedMonths) == 0:
            messagebox.showinfo("ERROR!", "Please select at least one month!", icon="warning")

        if len(self.selectedProducts) == 0:
            messagebox.showinfo("ERROR!", "Please select at least one product!", icon="warning")

        if self.graphType.get() == 0:
            messagebox.showinfo("ERROR!", "Please select a chart type!", icon="warning")


        #Create Barchart
        if self.graphType.get() == 1:
            self.createBarchart()
        if self.graphType.get() == 2:
            self.createLinechart()
        if self.graphType.get() == 3:
            self.createPiechart()



    def createBarchart(self):
        #Get sales for selected Products
        sales = self.dbController.getSalesForProduct(self.selectedProducts, self.selectedMonths)
        
        n_groups = len(self.selectedMonths)

        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.2
        opacity = 1

        offset = 0
        for i in sales:
            bar = plt.bar(index + offset, list(sales[i].values()),
                          bar_width, alpha =opacity,
                          label=i)
            offset+=bar_width

        plt.xlabel('Month')
        plt.ylabel('Units Sold')
        plt.title('Barchart Sales')
        plt.xticks(index + bar_width, tuple(sales[self.selectedProducts[0]].keys()))
        plt.legend()

        plt.tight_layout()
        plt.show()




    def createPiechart(self):
        sales = self.dbController.getSalesForProduct(self.selectedProducts, self.selectedMonths)

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        
        labels = list(sales.keys())
    

        x = []
        for i in labels:
            sum = 0
            for j in sales[i]:
                sum+= sales[i][j]
            x.append(sum)


        ax.pie(x, labels=labels, autopct='%2.0f%%')
        
        plt.show()
            



    def createLinechart(self):
        sales = self.dbController.getSalesForProduct(self.selectedProducts, self.selectedMonths)

        x = self.selectedMonths
        
        for i in sales:
            y = list(sales[i].values())
            plt.plot(x,y, label=i)
        plt.legend()
        plt.show()
        