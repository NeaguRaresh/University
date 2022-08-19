############################
##                        ##
##   NEAGU RARES CRISTIAN ##
##   STUNDET ID:001136056 ##
############################
import sqlite3
import datetime
import re

class dbController:

    def __init__(self):
        pass


    #Uses uid and passwd to check if there is a row with that information
    #returns a touple if it find one, None otherwise
    def check_user_login(self, uid, passwd):

        #Open admins database file
        connection = sqlite3.connect('./db/admins.db')
        cursor = connection.cursor()

        #SQL query to find the row and get all information
        cursor.execute("SELECT * FROM admins WHERE uid= ? AND password = ?", (uid, passwd, ))
        retValue = cursor.fetchall()
        
        connection.close()

        #Check if there is an user with 'uid' and 'passwd' 
        if len(retValue) is 0:
            return None
        else:
            return retValue

    
    #Returns a list containing all unanswerd queries;
    #List itmes are dicts with all the information needed
    def get_query_list(self):

        #OPEN Queries database file
        connection = sqlite3.connect('./db/queries.db')
        cursor = connection.cursor()

        #Get all unopened Queries
        queries = cursor.execute("SELECT * FROM queries WHERE seen=0").fetchall()

        connection.close()

        #OPEN Customers database file
        connection = sqlite3.connect('./db/customers.db')
        cursor = connection.cursor()

        #Define SQL query
        sqlQuery = "SELECT first_name, last_name FROM customers where customerID=?"


        query_list = []
        for queryItem in queries:

            #Find the name of the customer that placed the 'queryItem' query
            name = ' '.join(cursor.execute(sqlQuery, (queryItem[1],)).fetchone())

            #Create dict with all the necesary information for display
            query = {
                'id' : queryItem[0],
                'customer': name,
                'text': queryItem[2],
                'date': queryItem[3]
            }

            #Add to the list
            query_list.append(query)

        connection.close()
        return query_list

    #Returns the number of unaswered queries
    def get_query_count(self):
            
        connection = sqlite3.connect('./db/queries.db')
        cursor = connection.cursor()

        sql_query = "SELECT COUNT(*) FROM queries where seen=0"

        cursor.execute(sql_query)

        retValue = cursor.fetchall()[0][0]
        connection.close()
        return retValue
            
    #Returns the number of unaswerd reviews
    def get_review_count(self):
        connection = sqlite3.connect('./db/queries.db')
        cursor = connection.cursor()

        sql_query = "SELECT COUNT(*) FROM reviews where seen=0"

        cursor.execute(sql_query)

        retValue = cursor.fetchall()[0][0]
        connection.close()
        return retValue


    #Updates queries with a response
    def updateQueryResponse(self, responseData):
        

        connection = sqlite3.connect('./db/queries.db')
        cursor = connection.cursor()

        #Set query as seen 
        cursor.execute("UPDATE queries SET seen=1 WHERE queryID=?",[responseData[0]])
        connection.commit()
        
        #GET response ID
        cursor.execute("SELECT responseID from response")

        #Get all IDs
        ids = cursor.fetchall()
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")

        #Determine the ID
        if len(ids) is 0:
            responseID = "res1"
            #Add to db
            cursor.execute("""INSERT INTO response VALUES(
                ?,
                ?,
                ?,
                ?,
                ?
            )""", (responseID,responseData[0],responseData[1],responseData[2], now ))
            connection.commit()
        else:
            last_id = ids[len(ids)-1][0]
            responseID = "res" + str(int(re.match(r'([A-Za-z]+)([0-9]+)', last_id).groups()[1]) + 1)
            #Add to db
            cursor.execute("""INSERT INTO response VALUES(
                ?,
                ?,
                ?,
                ?,
                ?
            )""", (responseID,responseData[0],responseData[1],responseData[2], now ))
            connection.commit()
        

        connection.commit()
        connection.close()

    def updateReviewResponse(self, responseData):

        connection = sqlite3.connect('./db/queries.db')
        cursor = connection.cursor()

        cursor.execute("UPDATE reviews SET seen = 1 WHERE reviewID=?",[responseData[0]])
        connection.commit()
        
        cursor.execute("SELECT responseID FROM reviewResponse")
        
        ids = cursor.fetchall()
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")

        if len(ids) is 0:
            responseID = "res1"

            cursor.execute("""INSERT INTO reviewResponse VALUES(
                ?,
                ?,
                ?,
                ?,
                ?
            )""", (responseID,responseData[0],responseData[1],responseData[2], now ))
            connection.commit()
        else:
            last_id = ids[len(ids)-1][0]
            responseID = "res" + str(int(re.match(r'([A-Za-z]+)([0-9]+)', last_id).groups()[1]) + 1)

            cursor.execute("""INSERT INTO reviewResponse VALUES(
                ?,
                ?,
                ?,
                ?,
                ?
            )""", (responseID,responseData[0],responseData[1],responseData[2], now ))
            connection.commit()
            connection.close()


    def get_review_list(self):

        #Get All reviews
        connection = sqlite3.connect('./db/queries.db')
        c= connection.cursor()

        c.execute("SELECT * FROM reviews")
        allReviews = c.fetchall()

        connection.close()

        userConn = sqlite3.connect('./db/customers.db')
        userCurr = userConn.cursor()

        prodConn = sqlite3.connect('./db/products.db')
        prodCurr = prodConn.cursor()

        findUser_sql = "SELECT first_name, last_name FROM customers WHERE customerID=?"
        findProduct_sql = "SELECT productName FROM products WHERE productID=?"

        reviewList = []
        for review in allReviews:
            name = ' '.join(userCurr.execute(findUser_sql, (review[1],)).fetchone())
            product = prodCurr.execute(findProduct_sql, [review[2]]).fetchone()[0]

            review = {
                'id' : review[0],
                'customer': name,
                'product' : product, 
                'text': review[3],
                'date': review[4]
            }
            reviewList.append(review)

        userConn.close()
        prodConn.close()
        return reviewList

    def getProductIdName(self):

        connection = sqlite3.connect('./db/products.db')
        cursor = connection.cursor()

        cursor.execute("SELECT productID, productName FROM products")
        retValue = cursor.fetchall()

        connection.close()
        return retValue

    #Get a list woth prodcut names
    #Returns a dictionary with productName as key and quantity and month as values
    def getSalesForProduct(self, productLsit, monthList):

        conn = sqlite3.connect('./db/products.db')
        cursor = conn.cursor()

        productIds = []
        sql_query = "SELECT productID FROM products WHERE productName=?"

        for product in productLsit:
            cursor.execute(sql_query, [product])
            productIds.append((product, cursor.fetchone()[0]))

       
        conn.close()

        conn = sqlite3.connect('./db/sales.db')
        cursor = conn.cursor()
        

        sales = dict.fromkeys(productLsit)
        for product in productIds:
            montlySale = dict.fromkeys(monthList)
            for month in monthList:

                cursor.execute("SELECT unitsSold FROM sales where productID = ? and month = ?", (product[1], month, ))
                
                # a = ( product[0], month, cursor.fetchall()[0][0])
                # sales.append(a)

                montlySale[month] = int(cursor.fetchall()[0][0])
                sales[product[0]] = montlySale
        
        return sales

    def getDiscounts(self):
        connection = sqlite3.connect('./db/discount.db')
        cursor = connection.cursor()

        sql_query = "SELECT * FROM discount"

        cursor.execute(sql_query)
        return cursor.fetchall()
    
    def getProductsIdName(self):
        connection = sqlite3.connect('./db/products.db')
        cursor = connection.cursor()

        sql_query = "SELECT productID, productName From products"
        cursor.execute(sql_query)
        return cursor.fetchall()

    def removeDiscount(self, id):
        

        connection = sqlite3.connect('./db/discount.db')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM discount WHERE discountID = ?", [id])
        

        connection.commit()
        connection.close()

    def changeDiscount(self, data):

        connection = sqlite3.connect('./db/discount.db')
        cursor = connection.cursor()

        sqlquery = "UPDATE discount SET productsID = ? , discountAmount = ? , promoCode = ? WHERE discountID = ?"

        
        cursor.execute(sqlquery, (str(data[1]), str(data[2]), str(data[3]),str(data[0])))

        connection.commit()
        connection.close()
        
    def addDiscount(self, data):

        connection = sqlite3.connect('./db/discount.db')
        cursor = connection.cursor()

        cursor.execute("SELECT discountID from discount")

        ids = cursor.fetchall()
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")

        if len(ids) is 0:
            responseID = "disc1"

            cursor.execute("""INSERT INTO discount VALUES(
                ?,
                ?,
                ?,
                ?
                
            )""", (responseID,data[0],data[1],data[2] ))
            connection.commit()
        else:
            last_id = ids[len(ids)-1][0]
            responseID = "disc" + str(int(re.match(r'([A-Za-z]+)([0-9]+)', last_id).groups()[1]) + 1)

            cursor.execute("""INSERT INTO discount VALUES(
                ?,
                ?,
                ?,
                ?
                
            )""", (responseID,data[0],data[1],data[2] ))
            connection.commit()
        connection.close()
    
    def getNamePriceProducts(self):
        connection = sqlite3.connect('./db/products.db')
        cursor = connection.cursor()

        cursor.execute("SELECT productName, price FROM products")
        print(cursor.fetchall())            

def main():
    a = dbController()
    a.getNamePriceProducts()
main()


