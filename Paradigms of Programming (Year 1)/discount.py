


from tkinter import *
from tkinter import messagebox
from tkinter import ttk



class discountScheme(Frame):

    def __init__(self, parent, dbController, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        title = Label(self, text="Discount Schemes", padx=200, pady=30)
        title.config(font=("Courier", 20))

        title.pack(side="top")

        self.dbController = dbController
        self.productIdName = self.dbController.getProductsIdName()
        
        self.initGUI()


    def initGUI(self):
        self.discountDisplay = self.addDisplay()
        self.addButtons()

        self.showDiscounts()


    def addButtons(self):

        self.addDiscountBtn = Button(self, text="Add Discount Scheme", command= lambda: self.addDiscount())
        self.removeDiscountBtn = Button(self, text="Remove Discount Scheme", command = lambda : self.removeDiscount())
        self.changeDiscountBtn = Button(self, text="Change Discount Scheme", command = lambda : self.changeDiscount())

        
        self.addDiscountBtn.pack(side="top")
        self.removeDiscountBtn.pack(side="top")
        self.changeDiscountBtn.pack(side="top")

    def addDisplay(self):

        #get Products
    
        discountLabelframe = LabelFrame(self,text="Discounts", font="Courier 15 bold", borderwidth=1)
        
        discountLabelframe.pack(side="top")
        return discountLabelframe
    #Returns a list with titles based on the productsId inside the discount
    def createTitles(self):
        self.discounts = self.dbController.getDiscounts()
        fullText = []
        for discount in self.discounts:
            
            productsToAplly = discount[1].split(',')
            text = ""
            for prodcut in productsToAplly:
                
                for id in self.productIdName:
                    if prodcut == id[0]:
                        text += ", " + str(id[1])
                        break

            fullText.append(discount[0]  + " - " +text[2:] + " - " + discount[2] + " - " + discount[3])

        return fullText

    def showDiscounts(self):
        
        #Remove all the discounts before
        for slave in self.discountDisplay.slaves():
            slave.destroy()

        #Refresh the dicounts and titles
        
        titles = self.createTitles()

        self.discountButtons = []

        self.individualDiscount = IntVar()
        count=-1
        for title in titles:
            
            button = Radiobutton(self.discountDisplay, anchor="w", text = title, variable=self.individualDiscount, value=count)
            button.pack(fill="both")
            count+=1
            self.discountButtons.append((count, title))

        
            

    def addDiscount(self):

        self.addWindow = Tk()
        self.addWindow.title("Add Discount Scheme")

        frame = Frame(self.addWindow)

        title = Label(frame, text="Add discount", font="Courier 17 bold")
        title.grid(row="0",column="1")

        productLabelFrame = LabelFrame(frame, text="Products")
        
        self.addProductsToLabelFrame(productLabelFrame,"")
    
        discountAmountLabel=Label(frame, text="Discount:", font="Courier 12 bold")
        discountAmountLabel.grid(row="2", column="0",pady=20)

        discountAmount_string = StringVar()
        self.discountAmountEntry=Entry(frame, width=15, textvariable=discountAmount_string)
        self.discountAmountEntry.grid(row="2", column="1")

        promoCodeLabel=Label(frame, text="Promo code:", font="Courier 12 bold")
        promoCodeLabel.grid(row="3", column="0")

        promoCode_string = StringVar()
        self.promoCodeEntry=Entry(frame, width=15, textvariable=promoCode_string)
        self.promoCodeEntry.grid(row="3", column="1",pady=20)


        self.addDiscountButton = Button(frame, text="Add Discount Scheme", command = lambda : self.sendData("add"))
        self.addDiscountButton.grid(row="4",column="1")
        productLabelFrame.grid(row="1", column="1")
        frame.pack()
        
        

    def addProductsToLabelFrame(self, frame, checkState):

        self.productChechBoxList = []
        
        for i in self.productIdName:
            var1 = IntVar()
            btn = ttk.Checkbutton(frame, text=i[1], variable=var1, onvalue=1, offvalue=0)
            for product in checkState:
                if i[1] not in product:
                    btn.state(['!alternate'])
                else:
                    btn.state(['selected'])
            
            btn.pack(side="top")
            self.productChechBoxList.append((i[1], btn))

    def sendData(self, type):
        
        #Prepare data
        
        productIds = ""
        
        for product in self.productChechBoxList:
            
            if 'selected' in product[1].state():
                
                for id in self.productIdName:
                    
                    if product[0] == id[1]:
                        productIds += id[0]+","

        

        try:
            int(self.discountAmountEntry.get())
            if int(self.discountAmountEntry.get()) > 100 or int(self.discountAmountEntry.get()) < 1:
                raise(ValueError)
        except ValueError:
            messagebox.showinfo("Invalid Value!","Please submit a valid number for Discount")
            return 
        
       

        if type is "add":
            data = (productIds[:-1], self.discountAmountEntry.get(), self.promoCodeEntry.get())
            self.dbController.addDiscount(data)
            self.showDiscounts()
            self.addWindow.destroy()
        elif type is "change":
            data = (self.id, productIds, self.discountAmountEntry.get(), self.promoCodeEntry.get())
            # self.dbController.changeDiscount(data)
            
            self.showDiscounts()
            self.changeWindow.destroy()
        
        


        #Send data
        #refresh buttons




    def removeDiscount(self):
       
        print (self.individualDiscount.get())
        for i in self.discountButtons:
            
            if i[0] == self.individualDiscount.get() +1:
                
                self.dbController.removeDiscount(i[1].split(' ')[0])
                self.showDiscounts()
                break
        
        
    
    def getDataFromTitle(self):
        for i in self.discountButtons:
            if i[0] == self.individualDiscount.get() +1:
                titleList = i[1].split(' - ')
                self.id = titleList[0]
                self.productNames = titleList[1].split(',')
                self.discountAmount = titleList[2]
                self.promoCode = titleList[3]

        return (self.id, self.productNames, self.discountAmount, self.promoCode)
                

    def changeDiscount(self):


        self.changeWindow = Tk()
        self.changeWindow.title("Change Discount Scheme")

        frame = Frame(self.changeWindow)

        title = Label(frame, text="Change discount", font="Courier 17 bold")
        title.grid(row="0",column="1")

        productLabelFrame = LabelFrame(frame, text="Products")
        
        self.checkProducts = self.getDataFromTitle()

        self.addProductsToLabelFrame(productLabelFrame, self.checkProducts[1])
    
        discountAmountLabel=Label(frame, text="Discount:", font="Courier 12 bold")
        discountAmountLabel.grid(row="2", column="0",pady=20)

        discountAmount_string = StringVar()
        
        self.discountAmountEntry=Entry(frame, width=15, textvariable=discountAmount_string)
        self.discountAmountEntry.insert(0,self.checkProducts[2])
        self.discountAmountEntry.grid(row="2", column="1")

        promoCodeLabel=Label(frame, text="Promo code:", font="Courier 12 bold")
        promoCodeLabel.grid(row="3", column="0")

        promoCode_string = StringVar()
        self.promoCodeEntry=Entry(frame, width=15, textvariable=promoCode_string)
        self.promoCodeEntry.grid(row="3", column="1",pady=20)
        self.promoCodeEntry.insert(0,self.checkProducts[3])


        self.changeDiscountButton = Button(frame, text="Change Discount Scheme", command = lambda : self.sendData("change"))
        self.changeDiscountButton.grid(row="4",column="1")
        productLabelFrame.grid(row="1", column="1")
        frame.pack()
        
        
        


