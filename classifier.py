from collections import _OrderedDictKeysView
from dataclasses import dataclass
import sqlite3
import csv
from dataclasses import dataclass

@dataclass
class orderData:
    orderdate: str 
    title: str
    category: str
    itemtotal: str
    totalcharge: str
    payment: str 
    orderid: str
    carriertracking: str
    itemid: str


CreateOrderTable = """ CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        orderdate TEXT,
                        orderID TEXT,
                        payment TEXT,
                        website TEXT,
                        purchaseOrderNumber TEXT,
                        ordercustomeremail TEXT,
                        shipmentdate TEXT,
                        shippingaddressname TEXT,
                        shippingaddressstreet1 TEXT,
                        shippingaddressstreet2 TEXT,
                        shippingaddresscity TEXT,
                        shippingaddressstate TEXT,
                        shippingaddresszip TEXT,
                        orderstatus TEXT,
                        carriertracking TEXT,
                        subtotal TEXT,
                        shippingcharge TEXT,
                        taxbeforepromo TEXT,
                        totalpromos TEXT,
                        taxcharged TEXT,
                        totalcharge TEXT,
                        buyername TEXT,
                        groupname TEXT);
                        """

CreateItemTable = """ CREATE TABLE IF NOT EXISTS items (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      orderdate TEXT,
                      orderid TEXT,
                      title TEXT,
                      category TEXT,
                      isbn TEXT,
                      unspccode TEXT,
                      website TEXT,
                      releasedate TEXT,
                      condition TEXT,
                      seller TEXT,
                      sellercreds TEXT,
                      listprice TEXT,
                      purchaseprice TEXT,
                      quantity TEXT,
                      paymenttype TEXT,
                      ponum TEXT,
                      poline TEXT,
                      customeremail TEXT,
                      shipmentdate TEXT,
                      shippingaddressname TEXT,
                      shippingaddressstreet1 TEXT,
                      shippingaddressstreet2 TEXT,
                      shippingaddresscity TEXT,
                      shippingaddressstate TEXT,
                      shippingaddresszip TEXT,
                      orderstatus TEXT,
                      carriertracking TEXT,
                      itemsubtotal TEXT,
                      itemsubtotaltax TEXT,
                      itemtotal TEXT,
                      taxexemption TEXT,
                      taxexemptiontype TEXT,
                      taxexemptionoptout TEXT,
                      buyername TEXT,
                      currency TEXT,
                      groupname TEXT);
                      """

CreateCategoriesTable = """CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category TEXT);"""

InsertOrderItem = """INSERT INTO orders (orderdate,
                                        orderID,
                                        payment,
                                        website,
                                        purchaseOrderNumber,
                                        ordercustomeremail,
                                        shipmentdate,
                                        shippingaddressname,
                                        shippingaddressstreet1,
                                        shippingaddressstreet2,
                                        shippingaddresscity,
                                        shippingaddressstate,
                                        shippingaddresszip,
                                        orderstatus,
                                        carriertracking,
                                        subtotal,
                                        shippingcharge,
                                        taxbeforepromo,
                                        totalpromos,
                                        taxcharged,
                                        totalcharge,
                                        buyername,
                                        groupname)
                                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                  """
InsertItemItem = """INSERT INTO items (orderdate, 
                                    orderid,
                                    title,
                                    category,
                                    isbn,
                                    unspccode,
                                    website,
                                    releasedate,
                                    condition,
                                    seller,
                                    sellercreds,
                                    listprice,
                                    purchaseprice,
                                    quantity,
                                    paymenttype,
                                    ponum,
                                    poline,
                                    customeremail,
                                    shipmentdate,
                                    shippingaddressname,
                                    shippingaddressstreet1,
                                    shippingaddressstreet2,
                                    shippingaddresscity,
                                    shippingaddressstate,
                                    shippingaddresszip,
                                    orderstatus,
                                    carriertracking,
                                    itemsubtotal,
                                    itemsubtotaltax,
                                    itemtotal,
                                    taxexemption,
                                    taxexemptiontype,
                                    taxexemptionoptout,
                                    buyername,
                                    currency,
                                    groupname) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
"""

InsertCategoryItem = """INSERT INTO categories (category) VALUES (?)"""
SelectItems = """SELECT items.orderdate, items.title, items.category, items.itemtotal, orders.totalcharge, orders.payment,  orders.orderid, orders.carriertracking, items.id FROM items INNER JOIN orders on items.carriertracking = orders.carriertracking AND items.orderid = orders.orderid ORDER by orders.orderdate DESC, orders.totalcharge DESC"""                

def loadreports(conn, orderCSV, itemCSV, categories):
    '''Load the amazon reports into CSV'''

    with conn:
        cur = conn.cursor()
        #Create Tables
        cur.execute(CreateItemTable)
        cur.execute(CreateOrderTable)
        cur.execute(CreateCategoriesTable)
        
        orders=csv.reader(open(orderCSV,encoding='utf-8'))
        items=csv.reader(open(itemCSV,encoding='utf-8'))
        categories=csv.reader(open(categories,encoding='utf-8'))

        for r in orders:
            #print(r)
            cur.execute(InsertOrderItem, r)
            #print(cur.rowcount)

        for r in items:
            cur.execute(InsertItemItem, r)
        
        for r in categories:
            cur.execute(InsertCategoryItem, r)





def orderDataFactory(cursor,row):
    r = orderData(*row)
    return r

def getData(conn):
    '''load combined data'''
    itemlist=[]
    conn.row_factory=orderDataFactory
    with conn:
        cur = conn.cursor()
        cur.execute(SelectItems)
        rows = cur.fetchall()
        for r in rows:
            itemlist.append(r)
    return(itemlist)

def getCategories(conn):
    categories=[]
    conn.row_factory=None
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT category FROM categories")
        rows = cur.fetchall()
        for r in rows:
            categories.append(r[0])
    return categories
