#!/usr/bin/python
# -*- coding: utf-8 -*-

def trading(price,KEY,BuyingPoint,SellgingPoint1,SellingPoint2,AccountAmount):
      if  KEY >= BuyingPoint:
        if AccountAmount!=0:
           volume=AccountAmount/price
           BuyingPrice=price
           AccountAmount=0
           
      else:
          volume=0
      CurrentAmount=volume*price
      if AccountAmount==0:
          if price>=SellgingPoint1*BuyingPrice or price<=SellgingPoint1*BuyingPrice:
              CurrentAmount=0
              AccountAmount=volume*price
              volume=0
              
      Amount=AccountAmount+CurrentAmount
      return Amount        
    
