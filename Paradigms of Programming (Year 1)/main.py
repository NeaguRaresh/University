
import tkinter as tk
from tkinter.font import Font
from tkinter import *
from tkinter import messagebox
import sqlite3
from contextlib import closing

from loginWindow import *
from discount import *
from dbController import *

db = dbController()

productName = []
productPrice = []
storeWindow = tk.Tk()
storeWindow.title("The Store")
storeWindow.geometry("600x700")


def getDiscountScheme():

    discounts = db.getDiscounts()
    productIdName = db.getProductsIdName()
        
    fullText = []
    for discount in discounts:
            
        productsToAplly = discount[1].split(',')
        text = ""
        for prodcut in productsToAplly:
                
            for id in productIdName:
                if prodcut == id[0]:
                    text += ", " + str(id[1])
                    break

        fullText.append((text[2:] , discount[2] , discount[3]))

    return fullText

def products ():
    con = sqlite3.connect('./Done/db/products.db')  # creates a connection with the database
    cur = con.cursor()  # allows me to send SQL statements to the database
    data = cur.execute('SELECT productName, price FROM products').fetchall()
    print(data)

    product = []

    for item in data:
        products = ("%s, %s" % item)
        product.append(products)

    for item in product:
        fields = item.split(",")
        name = fields[0]
        price = fields[1]

        productName.append(name)
        productPrice.append(price)

        name_Label = LabelFrame(storeWindow, text=name, font =("Candara", 15), fg = 'White',)
        name_Label.pack(side = 'left',)

        price_label = LabelFrame(storeWindow, text=price, font=('Candara', 15), fg='red')
        price_label.pack(side='right')

    con.commit()
    closing(sqlite3.connect('Products.db'))
products()

def openLogin():
     
    LoginWindow()

def showStore():
    global storeWindow

    staffLoginButton = Button(storeWindow, text="Staff Login", command=lambda : openLogin())
    staffLoginButton.pack(side="top")

    storeLabelFrame = LabelFrame(storeWindow, text="Store Items")
    storeLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    storeItemsFrame = Frame(storeLabelFrame)
    storeItemsFrame.pack(padx="10", pady="6")

    for item in productName:

        IndexOfName = productName.index(item)
        priceIndex = productPrice[IndexOfName]
        Price = ("£" + priceIndex)

        itemFrame = Frame(storeItemsFrame, pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=item, font=("Candara", 15), fg="Blue")
        nameLabel.pack(side="left")

        price_label = Label(itemFrame, text=Price, font=('Candara', 15), fg='red')
        price_label.pack(side='left')

        AddToCartButton = Button(itemFrame, text="Add to cart", font=('Candara', 15),
                                 command=lambda i=item: addItemToCart(i))
        AddToCartButton.pack(side="right")

    btnGoCart = Button(storeWindow, text="Go To Cart", font=("Candara", 15, "bold"),
                       fg="red", bg="white", cursor="hand2", command=cart)
    btnGoCart.pack(pady="6")

def cart():
    cartWindow = Toplevel()
    cartWindow.title("Shopping Basket")
    cartWindow.geometry("400x500")

    cartItems = cartFunction.getCartItems()

    cartItemsLabelFrame = LabelFrame(cartWindow, text="Cart Items")
    cartItemsLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    cartItemsFrame = Frame(cartItemsLabelFrame, padx=3, pady=3)
    cartItemsFrame.pack()

    priceCalculation = 0
    index = 0
    for item in cartItems:
        IndexOfName = productName.index(item)
        priceIndex = productPrice[IndexOfName]
        Price = ("£" + priceIndex)

        itemFrame = Frame(cartItemsFrame, pady="5")
        itemFrame.pack(fill="both", expand="yes")
        nameLabel = Label(itemFrame, text=item, font=("Candara", 15), fg="blue")
        priceLabel = Label(itemFrame, text=Price, font=("Candara", 13), fg="red")
        addToCartBtn = Button(itemFrame, text="Remove From Cart", font=("Candara", 11, "bold"), fg="red", bg="white",
                              cursor="hand2", command=lambda i=index: removeFromCart(i, cartWindow))

        nameLabel.pack(side="left")
        priceLabel.pack(side="left")
        addToCartBtn.pack(side="right")

        priceCalculation = priceCalculation + int(float(priceIndex))
        index += 1

    checkOutFrame = Frame(cartWindow, pady="10")


    DiscountFrame = Frame(cartWindow)
    DiscountEntryUser = StringVar()
    DiscountLabel = Label(DiscountFrame, text="Please enter the discount code", fg='Blue')
    DiscountLabel.pack()
    DiscountEntry = Entry(DiscountFrame, textvariable=DiscountEntryUser)
    DiscountEntry.pack(pady=20, side="left")

    #DiscountPrice = StringVar()

    DiscoutnApply = Button(DiscountFrame, text="Apply Discount",
                           command=lambda :applyDiscount(priceCalculation, DiscountEntry, DiscountPriceLabel, cartItems))
    DiscoutnApply.pack(pady=20, side="left")

    DeliveryFrame = Frame(cartWindow)
    deliveryLabel = Label(DeliveryFrame, text="Please select a delivery option and click on Update", fg='Blue')
    deliveryLabel.pack()

    deliveryTypes = [
        "Standard Delivery - £3.50",
        "First Class - £5.00",
        "Second Class - £2.00",
    ]

    clicked = StringVar(DeliveryFrame)
    clicked.set(deliveryTypes[0])

    drop = OptionMenu(DeliveryFrame, clicked, *deliveryTypes)
    drop.pack(pady=20)
    str_out = StringVar(DeliveryFrame)
    str_out.set('Output')

    str_outBtn = Button(DeliveryFrame, text='Update', command=lambda: my_show())
    str_outBtn.pack()

    l2 = Label(DeliveryFrame, textvariable=str_out)
    l2.pack()

    DiscountPriceLabel = Label(cartWindow, text="Discount Price : £ %s" % priceCalculation,
                               font=("Candara", 14, "bold"), fg="indigo")
    DiscountPriceLabel.pack(side="top")
    global ActualPrice
    ActualPrice=priceCalculation

    totalPriceLabel = Label(cartWindow, text="Total Price : £ %s" % priceCalculation,
                            font=("Candara", 14, "bold"), fg="indigo")
    totalPriceLabel.pack()

    paymentFrame = Frame(cartWindow, pady="10")

    PaymentButton = Button(cartWindow, text="Payment", command=lambda:Payment(ActualPrice))
    PaymentButton.pack(side="bottom")

    #paymentFrame.pack()

    def my_show():
        global ActualPrice
        str_out.set(clicked.get())
        if 'First Class' in clicked.get():
            ActualPrice=ActualPrice + 5
            totalPriceLabel.config(text="Total Price : £ %s" % str(ActualPrice))
        elif 'Standard Delivery' in clicked.get():
            ActualPrice=ActualPrice+3.50
            totalPriceLabel.config(text="Total Price : £ %s" % str(ActualPrice))
        else:
            ActualPrice=ActualPrice+2
            totalPriceLabel.config(text="Total Price : £ %s" % str(ActualPrice))


    checkOutFrame.pack()
    DiscountFrame.pack()
    DeliveryFrame.pack()
    paymentFrame.pack()

def applyDiscount(priceCalculation, DiscountEntry, DiscountPrice, cartItems):
    global ActualPrice
    
    discounts = getDiscountScheme()
    print(discounts)
    print(cartItems)
    # if DiscountEntry.get() == 'OFF':
    #     ActualPrice= round(priceCalculation-(priceCalculation * 0.20), 2)
    #     DiscountPrice.config(text='Discount Price is : £ %s' %ActualPrice)

    for discount in discounts:

        #Check if they have an valid DiscountCode
        if DiscountEntry.get() in discount[2]:

            #Check if it applies to this product
            for product in cartItems:
                if product in discount[0] or len(discount[0]) == 0:
                    print(priceCalculation)
                    print(int(discount[1]) / 100)
                    print(priceCalculation * int(discount[1]) / 100 )
                    ActualPrice = round(priceCalculation -(priceCalculation * ( int(discount[1]) / 100 )),2)
                    DiscountPrice.config(text='Discount Price is : £ %s' %ActualPrice)




def Payment(ActualPrice):
    PaymentWindow = Toplevel()
    PaymentWindow.title("Payment")
    PaymentWindow.geometry("700x400")

    con = sqlite3.connect('Customer.db')  # creates a connection with the database
    cur = con.cursor()  # allows me to send SQL statements to the database

#CREATING SUBMIT FUNCTION
    def submit():
        con = sqlite3.connect('Customer.db')
        cur = con.cursor()

    # INSERTING VALUES INTO DATABASE
        cur.execute("INSERT INTO Customer (f_name, l_name, address, city, postcode,"
                    "nameonCard, cardNumber, expiryDate, cvv)"" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        f_name.get(),
                        l_name.get(),
                        address.get(),
                        city.get(),
                        postcode.get(),
                        nameonCard.get(),
                        cardNumber.get(),
                        expiryDate.get(),
                        cvv.get()
                    ))
        con.commit()
        closing(sqlite3.connect('Customer.db'))

     # clear text boxes after one entry
        f_name.delete(0, END)
        l_name.delete(0, END)
        address.delete(0, END)
        city.delete(0, END)
        postcode.delete(0, END)
        nameonCard.delete(0, END)
        cardNumber.delete(0, END)
        expiryDate.delete(0, END)
        cvv.delete(0, END)

#CREATING TEXT BOXES
    f_name = Entry(PaymentWindow, width=30)
    f_name.grid(row=0, column=1, padx=20)
    l_name = Entry(PaymentWindow, width=30)
    l_name.grid(row=1, column=1)
    address = Entry(PaymentWindow, width=30)
    address.grid(row=2, column=1)
    city = Entry(PaymentWindow, width=30)
    city.grid(row=3, column=1)
    postcode = Entry(PaymentWindow, width=30)
    postcode.grid(row=4, column=1)

# Create text box labels
    f_name_label = Label(PaymentWindow, text="First Name")
    f_name_label.grid(row=0, column=0)
    l_name_label = Label(PaymentWindow, text="Last Name")
    l_name_label.grid(row=1, column=0)
    address_label = Label(PaymentWindow, text="Address")
    address_label.grid(row=2, column=0)
    city_label = Label(PaymentWindow, text="City")
    city_label.grid(row=3, column=0)
    postcode_label = Label(PaymentWindow, text="Postcode")
    postcode_label.grid(row=4, column=0)

    user_input = f_name.get(), l_name.get()

    # MAKING LABELS FOR THE CARD DETAILS

    nameonCard_Label = Label(PaymentWindow, text="Name on Card")
    nameonCard_Label.grid(row=8, column=0)
    cardNumber_label = Label(PaymentWindow, text="Card Number")
    cardNumber_label.grid(row=9, column=0)
    expiryDate_label = Label(PaymentWindow, text="Expiry Date")
    expiryDate_label.grid(row=10, column=0)
    CVV_label = Label(PaymentWindow, text="CVV")
    CVV_label.grid(row=11, column=0)

# TAKING CARD DETAILS, CREATING ENTRY BOXES
    nameonCard = Entry(PaymentWindow,  width=30)
    nameonCard.grid(row=8, column=1)
    cardNumber = Entry(PaymentWindow, width=30)
    cardNumber.grid(row=9, column=1)
    expiryDate = Entry(PaymentWindow, width=30)
    expiryDate.grid(row=10, column=1)
    cvv = Entry(PaymentWindow, width=30)
    cvv.grid(row=11, column=1)

#TOTAL TO PAY
    totalPriceLabel = Label(PaymentWindow, text="Total Price : £ %s" %ActualPrice,
                            font=("Candara", 14, "bold"), fg="indigo")
    totalPriceLabel.grid(row=12, column=2)

#VALIDATION CHECK
    def check():
        sum_gss_10 = []
        gss_or_equ10 = []
        lss10 = []
        odd = []
        valid = list(cardNumber.get())
        for i in range(0, len(valid), 2):
            ss = int(valid[i]) * 2
            if (ss >= 10):
                gss_or_equ10.append(ss)
            else:
                lss10.append(ss)
        for j in range(0, len(gss_or_equ10)):
            io = str(gss_or_equ10[j])
            dim = 0
            for i in io:
                dim = int(dim) + int(i)
            sum_gss_10.append(dim)
        dim = 0
        for n in sum_gss_10:
            dim = dim + n
        lim = 0
        for l in lss10:
            lim = lim + l
        sid = dim + lim
        for i in range(1, len(valid), 2):
            ss = int(valid[i])
            odd.append(ss)
        lid = 0
        for u in odd:
            lid = lid + u
        mid = sid + lid
        rim = mid % 10
        if (rim == 0):
            messagebox.showinfo("Validation Details", "It's Valid Card")
            print("it's a valid credit card & Check Sum ", mid)
        else:
            messagebox.showinfo("Validation Details", "Invalid Card")
            print("Invalid Card")

    CheckCard=Button(PaymentWindow, text="Credit Card Check!", font=("verdana", 14), command=check)
    CheckCard.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # CREATING SUBMIT BUTTON
    submit_btn = Button(PaymentWindow, text="Pay now", command=submit)
    submit_btn.grid(row=13, column=2, columnspan=2, pady=10, padx=10, ipadx=100)

    con.commit()
    closing(sqlite3.connect('Customer.db'))

    receiptButton = Button(PaymentWindow, text="Receipt", command=receipt)
    receiptButton.grid(row=16, column=2)

    #paymentFrame.pack()

def receipt():
    receiptWindow = Toplevel()
    receiptWindow.title("Receipt")
    receiptWindow.geometry("700x400")
    cartItems = cartFunction.getCartItems()
    for item in cartItems:
        IndexOfName = productName.index(item)
        priceIndex = productPrice[IndexOfName]
        Price = ("£" + priceIndex)

        itemFrame = Frame(receiptWindow, pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(receiptWindow, text=item, font=("Candara", 15), fg="blue")
        nameLabel.pack()
        priceLabel = Label(receiptWindow, text=Price, font=("Candara", 13), fg="red")
        priceLabel.pack()



    showButton = Button(receiptWindow, text="Show Receipt", command=cartItems)
    showButton.pack()

    totalPriceLabel = Label(receiptWindow, text="Total Price : £ %s" % ActualPrice,
                            font=("Candara", 14, "bold"), fg="indigo")
    totalPriceLabel.pack()


def addItemToCart(item=None):
    global cartFunction
    cartFunction.addToCart(item)
    messagebox.showinfo(title="Success" , message="Item %s Added To The Cart !!"%item)

def removeFromCart(itemIndex=None,cartWindow=None):
    global cartFunction
    cartFunction.removeFromCart(itemIndex)
    messagebox.showinfo(title="success",message="Item Removed")
    cartWindow.destroy()
    cart()

class ShoppingCart:
    def __init__(self):
        self.items = []

    def addToCart(self, item):
        self.items.append(item)
        print(self.items)

    def removeFromCart(self, itemIndex):
        self.items.pop(itemIndex)

    def getCartItems(self):
        return self.items

class CreditCard:
    def __init__(self,card_no):
        self.card_no = card_no

cartFunction = ShoppingCart()

showStore()
storeWindow.mainloop()

