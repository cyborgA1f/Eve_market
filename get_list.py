import urllib.request
import xml.etree.ElementTree as ET
#from time import gmtime, strftime
import sqlite3

def lerning_XML():
    tag = input('enter tag:')
    url = 'https://api.eve-central.com/api/quicklook?typeid='+str(tag)
    response = urllib.request.urlopen(url)
    data = response.read()
    tree = ET.XML(data)
    return tree

def data_sqlite():
    conn = sqlite3.connect('Eve_online.db')
    c = conn.cursor()
    """"
    try:
        c.execute("DROP TABLE Sall_order")
        c.execute("DROP TABLE Buy_order")
        c.execute("DROP TABLE marker")
    except sqlite3.OperationalError as drop:
       print(drop)
    """
    try:
        c.execute("CREATE TABLE market("
              "Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
              " ItemId INTEGER,"
              " SallId INTEGER REFERENCES Sall_order (Id),"
              " BuyId  INTEGER REFERENCES Buy_order (Id))")

        c.execute("CREATE TABLE Sall_order("
              "Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
              " Region INTEGER,"
              " Security FLOAT,"
              " Station STRING, "
              "Price FLOAT)")

        c.execute("CREATE TABLE Buy_order("
              "Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
              " Region INTEGER,"
              " Security FLOAT,"
              " Station STRING, "
              "Price FLOAT)")
    except sqlite3.OperationalError as creat:
        print(creat)
    conn.commit()
    c.close()
    conn.close()

def filling_DB():
    data_sqlite()
    a = lerning_XML()
    buy = a.findall('quicklook/buy_orders/order')
    sall = a.findall('quicklook/sell_orders/order')

    conn = sqlite3.connect('Eve_online.db')
    c=conn.cursor()

    for ord in buy:
        price = ord.findtext('price')
        station_name = ord.findtext('station_name')
        security = ord.findtext('security')
        region = ord.findtext('region')
        tablet = [int(region), float(security), str(station_name) ,float(price)]
        c.execute("INSERT INTO Buy_order(Region, Security, Station, Price) VALUES (?, ?, ?, ?)",tablet)
    for ord in sall:
        price = ord.findtext('price')
        station_name = ord.findtext('station_name')
        security = ord.findtext('security')
        region = ord.findtext('region')
        tablet = [int(region), float(security), str(station_name) ,float(price)]
        c.execute("INSERT INTO Sall_order(Region, Security, Station, Price) VALUES (?, ?, ?, ?)",tablet)
    conn.commit()
    c.close()
    conn.close()

def main():
    #data_sqlite()
    filling_DB()
    #lerning_XML()

if __name__ == '__main__':
    main()