import numpy as np
import pandas as pd
import talib as ta


class MockBroker:
    def __init__(self, Balance, price):
        self.holdings = {}
        self.holdingsprofitat = {}
        self.Balance = Balance
        self.highestnetworth = 0
        self.price = price
        self.equity = 0
        self.networth = []
        self.stocksTraded = set()
        self.blacklistedstocks = {}

    def __str__(self):
        return "Equity: " + str(self.equity) + "\n Holdings: " + str(self.holdings) + "\n Balance: " + str(self.Balance) + "\n Total: " + str(self.networth[-1]) + "\n Highest Net Worth: " + str(self.highestnetworth) +  "\n Profit off Stocks: " + str(self.holdingsprofitat)

    def managenetworth(self, i):
        self.equity = 0
        for key, value in self.holdings.items():
            self.equity += self.price.get(key, [0])[i] * value
        current_networth = self.equity + self.Balance
        self.networth.append(current_networth)
    
        if (current_networth > self.highestnetworth):
            self.highestnetworth = current_networth

        print("Networth: " +str(current_networth))

    def buy(self, stock, price, qty):
        if self.Balance >= price * int(qty):
            org_qty = int(self.holdings.get(stock, 0))
            self.holdings.update({stock: org_qty + int(qty)})
            org_profit = int(self.holdingsprofitat.get(stock,0))
            self.holdingsprofitat.update({stock: org_profit-(price*int(qty))})
            self.Balance -= price * int(qty)
            print(f"Bought {qty} of {stock} at {price} each")
            # print(self.holdings)
            
            print("Balance: " + str(self.Balance))
            self.stocksTraded.add(stock)
        else:
            print("Not enough balance")

    def sell(self, stock, price, qty):
        org_qty = int(self.holdings.get(stock, 0))
        org_profit = int(self.holdingsprofitat.get(stock, 0))
        if org_qty >= int(qty):
            self.holdings.update({stock: org_qty - int(qty)})
            self.Balance += price * int(qty)
            self.holdingsprofitat.update({stock: org_profit + price*int(qty)})
            if (qty>0):
                print(f"Sold {qty} of {stock} at {price} each")
                # print(self.holdings)
                print("Balance: " + str(self.Balance))
        else:
            print("Can't sell more than bought")

    def sell_off(self, i):
        for key, value in self.holdings.items():
            self.sell(key,self.price[key][i], value)
        self.managenetworth(i)

    def sell_off_if(self, i):
        for key, value in self.holdings.items():
            if (self.holdingsprofitat.get(key, 0) + (self.price[key][i] * int(value)) > 0):
                self.sell(key,self.price[key][i], value)
        self.managenetworth(i)

    def sell_off_if_thres(self, i, thres):
        for key, value in self.holdings.items():
            if ((self.holdingsprofitat.get(key, 0) + (self.price[key][i] * int(value)) < -thres) | (self.holdingsprofitat.get(key, 0) + (self.price[key][i] * int(value)) > 0) ):
                self.sell(key,self.price[key][i], value)
        self.managenetworth(i)

    def sell_off_if_thres_blacklist(self, i, thres, bt):
        for key, value in self.holdings.items():
            if ((self.holdingsprofitat.get(key, 0) + (self.price[key][i] * int(value)) < -thres) ):
                self.sell(key,self.price[key][i], value)
                org_black = int(self.blacklistedstocks.get(key, 0))
                self.holdings.update({key: org_black + 1})

            if ((self.holdingsprofitat.get(key, 0) + (self.price[key][i] * int(value)) > 0) ):
                self.sell(key,self.price[key][i], value)
        self.managenetworth(i)

    def blacklist(self, stock):
        self.blacklistedstocks.add(stock)



    def get_holdings(self):
        return self.holdings
