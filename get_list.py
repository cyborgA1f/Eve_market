#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import xml.etree.ElementTree as ET
import sqlite3

def lerning_XML(): #Получение полного списка ордеров
    print("Получаем список:", end='')
    tag = 34 # input('enter tag:')
    url = 'https://api.eve-central.com/api/quicklook?typeid='+str(tag)
    response = urllib.request.urlopen(url)
    data = response.read()
    print("Ok")
    tree = ET.XML(data)
    return tree

def creating_tables():#создание таблици в sylite
    print('Создание таблици:', end='')
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
    conn.commit()
    c.close()
    conn.close()
    print('Ok')

def filling_DB(): #Заполнение даных полученых с сайта eve-central.com
    creating_tables()
    a = lerning_XML()
    buy = a.findall('quicklook/buy_orders/order')
    sall = a.findall('quicklook/sell_orders/order')

    print("Заполняем таблицу:", end=" ")
    conn = sqlite3.connect('Eve_online.db')
    c = conn.cursor()
    orders = {"Buy_order": buy, "Sall_order": sall}
    for key in orders:
        for item in orders[key]:
            price = item.findtext('price')
            station_name = item.findtext('station_name')
            security = item.findtext('security')
            region = item.findtext('region')
            tablet = [int(region), float(security), str(station_name) ,float(price)]
            c.execute("INSERT INTO " + key + "(Region, Security, Station, Price) VALUES (?, ?, ?, ?)", tablet)
    conn.commit()
    c.close()
    conn.close()
    print("OK")

def Instrt_data(): #Выборка с базы данных
    a = lerning_XML()
    info = a.findall('quicklook')
    for item in info:
        itemname = item.findtext('itemname')
        print(itemname)
    conn=sqlite3.connect('Eve_online.db')
    c=conn.cursor()
    c.execute('select * from Sall_order')
    data = c.fetchall()
    a=0
    for dat in data:
        sell = (dat[-1])
        a+=sell
    f=a/len(data)
    print("Средняя цена:", round(f, 2))

def main():
    print("Заполнения базы данных(1)\nПолучения получение среднего значения(2)\nВыход(0)")
    a = int(input("Введите значение:"))
    if a == 1:
        filling_DB()
    elif a== 2:
        Instrt_data()
    else:
        print("exit")

if __name__ == '__main__':
    main()