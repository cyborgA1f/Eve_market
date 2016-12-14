#!/usr/bin/python
# -*- coding: utf-8 -*-

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

def data_sqlite():#создание таблици
    conn = sqlite3.connect('Eve_online.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Sall_order")
    c.execute("DROP TABLE IF EXISTS Buy_order")
    c.execute("CREATE TABLE IF NOT EXISTS market(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Item_ID INTEGER REFERENCES Item (Id), Sall_ID INTEGER REFERENCES Sall_order (Id), Buy_ID  INTEGER REFERENCES Buy_order (Id))")
    c.execute("CREATE TABLE IF NOT EXISTS Sall_order(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Region INTEGER, Security FLOAT, Station STRING, Price FLOAT)")
    c.execute("CREATE TABLE IF NOT EXISTS Buy_order(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Region INTEGER, Security FLOAT, Station STRING, Price FLOAT)")
    c.execute("CREATE TABLE IF NOT EXISTS Region(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Name STRING)")
    c.execute("CREATE TABLE IF NOT EXISTS Security(Id INTEGER, Status FLOAT)")
    c.execute("CREATE TABLE IF NOT EXISTS Station(Id INTEGER PRIMARY KEY NOT NULL, Region_ID INTEGER REFERENCES Region (Id), Security_ID INTEGER REFERENCES Security (Id), Name STRING)")
    c.close()
    conn.close()

def filling_DB(): #Заполнение таблици данными
    data_sqlite()
    a = lerning_XML()
    buy = a.findall('quicklook/buy_orders/order')
    sall = a.findall('quicklook/sell_orders/order')

    cread_tablet = ['Buy_order', 'Sall_order']

    conn = sqlite3.connect('Eve_online.db')
    c=conn.cursor()

    for ord in buy:
        price = ord.findtext('price')
        station_name = ord.findtext('station_name')
        security = ord.findtext('security')
        region = ord.findtext('region')
        tablet = [int(region), float(security), str(station_name) ,float(price)]
        c.execute("INSERT INTO Buy_order(Region, Security, Station, Price) VALUES (?, ?, ?, ?)", tablet)
    for ordd in sall:
        price = ordd.findtext('price')
        station_name = ordd.findtext('station_name')
        security = ordd.findtext('security')
        region = ordd.findtext('region')
        tablet = [int(region), float(security), str(station_name) ,float(price)]
        c.execute("INSERT INTO Sall_order(Region, Security, Station, Price) VALUES (?, ?, ?, ?)",tablet)
    c.close()
    conn.close()

def main():
    filling_DB()

if __name__ == '__main__':
    main()